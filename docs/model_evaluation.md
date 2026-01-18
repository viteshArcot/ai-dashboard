# Notes on Model Performance and What Scores Actually Mean

After training a bunch of models and getting burned by misleading metrics, here's what I've learned about interpreting performance.

## R² Score (Regression)

What it actually measures: How much of the variation in the target the model explains.

My practical interpretation:
- **0.8+**: Pretty excellent - model is capturing most of the patterns
- **0.6-0.8**: Good enough for most purposes, might be worth refining
- **0.4-0.6**: Okay, there's signal but lots of room for improvement
- **0.2-0.4**: Weak - barely better than simple rules
- **Below 0.2**: Poor - model isn't finding real patterns
- **Negative**: Something's broken - model is worse than just predicting the average

## Accuracy (Classification)

What it measures: Percentage of correct predictions.

What I've learned to expect:
- **0.9+**: Excellent, but I always double-check for data leakage or class imbalance
- **0.8-0.9**: Solid performance, usually good enough for real use
- **0.7-0.8**: Decent, acceptable depending on what you're trying to do
- **0.6-0.7**: Weak but better than random
- **0.5-0.6**: Poor, barely better than guessing
- **Below 0.5**: Broken - check your code

## When Metrics Lie

I've been fooled by metrics enough times to be suspicious:

**High accuracy red flags**: Class imbalance (95% accuracy when 95% of data is one class), data leakage (suspiciously perfect scores), overfitting (great on training, terrible on test).

**R² gotchas**: Small datasets (high R² often just noise), outliers (few extreme values inflate the score), non-linear relationships (low R² even with strong patterns).

## Signs Something's Wrong

**Overfitting**: Training score much higher than test, very high scores on small datasets, performance drops on new data.

**Underfitting**: Both training and test scores are low, adding features doesn't help, performance plateaus quickly.

**Data issues**: Scores vary wildly between runs, inconsistent performance across data subsets.

## When I Don't Trust Results

I'm extra careful when:
- Dataset is small (< 100 samples)
- Features are highly correlated
- Target distribution is weird
- Performance seems too good (usually indicates a problem)
- Data collection process changed

## What I Do When Scores Are Bad

**Low R²**: Check for outliers, try polynomial features, look for missing important features, question if the problem is actually predictable.

**Low accuracy**: Check class balance, look at confusion matrix, try feature engineering, consider if classes are actually distinguishable.

## Metrics I Should Use But Don't

For classification: Precision/Recall (better for imbalanced classes), F1-Score, ROC-AUC.
For regression: Mean Absolute Error (more interpretable), RMSE (penalizes large errors).

I stick with R² and accuracy because they're simple to explain, but these others would give better insights.

## Bottom Line

Metrics are useful but not the whole story. I always combine them with visual inspection, domain knowledge, and common sense. The goal isn't to maximize metrics - it's to build something that actually works.