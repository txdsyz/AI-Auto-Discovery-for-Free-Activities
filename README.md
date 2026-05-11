# Youth Organization Discovery API - Backend

FastAPI backend for discovering and profiling youth organizations in Stockholm.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys
```

Required API keys:
- **Tavily API Key**: Get from [https://app.tavily.com](https://app.tavily.com)
- **OpenAI API Key**: Get from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Firebase Credentials**: Download from Firebase Console (see setup guide below)

### 3. Set Up Firebase

See the **Firebase Setup Guide** section below for detailed instructions.

### 4. Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## 📚 API Endpoints

### POST `/api/discover`
Run the discovery pipeline to find organizations.

**Request:**
```json
{
  "categories": ["sports", "youth_centers"],
  "max_organizations": 3
}
```

**Response:**
```json
{
  "run_id": "run_xyz123",
  "status": "completed",
  "organizations": [...],
  "total_organizations": 3,
  "total_events": 7,
  "execution_time_seconds": 45.2
}
```

### GET `/api/organizations`
Get all discovered organizations.

**Query Parameters:**
- `limit` (default: 10)
- `offset` (default: 0)

### GET `/api/organizations/{org_id}`
Get a specific organization with its events.

### GET `/api/discover/{run_id}`
Check the status of a discovery run.

## 🔥 Firebase Setup Guide

### Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"**
3. Project name: `afterclass-discovery` (or any name you prefer)
4. Disable Google Analytics (optional for this project)
5. Click **"Create project"**

### Step 2: Enable Firestore Database

1. In your Firebase project, click **"Firestore Database"** in the left menu
2. Click **"Create database"**
3. Choose **"Start in production mode"**
4. Select a location (choose closest to Stockholm, e.g., `europe-west1`)
5. Click **"Enable"**

### Step 3: Create Collections

Firestore will automatically create collections when you first write data, but you can pre-create them:

1. In Firestore, click **"Start collection"**
2. Create these collections:
   - `organizations`
   - `events`
   - `discovery_runs`

### Step 4: Generate Service Account Credentials

1. Click the **⚙️ gear icon** (Project settings) in the left sidebar
2. Go to the **"Service accounts"** tab
3. Click **"Generate new private key"**
4. Click **"Generate key"** in the popup
5. A JSON file will download (e.g., `afterclass-discovery-xxxxx.json`)
6. **Rename it to** `firebase-credentials.json`
7. **Move it to** your `backend/` directory
8. ⚠️ **NEVER commit this file to Git** (already in .gitignore)

### Step 5: Update .env File

Your `.env` should have:
```env
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

## 🧪 Testing

Run the discovery pipeline:

```bash
curl -X POST http://localhost:8000/api/discover \
  -H "Content-Type: application/json" \
  -d '{"categories": ["sports"], "max_organizations": 2}'
```

View results in Firebase Console:
1. Go to Firestore Database
2. Check the `organizations` collection
3. Check the `events` collection

## 📁 Project Structure

```
backend/
├── main.py                     # FastAPI app entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── firebase-credentials.json   # Firebase admin SDK (not in git)
│
├── app/
│   ├── config.py              # Configuration loader
│   ├── api/
│   │   ├── routes.py          # API endpoint handlers
│   │   └── models.py          # Pydantic models
│   ├── services/
│   │   ├── discovery.py       # Organization discovery
│   │   ├── profiling.py       # Organization profiling
│   │   └── pipeline.py        # Pipeline orchestration
│   ├── integrations/
│   │   ├── tavily.py          # Tavily API client
│   │   ├── openai.py          # OpenAI API client
│   │   └── firebase.py        # Firebase Firestore client
│   └── utils/
│       ├── prompts.py         # LLM prompt templates
│       └── validators.py      # Data validation
│
└── tests/
    ├── test_discovery.py
    └── test_profiling.py
```

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TAVILY_API_KEY` | Tavily API key for web search | Yes |
| `OPENAI_API_KEY` | OpenAI API key for LLM | Yes |
| `FIREBASE_CREDENTIALS_PATH` | Path to Firebase credentials file | Yes |
| `ENVIRONMENT` | Environment name (development/production) | No |

## 📊 Expected Results

- **3 organizations** discovered per run
- Each with **2-3 events**
- **Contact email** for each organization
- Age ranges: **7-19 years old**
- Execution time: **< 90 seconds**

## 🐛 Troubleshooting

### Firebase Authentication Error
- Check that `firebase-credentials.json` exists in the backend directory
- Verify the path in `.env` is correct
- Ensure the service account has Firestore permissions

### Tavily API Error
- Check your API key is correct
- Verify you haven't exceeded rate limits (100 requests/month free tier)
- Check internet connection

### OpenAI API Error
- Verify API key is valid
- Check you have available credits
- Ensure you're not hitting rate limits

## 📝 License

MIT
