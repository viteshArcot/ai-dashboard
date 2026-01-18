# How I Evaluate Models

## Train/Test Split Strategy

I use an 80/20 split because:
- 80% gives the model enough data to learn patterns
- 20% is sufficient to get a reliable performance estimate
- It's what most people use, so results are comparable

I set `random_state=42` so I get the same split every time. This makes debugging easier and results reproducible.

## Preventing Data Leakage

This was something I learned the hard way in a previous project. Here's how I avoid it:

1. **Separate target first** - Remove the target column before any preprocessing
2. **No future information** - Only use data that would be available at prediction time
3. **Consistent preprocessing** - Apply the same transformations to train and test

The key insight: if the model has access to information it wouldn't have in production, your performance estimates will be overly optimistic.

## Understanding the Metrics

### R² Score (Regression)
Think of R² as "how much of the variation in my target can the model explain?"
- R² = 0.8 means the model explains 80% of why values differ
- R² = 0 means the model is no better than just predicting the average
- Negative R² means the model is worse than predicting the average (bad sign!)

### Accuracy (Classification)
Simple: what percentage of predictions are correct?
- Accuracy = 0.85 means 85% of predictions are right
- But be careful with imbalanced data - 95% accuracy sounds great until you realize 95% of your data is one class

## When Metrics Can Mislead

**Class Imbalance Problem**
If 99% of emails are not spam, a model that always predicts "not spam" gets 99% accuracy but is useless.

**Overfitting Red Flags**
- Training accuracy much higher than test accuracy
- Performance drops significantly on new data
- Model memorized training examples instead of learning patterns

**Distribution Shift**
Model trained on summer data might fail in winter. Always check if test data matches production conditions.

## What I'm Not Doing (Yet)

- **Cross-validation**: Would give more robust performance estimates
- **Precision/Recall**: Important for imbalanced classification problems  
- **Learning curves**: Would help diagnose overfitting vs underfitting
- **Feature importance analysis**: Random Forest provides this, should use it more

These aren't implemented yet but would be my next priorities for improving evaluation.