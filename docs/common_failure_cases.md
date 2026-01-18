# Where My Models Break (and Why)

After testing this system on different datasets, I've figured out the patterns of where it fails. Writing this down mostly so I remember for next time.

## Linear Regression Problems

**Non-linear relationships**: R² stays low even with decent features. Linear regression assumes straight lines, so when the real relationship is curved or has interactions, it just can't capture it. Like trying to predict house prices where location effects are exponential.

**Outliers mess everything up**: One mansion in a dataset of normal houses can skew all predictions. Linear regression tries to minimize squared errors, so outliers have huge influence.

**Multicollinearity issues**: When features are highly correlated (like square footage and number of rooms), coefficients become unstable and feature importance becomes meaningless.

## Random Forest Problems

**Overkill for linear stuff**: Works fine but unnecessarily complex for simple linear relationships. It creates step-like decision boundaries when a smooth line would work better.

**High-dimensional sparse data**: Performance gets worse, training slows down. With many features and few samples, trees can't find reliable splits.

**Can't extrapolate**: Predictions become unreliable outside the training range. Tree models can only predict values they've seen before.

## Data-Related Failures

**Small datasets (< 100 samples)**: High variance, unreliable feature importance. Not enough data to learn stable patterns. I'm always skeptical of results with small datasets.

**Imbalanced classes**: High accuracy but terrible performance on minority class. Model learns to just predict the majority class. Classic fraud detection problem.

**Data leakage**: Suspiciously high performance that doesn't generalize. Usually means the model has access to information it wouldn't have in production. Like including "total_spent_next_month" to predict "will_churn_next_month".

**Concept drift**: Performance degrades over time because relationships change. Customer behavior model trained pre-pandemic fails during pandemic.

## Feature Issues

**Irrelevant features dominate**: Feature importance points to meaningless variables due to random correlations. "Customer ID" showing high importance is a red flag.

**Missing key info**: Low performance despite good features because the most predictive information isn't in the dataset.

**Categorical encoding problems**: LabelEncoder creates artificial ordering that confuses models. Encoding city names as numbers implies some cities are "greater" than others.

## Red Flags I Watch For

- Performance varies wildly between runs
- Feature importance changes dramatically with small data changes  
- Great training performance, terrible validation
- Results don't make business sense
- One feature has >80% importance (usually leakage)

## Diagnostic Questions

1. Is the dataset large enough to be reliable?
2. Are features actually available at prediction time?
3. Do important features make intuitive sense?
4. Is the target well-defined and consistent?
5. Are there obvious patterns the model should catch but isn't?

## What Would Actually Fix These

**Better regression**: Polynomial features for non-linear relationships, regularization for multicollinearity, robust methods for outliers.

**Better classification**: Class balancing, different metrics (precision/recall), ensemble methods, better categorical encoding.

**Better data handling**: Cross-validation, feature selection, time-based splits, proper train/validation/test splits.

## Honest Assessment

Most of these improvements aren't in my current system. This was a conscious trade-off - I wanted to get something working and understandable rather than handle every edge case.

In production, I'd address these systematically. But for learning, acknowledging the limitations is more important than solving every problem perfectly.

Key insight: every model fails somewhere. The question is whether you understand where and why.