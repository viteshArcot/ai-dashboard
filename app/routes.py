from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import json
import time
from datetime import datetime

from .database import get_db, Dataset, Analysis, MLModel
from .analysis import perform_eda, get_chart_data
from .visualization import generate_charts
from .llm import generate_summary
from .ml import train_model

router = APIRouter(prefix="/api/v1")

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload CSV file and store metadata"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        # Read CSV
        content = await file.read()
        df = pd.read_csv(pd.io.common.StringIO(content.decode('utf-8')))
        
        # Store dataset metadata
        dataset = Dataset(
            name=file.filename.split('.')[0],
            filename=file.filename,
            rows=int(len(df)),
            columns=int(len(df.columns))
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        
        # Save CSV file
        with open(f"static/dataset_{dataset.id}.csv", "wb") as f:
            f.write(content)
        
        return {
            "dataset_id": dataset.id,
            "message": "Dataset uploaded successfully",
            "rows": len(df),
            "columns": len(df.columns)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@router.get("/analyze/{dataset_id}")
async def analyze_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Perform analysis on uploaded dataset"""
    start_time = time.time()
    
    # Get dataset
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        # Load dataset
        df = pd.read_csv(f"static/dataset_{dataset_id}.csv")
        
        # Perform EDA
        stats = perform_eda(df)
        
        # Generate charts
        chart_urls = generate_charts(df, dataset_id)
        
        # Generate summary
        summary = await generate_summary(stats)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Store analysis with safe JSON serialization
        try:
            stats_json = json.dumps(stats, default=str)
        except:
            stats_json = json.dumps({"error": "Stats serialization failed"})
        
        analysis = Analysis(
            dataset_id=dataset_id,
            processing_time=processing_time,
            summary=summary,
            stats=stats_json,
            type="EDA"
        )
        db.add(analysis)
        db.commit()
        
        return {
            "stats": stats,
            "charts": chart_urls,
            "summary": summary,
            "processing_time": processing_time
        }
    
    except Exception as e:
        import traceback
        print(f"Analysis error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error analyzing dataset: {str(e)}")

@router.get("/history")
async def get_analysis_history(db: Session = Depends(get_db)):
    """Get last 10 analyses"""
    analyses = db.query(Analysis, Dataset).join(Dataset, Analysis.dataset_id == Dataset.id).order_by(Analysis.analysis_time.desc()).limit(10).all()
    
    history = []
    for analysis, dataset in analyses:
        history.append({
            "dataset_name": dataset.name,
            "timestamp": analysis.analysis_time.isoformat(),
            "summary": analysis.summary,
            "processing_time": analysis.processing_time
        })
    
    return {"history": history}

@router.get("/metrics")
async def get_system_metrics(db: Session = Depends(get_db)):
    """Get system metrics"""
    total_datasets = db.query(Dataset).count()
    total_analyses = db.query(Analysis).count()
    
    from sqlalchemy import func
    avg_processing_time = db.query(func.avg(Analysis.processing_time)).scalar() or 0
    
    return {
        "total_datasets": total_datasets,
        "total_analyses": total_analyses,
        "avg_processing_time": round(avg_processing_time, 2)
    }

@router.post("/train")
async def train_ml_model(
    dataset_id: int, 
    target_column: str, 
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """Train ML model on dataset"""
    start_time = time.time()
    
    # Get dataset
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        # Load dataset - either from file upload or existing dataset
        if file:
            # Handle new file upload
            content = await file.read()
            df = pd.read_csv(pd.io.common.StringIO(content.decode('utf-8')))
        else:
            # Use existing dataset
            df = pd.read_csv(f"static/dataset_{dataset_id}.csv")
        
        # Train model
        result = train_model(df, target_column, dataset_id)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Store model metadata
        ml_model = MLModel(
            dataset_id=dataset_id,
            model_name=result["model_name"],
            target_column=target_column,
            model_type=result["model_type"],
            algorithm=result["algorithm"],
            score=result["score"],
            feature_importance=json.dumps(result["feature_importance"]),
            model_path=result["model_path"],
            chart_path=result["chart_path"]
        )
        db.add(ml_model)
        
        # Log training in analysis history
        analysis = Analysis(
            dataset_id=dataset_id,
            processing_time=processing_time,
            summary=f"Trained {result['algorithm']} model for {target_column}. {result['score_name']}: {result['score']:.4f}",
            stats=json.dumps({
                "model_type": result["model_type"],
                "algorithm": result["algorithm"],
                "score": result["score"],
                "n_features": result["n_features"],
                "n_samples": result["n_samples"]
            }),
            type="ML Training"
        )
        db.add(analysis)
        db.commit()
        
        return {
            "model_name": result["model_name"],
            "model_type": result["model_type"],
            "algorithm": result["algorithm"],
            "score": result["score"],
            "score_name": result["score_name"],
            "feature_importance": result["feature_importance"],
            "chart_url": result["chart_path"],
            "processing_time": processing_time,
            "data_split": result["train_test_split"],
            "preprocessing": result["preprocessing_applied"],
            "assumptions": result["model_assumptions"],
            "interpretation": result["performance_interpretation"],
            "trust_level": result["trust_level"],
            "warnings": result["performance_warnings"] + result["feature_importance_warnings"]
        }
        
    except Exception as e:
        import traceback
        print(f"ML training error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error training model: {str(e)}")

@router.get("/models")
async def get_ml_models(db: Session = Depends(get_db)):
    """Get all trained models metadata"""
    models = db.query(MLModel, Dataset).join(Dataset, MLModel.dataset_id == Dataset.id).order_by(MLModel.created_at.desc()).all()
    
    model_list = []
    for ml_model, dataset in models:
        model_list.append({
            "id": ml_model.id,
            "model_name": ml_model.model_name,
            "dataset_name": dataset.name,
            "target_column": ml_model.target_column,
            "model_type": ml_model.model_type,
            "algorithm": ml_model.algorithm,
            "score": ml_model.score,
            "feature_importance": json.loads(ml_model.feature_importance) if ml_model.feature_importance else {},
            "chart_url": ml_model.chart_path,
            "created_at": ml_model.created_at.isoformat()
        })
    
    return {"models": model_list}