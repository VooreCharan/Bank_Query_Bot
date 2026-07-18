# 🏦 Banking Customer Service Chatbot

An intelligent, full-stack AI-powered banking assistant that provides real-time banking information, locates nearby branches/ATMs, supports multiple Indian languages, and offers voice interaction capabilities.

---------------------------------------------------------------------------------------------------------------------------------------------------

## ✨ Features

### Core Functionality
- **🤖 AI-Powered Chatbot:** Intelligent responses using Google Gemini 2.0-Flash via LangChain
- **🔍 Real-Time Banking Updates:** Web scraping for latest RBI policies, loan updates, and banking news
- **📍 Location Services:** Find nearby banks and ATMs using geolocation or manual address entry
- **🎤 Voice Input:** Speak your queries with Web Speech API integration
- **🌐 Multi-Language Support:** Supports 10+ Indian languages (Hindi, Telugu, Tamil, Bengali, etc.)
- **💬 Context-Aware Conversations:** RAG-based memory system with vector embeddings
- **🔐 Secure Authentication:** JWT-based user authentication with bcrypt password hashing
- **📊 Banking Analytics:** Track popular queries and user interactions

### Technical Features
- **Responsive Design:** Mobile-first UI with Framer Motion animations
- **Session Management:** Persistent chat history and conversation context
- **Error Handling:** Comprehensive error handling and user feedback
- **Rate Limiting:** API rate limiting to prevent abuse
- **CORS Support:** Secure cross-origin resource sharing

---------------------------------------------------------------------------------------------------------------------------------------------------

## 🛠 Tech Stack

### Frontend
- **Framework:** React 18.x
- **UI/Animation:** Framer Motion, React Icons
- **Routing:** React Router DOM 6.x
- **HTTP Client:** Axios
- **Notifications:** React Toastify
- **Markdown Rendering:** React Markdown
- **Voice Recognition:** React Speech Recognition

### Backend
- **Framework:** Flask 3.x (Python)
- **ORM:** SQLAlchemy with Flask-SQLAlchemy
- **Authentication:** Flask-JWT-Extended
- **Password Hashing:** bcrypt
- **HTTP Requests:** requests library

### AI & APIs
- **LLM:** Google Gemini API (gemini-2.0-flash)
- **Framework:** LangChain, LangChain-Google-GenAI
- **Web Search:** Serper API
- **Translation:** Deep-Translator
- **Location:** OpenStreetMap Nominatim API, Overpass API

### Database
- **Primary:** SQLite (development) / PostgreSQL (production)
- **Vector Database:** Supabase with pgvector extension
- **Session Storage:** Server-side session management

---------------------------------------------------------------------------------------------------------------------------------------------------

## 📁 Project Structure

banking-chatbot/
│
├── backend/
│ ├── database/
│ │ └── db_setup.py # Vector DB setup
│ ├── models/
│ │ ├── init.py
│ │ ├── user.py # User, ChatSession models
│ │ └── chat.py # ChatHistory, FAQ, UserPreferences
│ ├── routes/
│ │ ├── init.py
│ │ ├── auth.py # Authentication endpoints
│ │ ├── chat.py # Chat endpoints
│ │ ├── updates.py # Banking updates endpoints
│ │ └── location.py # Location search endpoints
│ ├── services/
│ │ ├── init.py
│ │ ├── ai_agent.py # Main AI agent logic
│ │ ├── memory_service.py # Vector memory management
│ │ ├── search_service.py # Web search integration
│ │ ├── translation_service.py # Multi-language support
│ │ ├── banking_data_service.py # Banking data scraping
│ │ └── location_service.py # Location/maps integration
│ ├── utils/
│ │ ├── init.py
│ │ ├── decorators.py # Custom decorators
│ │ └── helpers.py # Helper functions
│ ├── app.py # Flask application entry
│ ├── config.py # Configuration management
│ ├── requirements.txt # Python dependencies
│ └── .env # Environment variables
│
├── frontend/
│ ├── public/
│ │ ├── index.html
│ │ └── favicon.ico
│ ├── src/
│ │ ├── components/
│ │ │ ├── Auth/
│ │ │ │ ├── Login.jsx
│ │ │ │ └── Register.jsx
│ │ │ ├── Chat/
│ │ │ │ ├── ChatInterface.jsx
│ │ │ │ ├── ChatMessage.jsx
│ │ │ │ ├── VoiceInput.jsx
│ │ │ │ ├── BankSelector.jsx
│ │ │ │ └── LocationSearch.jsx
│ │ │ ├── Updates/
│ │ │ │ ├── LatestUpdates.jsx
│ │ │ │ └── UpdateCard.jsx
│ │ │ └── Layout/
│ │ │ ├── Navbar.jsx
│ │ │ └── Sidebar.jsx
│ │ ├── context/
│ │ │ └── AuthContext.js # Authentication context
│ │ ├── services/
│ │ │ ├── api.js # API service layer
│ │ │ └── auth.js # Auth service
│ │ ├── styles/
│ │ │ ├── index.css # Global styles
│ │ │ ├── Auth.css
│ │ │ ├── Chat.css
│ │ │ ├── Updates.css
│ │ │ ├── Sidebar.css
│ │ │ └── LocationSearch.css
│ │ ├── utils/
│ │ │ └── constants.js # Constants/config
│ │ ├── App.js # Main App component
│ │ └── index.js # Entry point
│ ├── package.json
│ ├── .env # Environment variables
│ └── .gitignore
│
├── .gitignore
└── README.md


