# Model Performance Interpretation Guide

## Regression Performance (R² Score)

### Performance Ranges
- **0.9-1.0: Excellent** 
  - Model explains 90%+ of variance
  - ⚠️ **Warning**: May indicate overfitting, especially with small datasets
  - **Action**: Validate on additional test data

- **0.7-0.9: Good**
  - Strong predictive power
  - Suitable for most business applications
  - **Action**: Consider minor improvements

- **0.5-0.7: Moderate**
  - Room for improvement exists
  - May be acceptable depending on domain complexity
  - **Action**: Try feature engineering or different algorithms

- **<0.5: Poor**
  - Model barely better than predicting the mean
  - **Action**: Reconsider approach, check data quality, try non-linear models

### Common Issues
- **Negative R²**: Model worse than baseline (predicting mean)
- **R² = 1.0**: Perfect fit, likely overfitting or data leakage
- **Inconsistent performance**: High variance, need more data or regularization

## Classification Performance (Accuracy)

### Performance Ranges
- **>0.95: Excellent**
  - Very high accuracy
  - ⚠️ **Warning**: Check for data leakage or class imbalance
  - **Action**: Validate assumptions and data integrity

- **0.85-0.95: Good**
  - Strong classification performance
  - Suitable for production deployment
  - **Action**: Monitor for concept drift

- **0.70-0.85: Acceptable**
  - Decent performance, can be improved
  - **Action**: Feature engineering, hyperparameter tuning

- **<0.70: Poor**
  - Needs significant improvement
  - **Action**: Try different algorithms, collect more data

### Accuracy Limitations
- **Class imbalance**: High accuracy can be misleading with skewed classes
- **Cost sensitivity**: Some errors may be more costly than others
- **Multi-class complexity**: Harder to achieve high accuracy with many classes

## When Models Typically Fail

### Linear Regression Failures
- **Non-linear relationships**: Curved or complex patterns in data
- **Outliers**: Extreme values heavily influence the model
- **Multicollinearity**: Highly correlated features cause instability
- **Heteroscedasticity**: Non-constant variance in residuals

### Random Forest Failures
- **Very high dimensions**: Curse of dimensionality with sparse data
- **Linear relationships**: Overkill for simple linear patterns
- **Extrapolation**: Poor performance outside training data range
- **Memory constraints**: Large forests require significant resources

## Performance Monitoring

### Red Flags
- Sudden performance drops in production
- Large gap between training and test performance
- Inconsistent results across different data subsets
- Performance varies significantly with small data changes

### Best Practices
- Always compare against simple baselines
- Use multiple evaluation metrics when possible
- Validate performance on recent, unseen data
- Monitor performance over time in production