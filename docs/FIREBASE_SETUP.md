# Firebase Setup Guide for AfterClass Discovery

This guide walks you through setting up Firebase for the Youth Organization Discovery project.

## Step-by-Step Firebase Setup

### 1. Create a Firebase Project

1. **Go to Firebase Console**
   - Visit: [https://console.firebase.google.com/](https://console.firebase.google.com/)
   - Sign in with your Google account

2. **Create New Project**
   - Click **"Add project"** or **"Create a project"**
   - Project name: `afterclass-discovery` (or choose your own name)
   - Click **Continue**

3. **Google Analytics (Optional)**
   - You can **disable** Google Analytics for this project (not needed for our use case)
   - Or enable it if you want analytics tracking
   - Click **Create project**

4. **Wait for Setup**
   - Firebase will set up your project (takes ~30 seconds)
   - Click **Continue** when done

---

### 2. Enable Firestore Database

1. **Navigate to Firestore**
   - In the left sidebar, find **"Build"** section
   - Click **"Firestore Database"**

2. **Create Database**
   - Click **"Create database"** button

3. **Select Security Rules**
   - Choose **"Start in production mode"**
   - (We'll use server-side SDK with admin privileges, so we don't need public access)
   - Click **Next**

4. **Choose Location**
   - Select a location close to Stockholm
   - Recommended: `europe-west1` (Belgium) or `europe-west3` (Frankfurt)
   - ⚠️ **Important:** You cannot change this later!
   - Click **Enable**

5. **Wait for Database Creation**
   - Firestore will be provisioned (takes ~1 minute)

---

### 3. Create Firestore Collections

Firestore will automatically create collections when you first write data, but you can pre-create them for clarity:

#### Option A: Create Manually (Recommended for Learning)

1. In Firestore console, click **"Start collection"**

2. **Create `organizations` collection:**
   - Collection ID: `organizations`
   - Click **Next**
   - Add a sample document:
     - Document ID: `sample-org` (Auto-ID is fine too)
     - Fields:
       ```
       name (string): "Sample Organization"
       type (string): "Sports Club"
       website (string): "https://example.se"
       created_at (timestamp): (use "Add field" → timestamp → now)
       ```
   - Click **Save**

3. **Create `events` collection:**
   - Click **"Start collection"**
   - Collection ID: `events`
   - Add a sample document with fields:
     ```
     organization_id (string): "sample-org"
     name (string): "Sample Event"
     type (string): "recurring"
     age_range (string): "8-14"
     created_at (timestamp): now
     ```
   - Click **Save**

4. **Create `discovery_runs` collection:**
   - Click **"Start collection"**
   - Collection ID: `discovery_runs`
   - Add a sample document with fields:
     ```
     status (string): "test"
     started_at (timestamp): now
     ```
   - Click **Save**

#### Option B: Let the Code Create Collections Automatically

Just run the backend - it will create collections on first write.

---

### 4. Generate Service Account Credentials

This is the **most important step** for connecting your backend to Firebase.

1. **Go to Project Settings**
   - Click the **⚙️ gear icon** next to "Project Overview" in the top left
   - Select **"Project settings"**

2. **Navigate to Service Accounts**
   - Click the **"Service accounts"** tab at the top

3. **Generate Private Key**
   - You should see a section titled "Firebase Admin SDK"
   - Click the button **"Generate new private key"**

4. **Confirm Download**
   - A popup will appear warning you to keep this file secure
   - Click **"Generate key"**
   - A JSON file will download automatically (e.g., `afterclass-discovery-xxxxx-firebase-adminsdk-xxxxx.json`)

5. **⚠️ IMPORTANT: Secure This File**
   - This file contains secret credentials
   - **NEVER commit it to Git**
   - **NEVER share it publicly**
   - If compromised, regenerate a new key immediately

6. **Rename and Move the File**
   ```bash
   # Rename the downloaded file
   mv ~/Downloads/afterclass-discovery-xxxxx-firebase-adminsdk-xxxxx.json firebase-credentials.json
   
   # Move it to your backend directory
   mv firebase-credentials.json /path/to/afterclass/backend/
   ```

---

### 5. Configure Environment Variables

1. **Copy the example env file:**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   # Use your favorite editor
   nano .env
   # or
   code .env
   ```

3. **Add your API keys:**
   ```env
   # Tavily API Key (get from https://app.tavily.com)
   TAVILY_API_KEY=tvly-your_actual_key_here
   
   # OpenAI API Key (get from https://platform.openai.com/api-keys)
   OPENAI_API_KEY=sk-your_actual_key_here
   
   # Firebase credentials file path
   FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
   
   # Environment
   ENVIRONMENT=development
   ```

4. **Verify file location:**
   ```bash
   ls -la backend/
   # You should see:
   # - .env (your secrets)
   # - .env.example (the template)
   # - firebase-credentials.json (Firebase credentials)
   ```

---

### 6. Test Firebase Connection

1. **Install dependencies:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Check health endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```

   Expected response:
   ```json
   {
     "status": "healthy",
     "environment": "development",
     "services": {
       "tavily": "configured",
       "openai": "configured",
       "firebase": "configured"
     }
   }
   ```

4. **Check Firebase initialization:**
   - Look at the terminal output
   - You should see: `✓ Firebase initialized successfully`
   - If you see an error, check the troubleshooting section below

---

## Firestore Data Structure

Your Firestore will have these collections:

### `organizations` Collection
```
organizations/
  {org_id}/
    name: "Rinkeby IF"
    type: "Sports Club"
    website: "https://rinkebyif.se"
    contact:
      email: "info@rinkebyif.se"
      phone: "+46 8 XXX XXXX"
    location: "Rinkeby, Stockholm"
    description: "Sports club for youth..."
    created_at: timestamp
    last_updated: timestamp
```

### `events` Collection
```
events/
  {event_id}/
    organization_id: "org_doc_id"
    name: "Football Training"
    type: "recurring"
    schedule: "Mondays & Wednesdays 17:00-19:00"
    date: null
    age_range: "8-14"
    description: "Weekly training..."
    created_at: timestamp
```

### `discovery_runs` Collection
```
discovery_runs/
  {run_id}/
    search_queries: ["idrottsföreningar Stockholm ungdom", ...]
    organizations_found: 3
    total_events_extracted: 7
    status: "completed"
    started_at: timestamp
    completed_at: timestamp
    error: null
```

---

## Getting API Keys

### Tavily API Key

1. Go to [https://app.tavily.com](https://app.tavily.com)
2. Sign up for a free account
3. Go to API Keys section
4. Copy your API key (starts with `tvly-`)
5. Free tier: 100 requests/month

### OpenAI API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **"Create new secret key"**
4. Name it: "AfterClass Discovery"
5. Copy the key (starts with `sk-`)
6. ⚠️ **You can only see it once!**
7. You'll need credits in your account (add a payment method)

---

## Troubleshooting

### Error: "Firebase credentials file not found"

**Solution:**
```bash
# Check if file exists
ls -la backend/firebase-credentials.json

# If not, make sure you downloaded it from Firebase Console
# and placed it in the backend directory
```

### Error: "Permission denied" when reading credentials

**Solution:**
```bash
# Make sure the file has read permissions
chmod 600 backend/firebase-credentials.json
```

### Error: "Invalid credentials" or "Authentication failed"

**Possible causes:**
1. Wrong credentials file
2. Firebase project deleted or changed
3. Service account key revoked

**Solution:**
- Regenerate a new service account key from Firebase Console
- Replace the old `firebase-credentials.json` file

### Error: "Collection not found" or "Permission denied" in Firestore

**Solution:**
- Make sure Firestore is enabled in your Firebase project
- Check that you're using the correct project (check project ID in credentials file)

### Firestore Rules Error

If you get permission errors:

1. Go to Firestore → Rules
2. Make sure rules allow server-side access:
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /{document=**} {
         allow read, write: if false;  // Public access disabled (we use Admin SDK)
       }
     }
   }
   ```

### Can't connect to Firestore

**Check:**
1. Internet connection
2. Firestore is enabled in Firebase Console
3. Service account has Firestore permissions (should be automatic)

---

## Security Best Practices

### ✅ DO:
- Keep `firebase-credentials.json` in `.gitignore`
- Keep `.env` in `.gitignore`
- Use environment variables for all secrets
- Regenerate keys if compromised
- Use different Firebase projects for dev/staging/prod

### ❌ DON'T:
- Commit credentials to Git
- Share credentials in messages/emails
- Use production credentials in development
- Store credentials in cloud storage
- Hardcode credentials in code

---

## Next Steps

Once Firebase is set up:

1. ✅ Verify all services are "configured" in `/health` endpoint
2. ✅ Test creating a document manually in Firestore Console
3. ✅ Move on to implementing the API integrations (Phase 2 of TODO)
4. ✅ Test the complete pipeline

---

## Quick Reference

### Firebase Console URLs
- Main Console: https://console.firebase.google.com/
- Your Project: https://console.firebase.google.com/project/YOUR-PROJECT-ID
- Firestore: https://console.firebase.google.com/project/YOUR-PROJECT-ID/firestore

### Environment Variables
```env
TAVILY_API_KEY=tvly-...
OPENAI_API_KEY=sk-...
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

### Test Commands
```bash
# Check health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs

# Check Firestore in console
# Go to Firebase Console → Firestore Database
```

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Firebase documentation: https://firebase.google.com/docs
3. Check backend logs for specific error messages
4. Verify all credentials are correctly set in `.env`

---

**You're ready to build!** 🚀

Once Firebase is set up, proceed to Phase 2 in the TODO.md to implement the API integrations.
