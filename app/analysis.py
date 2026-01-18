import pandas as pd
import numpy as np
import json
from scipy import stats as scipy_stats

def perform_eda(df):
    """Enhanced exploratory data analysis with deeper insights"""
    try:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        # Basic stats
        basic_stats = {
            "shape": [int(df.shape[0]), int(df.shape[1])],
            "columns": list(df.columns),
            "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
            "missing_values": {str(k): int(v) for k, v in df.isnull().sum().items()},
            "memory_usage_mb": float(round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2))
        }
    
        # Enhanced numeric statistics
        numeric_insights = {}
        if len(numeric_cols) > 0:
            for col in numeric_cols:
                try:
                    data = df[col].dropna()
                    if len(data) > 0:
                        numeric_insights[str(col)] = {
                            "mean": float(round(data.mean(), 3)),
                            "median": float(round(data.median(), 3)),
                            "std": float(round(data.std(), 3)),
                            "min": float(round(data.min(), 3)),
                            "max": float(round(data.max(), 3)),
                            "skewness": float(round(scipy_stats.skew(data), 3)),
                            "kurtosis": float(round(scipy_stats.kurtosis(data), 3)),
                            "outliers_count": int(len(detect_outliers(data))),
                            "unique_values": int(data.nunique()),
                            "zero_count": int((data == 0).sum())
                        }
                except Exception as e:
                    numeric_insights[str(col)] = {"error": str(e)}
    
        # Categorical insights
        categorical_insights = {}
        if len(categorical_cols) > 0:
            for col in categorical_cols:
                try:
                    data = df[col].dropna()
                    if len(data) > 0:
                        value_counts = data.value_counts()
                        categorical_insights[str(col)] = {
                            "unique_count": int(data.nunique()),
                            "most_frequent": str(value_counts.index[0]) if len(value_counts) > 0 else None,
                            "most_frequent_count": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                            "diversity_ratio": float(round(data.nunique() / len(data), 3)),
                            "top_categories": {str(k): int(v) for k, v in value_counts.head(5).items()}
                        }
                except Exception as e:
                    categorical_insights[str(col)] = {"error": str(e)}
    
        # Data quality metrics
        quality_metrics = {
            "completeness_ratio": float(round((df.size - df.isnull().sum().sum()) / df.size, 3)),
            "duplicate_rows": int(df.duplicated().sum()),
            "columns_with_missing": int((df.isnull().sum() > 0).sum()),
            "numeric_columns": int(len(numeric_cols)),
            "categorical_columns": int(len(categorical_cols))
        }
    
        # Correlations for numeric data
        correlations = {}
        if len(numeric_cols) > 1:
            try:
                corr_matrix = df[numeric_cols].corr()
                # Find strongest correlations
                corr_pairs = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        col1, col2 = corr_matrix.columns[i], corr_matrix.columns[j]
                        corr_val = corr_matrix.iloc[i, j]
                        if not np.isnan(corr_val) and abs(corr_val) > 0.5:
                            corr_pairs.append({
                                "column1": str(col1),
                                "column2": str(col2),
                                "correlation": float(round(corr_val, 3))
                            })
                # Convert correlation matrix to serializable format
                matrix_dict = {}
                for col in corr_matrix.columns:
                    matrix_dict[str(col)] = {str(k): float(v) if not np.isnan(v) else 0.0 for k, v in corr_matrix[col].items()}
                
                correlations = {
                    "matrix": matrix_dict,
                    "strong_correlations": sorted(corr_pairs, key=lambda x: abs(x["correlation"]), reverse=True)
                }
            except Exception as e:
                correlations = {"error": str(e)}
    
        return {
            **basic_stats,
            "numeric_insights": numeric_insights,
            "categorical_insights": categorical_insights,
            "quality_metrics": quality_metrics,
            "correlations": correlations
        }
    except Exception as e:
        return {
            "shape": [0, 0],
            "columns": [],
            "dtypes": {},
            "missing_values": {},
            "error": str(e)
        }

def detect_outliers(data, method='iqr'):
    """Detect outliers using IQR method"""
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data < lower_bound) | (data > upper_bound)]

def get_chart_data(df):
    """Extract data for chart generation"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    chart_data = {
        "numeric_columns": list(numeric_cols),
        "categorical_columns": list(categorical_cols),
        "sample_data": df.head(10).to_dict('records')
    }
    
    return chart_data