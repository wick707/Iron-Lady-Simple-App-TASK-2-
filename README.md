# Iron-Lady-Simple-App-TASK-2-

A Django-based course management application with an integrated AI-powered chatbot for course recommendations and FAQs. This system allows administrators to manage leadership programs while providing users with intelligent course guidance through a RAG (Retrieval Augmented Generation) chatbot.

## 🚀 Features

### **Course Management (CRUD)**
- **Create** new courses with detailed information
- **Read** and browse all available courses on the dashboard
- **Update** existing course details
- **Delete** courses with confirmation prompts
- User authentication and authorization
- Responsive dashboard with course statistics

### **AI-Powered Chatbot** 
- **FAQ Mode**: Answers specific questions about programs, duration, fees, certificates
- **Recommendation Mode**: Suggests courses based on user interests and career goals
- **Vector Search**: Uses FAISS for semantic search through course content
- **Auto-updating Knowledge Base**: Automatically updates when courses are modified
- **Multi-turn Conversations**: Maintains chat history for context

### **Dashboard Analytics**
- Total course count
- Online vs Hybrid program statistics
- Course overview with truncated descriptions
- Quick access to add/edit/delete operations

## 🛠️ Technology Stack

**Backend:**
- **Django 4.x** - Main web framework
- **FastAPI** - Chatbot API server
- **SQLite** - Database (default Django setup)

**AI/ML Components:**
- **FAISS** - Vector similarity search
- **Sentence Transformers** - Text embeddings
- **Groq API** - Large Language Model integration
- **Llama 3.1 8B** - Language model for responses

**Frontend:**
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript** - Interactive chatbot interface

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation

### 1. Clone and Setup Environment

```bash
git clone <your-repository-url>
cd iron-lady-course-management
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory:

```env
# Groq API key (required for chatbot)
GROQ_API_KEY=your_groq_api_key_here

# Knowledge base settings
KB_FILE=knowledgebase.md
TOP_K=8

# Optional: Model configurations
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
GEN_MODEL=llama-3.1-8b-instant
```

**⚠️ Important:** Never commit your actual API keys to version control. Use the `.env.example` template.

### 4. Django Setup

```bash
# Run database migrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Collect static files (if needed)
python manage.py collectstatic
```

## 🚀 Running the Application

### Start Django Development Server

```bash
python manage.py runserver
```
The course management interface will be available at `http://127.0.0.1:8000`

### Start FastAPI Chatbot Server

```bash
python app.py
```
The chatbot interface will be available at `http://127.0.0.1:8000/chatbot`

## 📖 Usage Guide

### **Course Management**

1. **Login/Signup**: Access the authentication system at `/accounts/login/`
2. **Dashboard**: View all courses with statistics at `/`
3. **Add Course**: Click "Add New Program" to create courses
4. **Edit Course**: Click edit buttons on course cards
5. **Delete Course**: Use delete buttons with confirmation prompts

### **AI Chatbot**

1. **Access**: Navigate to `/chatbot` for the chat interface
2. **FAQ Mode**: Ask direct questions about programs
   - "What programs do you offer?"
   - "What is the duration of courses?"
   - "Are certificates provided?"

3. **Recommendation Mode**: Get personalized course suggestions
   - Describe your background and goals
   - Receive tailored program recommendations

## 🏗️ Project Structure

```
iron-lady-course-management/
├── accounts/                    # User authentication app
│   ├── templates/accounts/      # Login/signup templates
│   ├── views.py                # Authentication views
│   └── urls.py                 # Auth URL patterns
├── courses/                     # Course management app
│   ├── templates/courses/       # Course templates
│   ├── models.py               # Course model
│   ├── views.py                # CRUD views
│   ├── forms.py                # Course forms
│   └── urls.py                 # Course URL patterns
├── iron_lady_project/          # Django project settings
├── app.py                      # FastAPI chatbot server
├── chatbot.html               # Chatbot interface
├── knowledgebase.md           # Auto-generated course data
├── requirements.txt           # Python dependencies
├── manage.py                  # Django management script
└── .env                       # Environment variables
```

## 🎯 Core Models

### Course Model
```python
class Course(models.Model):
    name = models.CharField(max_length=200)
    overview = models.TextField()
    target_audience = models.TextField()
    duration = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)
    fee = models.CharField(max_length=100)
    certificate_provided = models.BooleanField(default=False)
    interests_aligned = models.TextField()
```

## 🤖 Chatbot Architecture

The chatbot uses a **RAG (Retrieval Augmented Generation)** approach:

1. **Vector Embeddings**: Course content is embedded using Sentence Transformers
2. **FAISS Index**: Enables fast semantic search across course content
3. **Context Retrieval**: Finds relevant course information based on user queries
4. **LLM Generation**: Groq API generates contextual responses
5. **Auto-sync**: Knowledge base updates automatically when courses change

## 🔐 Security Features

- **User Authentication**: Login required for course management
- **CSRF Protection**: Django's built-in CSRF middleware
- **Environment Variables**: Sensitive data stored in `.env` files
- **Input Validation**: Form validation for course creation/editing

## 🚀 Deployment Considerations

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=your-production-database-url
GROQ_API_KEY=your-production-groq-key
```

### Static Files
```bash
python manage.py collectstatic
```

## 🧪 API Endpoints

### FastAPI Chatbot Endpoints
- `GET /` - Serves main interface
- `GET /chatbot` - Chatbot interface
- `POST /chat` - Chat API endpoint

### Django URLs
- `/accounts/login/` - User login
- `/accounts/signup/` - User registration
- `/` - Course dashboard
- `/add/` - Add new course
- `/<id>/edit/` - Edit course
- `/<id>/delete/` - Delete course

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

***

**Built with ❤️ for Iron Lady Leadership Programs**
