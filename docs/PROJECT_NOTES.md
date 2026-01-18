# Development Notes

## Why I Built This

I wanted to understand how production ML systems work end-to-end. Most tutorials focus on model training in notebooks, but real systems need data pipelines, APIs, user interfaces, and model management.

## Technical Challenges I Solved

**Automatic Algorithm Selection**: Instead of making users choose algorithms, the system detects whether the target is numeric or categorical and picks an appropriate model. This required understanding when each algorithm works well.

**Data Leakage Prevention**: Early versions had subtle bugs where test data influenced preprocessing. I learned to separate the target column first and apply all transformations consistently.

**JSON Serialization**: NumPy and Pandas types don't serialize to JSON by default. Had to convert all int64/float64 values to native Python types for the API responses.

**Chart Generation**: Matplotlib in a web context requires careful memory management and the right backend. Took some trial and error to get clean, professional-looking charts.

## What I Learned

**Start Simple**: My first attempt used XGBoost and complex feature engineering. The simple Linear Regression + Random Forest approach actually works better for most cases and is much easier to debug.

**Documentation Matters**: Writing down my reasoning for model choices helped me catch assumptions I hadn't thought through. It also makes the project much easier to explain to others.

**Real Data is Messy**: The system handles missing values, mixed data types, and edge cases that don't appear in clean tutorial datasets.

## Future Improvements

If I were to extend this system:
1. Cross-validation for more robust performance estimates
2. Hyperparameter tuning with reasonable defaults
3. More sophisticated feature engineering
4. Model monitoring and drift detection
5. Support for time series data

But the current version demonstrates the core concepts well and actually works reliably.