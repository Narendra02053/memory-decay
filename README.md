# Memory Decay Predictor

A full-stack web application that predicts when you might forget learned material based on various factors like study time, confidence level, difficulty, mood, and more. The application uses machine learning to help optimize your study schedule through spaced repetition.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Testing](#testing)

## ✨ Features

- **Memory Decay Prediction**: ML-powered prediction of days until review needed
- **Interactive Chat**: AI-powered chat interface for study assistance
- **Notes Management**: Save and manage your study notes
- **Different Inputs, Different Outputs**: Each unique input combination produces distinct predictions

## 🔧 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

1. **Python 3.8 or higher**
   - Check version: `python --version` or `python3 --version`
   - Download: [Python Official Website](https://www.python.org/downloads/)

2. **Node.js 16 or higher and npm**
   - Check version: `node --version` and `npm --version`
   - Download: [Node.js Official Website](https://nodejs.org/)

3. **Git** (optional, for cloning the repository)
   - Download: [Git Official Website](https://git-scm.com/downloads)

### Optional Software

- **MongoDB** (optional, for data persistence)
   - The application works without MongoDB, but some features may be limited
   - Download: [MongoDB Official Website](https://www.mongodb.com/try/download/community)

## 📦 Installation

### Step 1: Clone or Download the Project

If you have the project files, navigate to the project directory:

```bash
cd Memory
```

### Step 2: Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd "backend (3)/backend"
   ```

2. **Create a virtual environment:**
   
   **Windows:**
   ```bash
   python -m venv venv
   ```
   
   **Linux/Mac:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   
   **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note:** This may take several minutes as it installs machine learning libraries (PyTorch, scikit-learn, etc.)

5. **Verify model files exist:**
   Ensure the following files are present in the `models/` directory:
   - `memory_model.pkl`
   - `scaler.pkl`
   - `label_encoders.pkl`

### Step 3: Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd "../../frontend (2)/frontend"
   ```
   
   Or from the project root:
   ```bash
   cd "frontend (2)/frontend"
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
   
   This will install React, Vite, and other frontend dependencies.

### Step 4: Environment Variables (Optional)

If you want to use MongoDB, create a `.env` file in the `backend (3)/backend/` directory:

```env
MONGO_URI=mongodb://127.0.0.1:27017
DB_NAME=memory_decay_db
```

**Note:** The application works without MongoDB. If MongoDB is not available, the app will continue to function but won't save data to the database.

## 🚀 Running the Application

You need to run both the backend and frontend servers. Open **two separate terminal windows**.

### Terminal 1: Backend Server

1. **Navigate to backend directory:**
   ```bash
   cd "backend (3)/backend"
   ```

2. **Activate virtual environment:**
   
   **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

3. **Start the backend server:**
   ```bash
   python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```
   
   You should see output like:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

### Terminal 2: Frontend Server

1. **Navigate to frontend directory:**
   ```bash
   cd "frontend (2)/frontend"
   ```

2. **Start the frontend development server:**
   ```bash
   npm run dev
   ```
   
   You should see output like:
   ```
   VITE v5.x.x  ready in xxx ms
   
   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose
   ```

### Access the Application

Once both servers are running:

- **Frontend (Main Application):** http://localhost:5173
- **Backend API:** http://127.0.0.1:8000
- **API Documentation (Swagger UI):** http://127.0.0.1:8000/docs
- **Alternative API Docs (ReDoc):** http://127.0.0.1:8000/redoc

## 📁 Project Structure

```
Memory/
├── backend (3)/
│   └── backend/
│       ├── app.py                 # FastAPI application entry point
│       ├── requirements.txt       # Python dependencies
│       ├── models/                # ML model files
│       │   ├── memory_model.pkl
│       │   ├── scaler.pkl
│       │   └── label_encoders.pkl
│       ├── routes/                # API route handlers
│       │   ├── prediction_routes.py
│       │   ├── chat_routes.py
│       │   └── notes_routes.py
│       ├── services/              # Business logic
│       │   ├── prediction_service.py
│       │   ├── preprocess.py
│       │   ├── chat_service.py
│       │   └── note_service.py
│       ├── db/                    # Database models and connection
│       │   ├── connection.py
│       │   ├── user_model.py
│       │   ├── notes_model.py
│       │   └── chat_model.py
│       └── venv/                  # Virtual environment (don't commit)
│
└── frontend (2)/
    └── frontend/
        ├── package.json           # Node.js dependencies
        ├── vite.config.jsx        # Vite configuration
        ├── src/
        │   ├── main.jsx           # React entry point
        │   ├── app.jsx            # Main app component
        │   ├── pages/            # Page components
        │   │   ├── Predict.jsx
        │   │   └── Chat.jsx
        │   ├── components/        # Reusable components
        │   │   └── Navbar.jsx
        │   └── services/          # API service functions
        │       ├── api.jsx
        │       └── chatApi.js
        └── dist/                  # Build output (generated)
```

## 📡 API Documentation

### Prediction Endpoint

**POST** `/api/predict/`

Predicts days until review needed based on input parameters.

**Request Body:**
```json
{
  "topic_name": "Neuroplasticity",
  "category": "science",
  "domain": "school",
  "category_type": "concept",
  "study_time": 1.5,
  "review_count": 2,
  "confidence": 4,
  "difficulty": "medium",
  "stress_level": 2,
  "sleep_hours": 7.5,
  "mood": "calm",
  "distraction_level": 1,
  "recent_event": "none",
  "attention_level": 4
}
```

**Response:**
```json
{
  "status": "success",
  "prediction": 5.23
}
```

### Chat Endpoint

**POST** `/api/chat/`

Send a message to the AI chat assistant.

**Request Body:**
```json
{
  "email": "user@example.com",
  "message": "How can I improve my memory retention?"
}
```

### Notes Endpoint

**GET** `/api/notes/{email}` - Get all notes for a user

**POST** `/api/notes/` - Create a new note

**PUT** `/api/notes/{note_id}` - Update a note

**DELETE** `/api/notes/{note_id}` - Delete a note

For detailed API documentation, visit: http://127.0.0.1:8000/docs

## 🧪 Testing

### Test Backend Connection

Run the test script:

```bash
cd "backend (3)/backend"
python test_backend.py
```

### Test Different Inputs Produce Different Outputs

```bash
cd "backend (3)/backend"
python test_all_features.py
```

This will test that different input combinations produce different prediction values.

## 🔍 Troubleshooting

### Backend Issues

**Problem: Module not found errors**
- **Solution:** Make sure you've activated the virtual environment and installed all requirements:
  ```bash
  pip install -r requirements.txt
  ```

**Problem: Model file not found**
- **Solution:** Ensure all `.pkl` files are present in the `models/` directory:
  - `memory_model.pkl`
  - `scaler.pkl`
  - `label_encoders.pkl`

**Problem: Port 8000 already in use**
- **Solution:** Either stop the process using port 8000, or change the port:
  ```bash
  python -m uvicorn app:app --host 127.0.0.1 --port 8001 --reload
  ```
  Then update the frontend API URL in `frontend (2)/frontend/src/services/api.jsx`

**Problem: MongoDB connection errors**
- **Solution:** MongoDB is optional. The app will work without it. If you see MongoDB errors, they're non-critical and can be ignored.

### Frontend Issues

**Problem: npm install fails**
- **Solution:** 
  - Clear npm cache: `npm cache clean --force`
  - Delete `node_modules` folder and `package-lock.json`
  - Run `npm install` again

**Problem: Frontend can't connect to backend**
- **Solution:** 
  - Ensure backend is running on http://127.0.0.1:8000
  - Check browser console for CORS errors
  - Verify the API URL in `src/services/api.jsx`

**Problem: Port 5173 already in use**
- **Solution:** Vite will automatically use the next available port, or specify a different port:
  ```bash
  npm run dev -- --port 3000
  ```

### General Issues

**Problem: Different inputs produce same output**
- **Solution:** This has been fixed in the latest version. Ensure you're using the updated `preprocess.py` file with improved encoding logic.

**Problem: Python version errors**
- **Solution:** Ensure you're using Python 3.8 or higher:
  ```bash
  python --version
  ```
  If needed, install a newer version from [python.org](https://www.python.org/downloads/)

**Problem: Permission errors (Linux/Mac)**
- **Solution:** You may need to use `sudo` for some operations, or fix permissions:
  ```bash
  sudo chmod -R 755 "backend (3)/backend"
  ```

## 🛠️ Development

### Building for Production

**Frontend:**
```bash
cd "frontend (2)/frontend"
npm run build
```

The built files will be in the `dist/` directory.

**Backend:**
The backend can be deployed using:
- **Uvicorn** (development): `uvicorn app:app --host 0.0.0.0 --port 8000`
- **Gunicorn** (production): `gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker`

## 📝 Notes

- The application uses machine learning models that must be present in the `models/` directory
- MongoDB is optional - the app works without it
- Different input combinations will produce different prediction values
- The backend API includes CORS middleware to allow frontend connections
- All API endpoints return JSON responses

## 📄 License

This project is for educational purposes.

## 🤝 Support

If you encounter any issues:
1. Check the Troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure both backend and frontend servers are running
4. Check the terminal output for error messages
5. Visit the API documentation at http://127.0.0.1:8000/docs

---

**Happy Learning! 🎓**

