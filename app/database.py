from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from datetime import datetime

DATABASE_URL = "sqlite:///./dashboard.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    filename = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)
    rows = Column(Integer)
    columns = Column(Integer)

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer)
    analysis_time = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Float)
    summary = Column(Text)
    stats = Column(Text)
    type = Column(String, default="EDA")  # "EDA" or "ML Training"

class MLModel(Base):
    __tablename__ = "ml_models"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer)
    model_name = Column(String, index=True)
    target_column = Column(String)
    model_type = Column(String)  # "regression" or "classification"
    algorithm = Column(String)  # "LinearRegression" or "RandomForestClassifier"
    score = Column(Float)
    feature_importance = Column(Text)  # JSON string
    model_path = Column(String)
    chart_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Recreate tables with new schema
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()