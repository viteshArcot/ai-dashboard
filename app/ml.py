import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import joblib
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import r2_score, accuracy_score
from sklearn.preprocessing import LabelEncoder
import os

def determine_model_type(target_series):
    """Determine if target is numeric (regression) or categorical (classification)"""
    if pd.api.types.is_numeric_dtype(target_series):
        return "regression", "LinearRegression"
    else:
        return "classification", "RandomForestClassifier"

def prepare_features(df, target_column):
    """
    Basic feature preprocessing that I've found works reliably.
    
    I keep this simple on purpose - I've learned that complex preprocessing
    often introduces bugs that are hard to track down. Better to start
    simple and add complexity only when needed.
    """
    # Separate features from target - learned this lesson the hard way
    # My first models had suspiciously good performance due to data leakage
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # Convert categorical features to numbers using LabelEncoder
    # This assumes some ordering which isn't always true, but Random Forest handles it okay
    categorical_cols = X.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
    
    # Fill missing values with column mean - simple but works for most cases
    # TODO: Could be smarter about this, but good enough for now
    X = X.fillna(X.mean() if len(X.select_dtypes(include=[np.number]).columns) > 0 else 0)
    
    return X, y

def train_model(df, target_column, dataset_id):
    """
    Train ML model with simple algorithm selection.
    
    I chose this approach because it's reliable and interpretable.
    Starting with simple models helps me understand the data before
    trying anything complex. Plus, these models are easy to debug
    when things go wrong.
    """
    try:
        # Validate target column
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset")
        
        # Remove rows with missing target values
        df_clean = df.dropna(subset=[target_column])
        if len(df_clean) < 10:
            raise ValueError("Insufficient data after removing missing target values")
        
        # Prepare features
        X, y = prepare_features(df_clean, target_column)
        
        # Simple logic: numeric target = regression, categorical = classification
        model_type, algorithm = determine_model_type(y)
        
        # Handle categorical target for classification
        if model_type == "classification":
            le_target = LabelEncoder()
            y_encoded = le_target.fit_transform(y.astype(str))
        else:
            y_encoded = y
        
        # I've found this works well in practice - 80% for training, 20% for testing
        # Using random_state=42 so I get consistent results (makes debugging easier)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42
        )
        
        # I always start with Linear Regression for continuous targets
        # It's interpretable - I can see exactly how each feature contributes
        # Plus it's fast and serves as a good baseline to beat
        if model_type == "regression":
            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = r2_score(y_test, y_pred)
            score_name = "R² Score"
        else:
            # Random Forest for classification because it handles complexity well
            # Doesn't need feature scaling, handles mixed data types, robust to outliers
            # The 100 trees is a good balance - more trees = better but slower
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = accuracy_score(y_test, y_pred)
            score_name = "Accuracy"
        
        # Get feature importance and check if it's reliable
        # This helps understand what drives predictions, but can be misleading
        if hasattr(model, 'feature_importances_'):
            importance = dict(zip(X.columns, model.feature_importances_))
        elif hasattr(model, 'coef_'):
            # For linear regression, use absolute coefficients
            importance = dict(zip(X.columns, abs(model.coef_)))
        else:
            importance = {}
        
        # Sort by importance and check reliability
        importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
        importance_warnings = analyze_feature_importance_reliability(importance, len(df_clean))
        
        # Generate model name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = f"model_{dataset_id}_{target_column}_{timestamp}"
        
        # Save model
        model_path = f"models/{model_name}.joblib"
        joblib.dump(model, model_path)
        
        # Create feature importance plot
        chart_path = create_importance_plot(importance, model_name, target_column)
        
        performance_result = get_performance_interpretation(score, model_type)
        
        return {
            "model_name": model_name,
            "model_type": model_type,
            "algorithm": algorithm,
            "score": float(round(score, 4)),
            "score_name": score_name,
            "feature_importance": importance,
            "model_path": model_path,
            "chart_path": chart_path,
            "n_features": len(X.columns),
            "n_samples": len(df_clean),
            "train_test_split": "80/20",
            "preprocessing_applied": ["categorical_encoding", "missing_value_imputation"],
            "model_assumptions": get_model_assumptions(model_type),
            "performance_interpretation": performance_result["interpretation"],
            "trust_level": performance_result["trust_level"],
            "performance_warnings": performance_result["warnings"],
            "feature_importance_warnings": importance_warnings
        }
        
    except Exception as e:
        raise Exception(f"Model training failed: {str(e)}")

