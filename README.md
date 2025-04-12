# Happyfox assignment - Gmail Rule Engine

A standalone, production-grade Python script to:
- Authenticate with Gmail via OAuth
- Fetch and store emails in PostgreSQL
- Process rule-based conditions (from JSON)
- Apply actions like mark as read/unread or move to label

---

## Features

- Gmail API integration (OAuth 2.0)
- PostgreSQL backend via Docker
- Configurable rule engine via JSON
- Supports string and date predicates
- Modular and maintainable codebase

---

## Setup Instructions

### 1. Clone the Repo
```bash
git clone git@github.com:sanidhyarajawat/happyfox-gmail-rule-engine.git
cd happyfox-gmail-rule-engine
```

### 2. Set Up PostgreSQL with Docker
docker-compose up -d
DB is exposed on localhost:5432, default credentials:
	•	user: gmailuser
	•	password: gmailpass
	•	db: gmail_db

### 3. Install Python Dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 4. Setup Gmail OAuth

To authorize the script to access Gmail:

Step 1: Go to Google Cloud Console
    - Visit: https://console.cloud.google.com/

Step 2: Create a Project (if needed)
    - Click the project dropdown at the top and select "New Project"
    - Name it something like `Gmail Rule Engine` and click "Create"

Step 3: Enable Gmail API
    - With the project selected, go to: https://console.cloud.google.com/apis/library/gmail.googleapis.com
    - Click "Enable"

Step 4: Configure OAuth Consent Screen
    - Navigate to: APIs & Services → OAuth consent screen
    - Choose "External" user type (important)
    - Fill out app name, user support email, and developer contact info
    - Click through Scopes and Test Users — on Test Users screen, add your Gmail address
    - Save and continue

Step 5: Create OAuth Client Credentials
    - Go to: APIs & Services → Credentials
    - Click "Create Credentials" → "OAuth Client ID"
    - Choose "Desktop App" and name it `Gmail Script`
    - Click "Create", then download the `credentials.json`

Step 6: Place the credentials file
    - Save `credentials.json` to the root folder of this project

Step 7: Run the Script
    - Run: `python main.py`
    - A browser window will open prompting you to authorize access with your Gmail account
    - After successful login, a `token.pickle` file will be created to cache your session

### 5. Configure Rules

Edit rules/rules.json to define matching rules and actions.
Example file provided in folder

### 6. python main.py

Note
	•	Your access token is stored in token.pickle (auto-refreshes)
	•	You can delete this file to force re-authentication


### 🧪 Running Tests

Run all tests from the root folder:

```bash
pytest
