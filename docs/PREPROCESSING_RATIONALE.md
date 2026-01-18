# Data Preprocessing Decisions

## Why I Handle Categorical Data This Way

I use `LabelEncoder` for categorical features because:
- It's simple and works well with Random Forest
- Doesn't explode the feature space like one-hot encoding
- Random Forest can handle the implied ordering even when it doesn't exist

**Trade-off**: LabelEncoder assumes categories have an order (red=0, blue=1, green=2 implies green > blue > red). This isn't always true, but tree-based models handle it reasonably well.

**Alternative I considered**: One-hot encoding creates a column for each category. Better for linear models but creates too many features with high-cardinality categories.

## Missing Value Strategy

I fill missing numeric values with the column mean because:
- It's fast and doesn't require complex logic
- Preserves the overall distribution center
- Works okay when data is missing randomly

**Downside**: This reduces variance and might hide important patterns. If someone's income is missing, maybe that's meaningful information I'm throwing away.

**Better approaches for later**:
- Median for skewed distributions
- KNN imputation using similar records
- Separate "missing" indicator columns

## Feature Selection Approach

Currently, I use all available features except the target. My reasoning:
- Random Forest naturally handles irrelevant features
- Don't want to accidentally remove useful information
- Keeps the pipeline simple

**Problems with this**:
- Might include noisy features that hurt performance
- Computational cost grows with more features
- Some features might be highly correlated (redundant)

## Pipeline Order Matters

My preprocessing steps happen in this order:
1. Load data
2. Remove target column (prevents leakage)
3. Encode categorical features
4. Fill missing values
5. Split into train/test
6. Train model

**Why this order**: Target separation first prevents any chance of data leakage. Encoding before imputation ensures consistent data types. Splitting after preprocessing maintains data integrity.

## Known Issues I Haven't Fixed

**No feature scaling**: Linear Regression might perform better with standardized features, but I haven't implemented this yet.

**Basic imputation**: Mean filling is crude. More sophisticated methods could preserve relationships better.

**No outlier handling**: Extreme values might be skewing results, especially for Linear Regression.

**No correlation analysis**: Highly correlated features might be confusing the models.

These are on my todo list but weren't critical for getting the initial system working.