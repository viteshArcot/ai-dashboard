# My ML Decisions and Why I Made Them

These are basically my notes on why I chose certain approaches. Mostly written after debugging sessions when I finally understood what was going on.

## Model Choices

I went through a few iterations before settling on the current approach.

### Linear Regression for Continuous Stuff

I always start here because:
- You can actually understand what it's doing (each coefficient tells you something)
- It's fast, which is nice when you're experimenting
- Makes a good baseline - if something fancier can't beat linear regression, maybe the problem isn't that complex
- When it breaks, it's usually obvious why

The big assumption is that relationships are roughly linear. This isn't always true, but it's a reasonable starting point.

### Random Forest for Categories

For classification, I picked Random Forest after trying a few things:
- Handles weird feature interactions without me having to think about it
- Pretty robust to outliers and messy data
- Doesn't need much preprocessing (no scaling, handles mixed data types)
- Gives you feature importance for free

Downside is it's less interpretable, but usually the performance trade-off is worth it.

## How I Pick Algorithms

Super simple logic:
```
if target_is_numeric:
    use LinearRegression()
else:
    use RandomForestClassifier()
```

Not sophisticated, but it works. I tried building more complex selection logic but it usually just made things worse.

## Why Simple Models First

I learned this the hard way. My first version used XGBoost with tons of hyperparameter tuning and complex feature engineering. Took forever to debug and didn't perform much better than the simple approach.

Current philosophy: get something working, understand the data, then optimize if you actually need to.

## Trade-offs I Made

**Interpretability vs Performance**: Linear regression is easy to explain but might miss complex patterns. Random Forest captures more complexity but is harder to interpret. I use both depending on the problem.

**Simplicity vs Sophistication**: Could use ensemble methods, neural networks, etc. Chose simple models because they're easier to debug when things go wrong.

**Speed vs Accuracy**: Could do extensive hyperparameter tuning but chose reasonable defaults for faster iteration.

## What This Doesn't Handle

Being honest about limitations:
- Non-linear relationships (Linear Regression struggles)
- Really high-dimensional data (both models can have issues)
- Time series (neither handles temporal patterns)
- Severely imbalanced classes (Random Forest biased toward majority)
- Causal inference (these are predictive models, not causal)

## If I Were to Extend This

Future considerations (probably won't implement, but good to think about):
1. Regularized regression (Ridge/Lasso) for high-dimensional data
2. Gradient boosting (XGBoost) for better performance
3. Logistic regression for interpretable classification
4. Cross-validation for better model selection

But the current approach works for learning the fundamentals.