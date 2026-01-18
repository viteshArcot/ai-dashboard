# ML Methodology Documentation

## Model Selection Rationale

### Linear Regression (Continuous Targets)
- **Why chosen**: Interpretable baseline model, fast training, clear feature relationships
- **Best for**: Linear relationships, small datasets, when interpretability is crucial
- **Assumptions**: Linear relationship between features and target, normally distributed residuals

### Random Forest Classifier (Categorical Targets)
- **Why chosen**: Handles non-linear relationships, robust to outliers, provides feature importance
- **Best for**: Complex feature interactions, mixed data types, when accuracy > interpretability
- **Advantages**: No feature scaling required, handles missing values, reduces overfitting

### Decision Logic
```
if target_is_numeric:
    use LinearRegression  # Continuous prediction
else:
    use RandomForestClassifier  # Discrete classification
```

## Training Pipeline Explanation

### Train/Test Split (80/20)
- **Rationale**: Industry standard providing sufficient evaluation data
- **Random state=42**: Ensures reproducible results across runs
- **Why not 90/10**: Need adequate test data for reliable performance estimates
- **Why not 70/30**: Maximizes training data while maintaining evaluation reliability

### Data Leakage Prevention
- **Target separation**: Target column removed from features before training
- **No future data**: Only historical data used for predictions
- **No target-derived features**: Features don't contain information from target variable
- **Temporal consistency**: No look-ahead bias in feature engineering

## Evaluation Metrics Deep Dive

### R² Score (Regression)
- **Definition**: Proportion of variance in target explained by model
- **Range**: 0 to 1 (higher is better)
- **Interpretation**:
  - >0.7: Good predictive power
  - 0.5-0.7: Moderate performance
  - <0.5: Poor, consider different approach
- **Formula**: 1 - (SS_res / SS_tot)

### Accuracy (Classification)
- **Definition**: Percentage of correct predictions
- **Range**: 0 to 1 (higher is better)
- **Interpretation**:
  - >0.8: Good performance
  - 0.6-0.8: Acceptable
  - <0.6: Poor performance
- **Limitation**: Can be misleading with imbalanced datasets

## Current Limitations

### Model Limitations
- **No cross-validation**: Single train/test split may not represent true performance
- **No hyperparameter tuning**: Using default parameters, not optimized
- **No feature scaling**: Linear regression may benefit from standardization
- **No imbalanced data handling**: Classification assumes balanced classes

### Data Processing Limitations
- **Simple imputation**: Mean filling may not be optimal strategy
- **Basic encoding**: LabelEncoder assumes ordinal relationships
- **No feature selection**: Using all features without relevance filtering
- **No outlier handling**: Extreme values may skew model performance

### Future Improvements
1. Implement k-fold cross-validation
2. Add hyperparameter optimization (GridSearch/RandomSearch)
3. Include feature scaling for regression models
4. Add class balancing for classification
5. Implement more sophisticated imputation strategies