---------------------------------------------------------------------------------------------------------------------------------------------------

## 📋 Prerequisites

### Required Software
- **Python:** 3.11 or higher
- **Node.js:** 16.x or higher
- **npm:** 8.x or higher
- **Git:** Latest version

### Required API Keys (Free Tier Available)
1. **Google Gemini API Key** - [Get it here](https://aistudio.google.com/app/apikey)
2. **Serper API Key** - [Get it here](https://serper.dev) (2,500 free searches)
3. **Supabase Account** - [Sign up here](https://supabase.com)

---

## 🚀 Installation

### 1. Clone the Repository

git clone https://github.com/yourusername/banking-chatbot.git
cd banking-chatbot


### 2. Backend Setup

#### a. Create Virtual Environment

cd backend
python -m venv venv
source venv/bin/activate # Or 'venv\Scripts\activate' on Windows


#### b. Install Dependencies

pip install -r requirements.txt


#### c. Configure Environment

Create a `.env` file in `backend/`:

SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///banking_chatbot.db
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
GOOGLE_API_KEY=your-google-gemini-api-key
SERPER_API_KEY=your-serper-api-key



#### d. Run Backend

python app.py

Runs on http://localhost:5000



### 3. Frontend Setup

#### a. Install Dependencies

cd ../frontend
npm install


#### b. Set API URL

Create a `.env` in `frontend/`:

REACT_APP_API_URL=http://localhost:5000/api


#### c. Start React App

npm start

Opens http://localhost:3000


---

## Key Functionalities

- Chat securely with AI on banking topics
- Get updates on banking policies and news (live web scraping)
- Search for branches/ATMs near you by typing or using your current location
- Interact in multiple Indian languages or English
- Voice recognition for sending queries
- JWT-secured user authentication and registration

---

## Environment Variables

| Key                    | Usage                                   |
|------------------------|------------------------------------------|
| SECRET_KEY             | Flask app sessions/security              |
| JWT_SECRET_KEY         | For secure JWT auth                      |
| DATABASE_URL           | Postgres/SQLite DB connection            |
| SUPABASE_URL           | Supabase project API endpoint            |
| SUPABASE_KEY           | Public anon key for Supabase vector DB   |
| GOOGLE_API_KEY         | Google Gemini AI API key                 |
| SERPER_API_KEY         | (Optional) Serper Web Search API Key     |

---

## API Endpoints

- `POST /api/auth/register` — User registration
- `POST /api/auth/login` — User login, returns JWT
- `POST /api/chat` — Send chat message, get AI response
- `POST /api/chat/new-session` — Start a new chat
- `POST /api/location/search` — Find banks or ATMs near a location
- `GET /api/updates` — Fetch latest banking updates/news


---

## License

MIT

---

## Credits

- [LangChain](https://langchain.com/)
- [Google Gemini API](https://ai.google.dev/)
- [Supabase](https://supabase.com/)
- [OpenStreetMap](https://www.openstreetmap.org/)
- [Serper](https://serper.dev/)
- [React](https://react.dev/)
- [Flask](https://flask.palletsprojects.com/)

---

## Author

Charan Voore

---