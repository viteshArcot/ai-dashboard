# DataLab - My Data Science Learning Project

A data science platform I built while learning how production ML systems actually work. Started as a simple CSV analyzer, evolved into something that can train models and generate insights.

## What It Actually Does

- Upload CSV files and get statistical analysis
- Generates charts automatically (took forever to get matplotlib working in a web context)
- Trains basic ML models - Linear Regression or Random Forest depending on the data
- Uses OpenRouter API to generate plain English summaries
- Keeps track of all the models I've trained

## How I Approached the ML Parts

I kept the ML simple on purpose after trying more complex approaches first:

**Model Selection**: The system picks Linear Regression for continuous targets, Random Forest for categorical ones. I initially tried XGBoost and other fancy algorithms, but honestly the simple ones work just as well for most cases and are way easier to debug.

**Data Handling**: 80/20 train/test split because that's what everyone uses and it works. I'm careful about data leakage - learned that lesson the hard way when my first models had suspiciously perfect scores.

**Evaluation**: R² for regression, accuracy for classification. Not the most sophisticated metrics, but they're easy to explain. I've noticed R² above 0.7 usually means the model found something useful.

**What's Missing**: No cross-validation (should add this), no hyperparameter tuning (using defaults), pretty basic preprocessing. These are conscious shortcuts - wanted to get something working first.

## Where It Works Well (and Where It Doesn't)

After testing with various datasets, I've learned where this approach shines and where it falls flat:

**Works well with**: Clean tabular data, balanced classes, problems where you can actually see patterns in the data.

**Struggles with**: Messy real-world data, highly imbalanced classes, non-linear relationships that Linear Regression can't capture, really high-dimensional stuff.

**My evaluation approach**: I don't just trust the metrics. R² below 0.5 usually means the model isn't finding real patterns. Accuracy above 0.95 makes me suspicious - often means overfitting or I messed up the data split somehow.

**Known issues I haven't fixed**: Only using one train/test split instead of cross-validation, pretty basic preprocessing that could be smarter, no hyperparameter tuning beyond reasonable defaults.

## What I'd Work On Next

If I had more time (and wasn't moving on to other learning projects):

1. Cross-validation - would give much better performance estimates
2. Better handling of categorical features - one-hot encoding for linear models
3. Class balancing for those annoying imbalanced datasets
4. Some kind of feature selection to remove noise
5. Basic hyperparameter tuning, nothing fancy
6. Maybe some monitoring to catch when models start performing poorly

But honestly, the current version does what I need it to do and taught me the fundamentals.

## Setup Instructions

### 1. Install Dependencies

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

### 2. Environment Configuration

```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

### 3. Run Full Application

```bash
# Start both frontend and backend
./start_full_app.sh

# OR start individually:
# Backend: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# Frontend: cd frontend && npm start
```

### 4. Access Application

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Upload Dataset
```
POST /api/v1/upload
Content-Type: multipart/form-data
Body: file (CSV)
```

### Analyze Dataset
```
GET /api/v1/analyze/{dataset_id}
Response: {"stats": {}, "charts": [], "summary": ""}
```

### Analysis History
```
GET /api/v1/history
Response: {"history": [...]}
```

### System Metrics
```
GET /api/v1/metrics
Response: {"total_datasets": 0, "avg_processing_time": 0}
```

## Technical Stuff

- **Backend**: FastAPI because it's fast and the auto-docs are nice
- **Frontend**: React with a dark theme (took way too long to get the styling right)
- **ML**: Scikit-learn for the models, Pandas for data wrangling
- **Charts**: Matplotlib with custom styling - getting this to work in a web context was painful
- **Database**: SQLite because simple is better
- **AI Integration**: OpenRouter API for the natural language summaries

## Project Structure

Pretty standard layout:

```
ai-dashboard/
├── app/                 # Backend stuff
│   ├── main.py          # FastAPI setup
│   ├── routes.py        # API endpoints
│   ├── analysis.py      # Statistical analysis
│   ├── ml.py           # Model training logic
│   ├── visualization.py # Chart generation
│   └── database.py     # Data models
├── frontend/           # React app
├── docs/               # My notes and documentation
├── static/             # Generated charts and datasets
└── models/             # Saved models
```


<img width="1362" height="688" alt="ai 1" src="https://github.com/user-attachments/assets/3980ae65-9e7c-4f23-9625-44050cb1ef4a" />

<img width="1363" height="681" alt="ai 2" src="https://github.com/user-attachments/assets/baaa3099-681a-49c8-8add-71968f9a4477" />

<img width="1364" height="690" alt="ai3" src="https://github.com/user-attachments/assets/1d0fea63-902a-4e45-84cc-bf9c09208781" />