def create_importance_plot(importance, model_name, target_column):
    """Create feature importance visualization"""
    if not importance:
        return None
    
    # Take top 10 features
    top_features = dict(list(importance.items())[:10])
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#0a0a0a')
    
    features = list(top_features.keys())
    importances = list(top_features.values())
    
    # Create horizontal bar plot
    colors = plt.cm.viridis(np.linspace(0, 1, len(features)))
    bars = ax.barh(features, importances, color=colors, alpha=0.8)
    
    # Customize plot
    ax.set_xlabel('Feature Importance', fontsize=12, color='#ccc')
    ax.set_title(f'Feature Importance: {target_column}', fontsize=16, fontweight='300', color='white', pad=20)
    ax.grid(True, alpha=0.2, axis='x')
    
    # Add value labels
    for bar, importance in zip(bars, importances):
        width = bar.get_width()
        ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
                f'{importance:.3f}', ha='left', va='center', fontsize=10, color='white')
    
    plt.tight_layout()
    
    # Save plot
    chart_filename = f"feature_importance_{model_name}.png"
    chart_path = f"static/{chart_filename}"
    plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
    plt.close()
    
    return f"/static/{chart_filename}"

def load_model(model_path):
    """Load trained model from file"""
    try:
        return joblib.load(model_path)
    except Exception as e:
        raise Exception(f"Failed to load model: {str(e)}")

def get_performance_warnings(score, model_type):
    """Flag potential issues I've learned to watch out for"""
    warnings = []
    
    if model_type == "regression":
        if score > 0.95:
            warnings.append("Very high R² - check for overfitting or data leakage")
        if score < 0.0:
            warnings.append("Negative R² means model is worse than predicting the mean")
    else:
        if score > 0.95:
            warnings.append("Very high accuracy - might be overfitting or class imbalance")
        if score < 0.6:
            warnings.append("Low accuracy - check if classes are balanced")
    
    return warnings

def analyze_feature_importance_reliability(importance_dict, n_samples):
    """Check if feature importance can be trusted"""
    warnings = []
    
    if n_samples < 100:
        warnings.append("Small dataset - feature importance may be unreliable")
    
    # Check if one feature dominates
    if importance_dict:
        max_importance = max(importance_dict.values())
        if max_importance > 0.8:
            warnings.append("One feature dominates - might indicate data leakage")
    
    return warnings

def get_model_assumptions(model_type):
    """What I assume when using these models"""
    if model_type == "regression":
        return [
            "Linear relationship between features and target",
            "Features aren't too correlated with each other",
            "No major outliers skewing the results",
            "Enough data points to be reliable"
        ]
    else:
        return [
            "Classes are reasonably balanced",
            "Features actually help distinguish between classes",
            "Training data represents future data well",
            "No systematic bias in the data collection"
        ]

def get_performance_interpretation(score, model_type):
    """Interpret performance based on what I've learned works in practice"""
    if model_type == "regression":
        if score >= 0.7:
            interpretation = "Pretty good - explains most of the variation. Ready for initial insights."
            trust_level = "high"
        elif score >= 0.5:
            interpretation = "Okay, but could be better. Might need more features or different approach."
            trust_level = "medium"
        elif score >= 0.0:
            interpretation = "Not great - model is struggling to find patterns. Check data quality."
            trust_level = "low"
        else:
            interpretation = "Worse than just predicting the average. Something's wrong with the data or approach."
            trust_level = "very_low"
    else:
        if score >= 0.8:
            interpretation = "Solid performance for most business use cases. Good enough to act on."
            trust_level = "high"
        elif score >= 0.6:
            interpretation = "Decent, might be acceptable depending on the problem. Could improve with more data."
            trust_level = "medium"
        elif score >= 0.5:
            interpretation = "Better than random guessing, but needs work. Try different features."
            trust_level = "low"
        else:
            interpretation = "Poor performance - barely better than random. Need to rethink approach."
            trust_level = "very_low"
    
    return {
        "interpretation": interpretation,
        "trust_level": trust_level,
        "warnings": get_performance_warnings(score, model_type)
    }

def get_model_info(model_path):
    """Get basic info about a saved model"""
    try:
        model = load_model(model_path)
        return {
            "type": type(model).__name__,
            "n_features": getattr(model, 'n_features_in_', 'Unknown')
        }
    except:
        return {"type": "Unknown", "n_features": "Unknown"}