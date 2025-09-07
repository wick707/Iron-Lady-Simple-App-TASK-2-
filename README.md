# Iron-Lady-Simple-App-TASK-2-
Iron Lady Course Management System
A Django-based course management application with an integrated AI-powered chatbot for course recommendations and FAQs. This system allows administrators to manage leadership programs while providing users with intelligent course guidance through a RAG (Retrieval Augmented Generation) chatbot.

🚀 Features
Course Management (CRUD)
Create new courses with detailed information

Read and browse all available courses on the dashboard

Update existing course details

Delete courses with confirmation prompts

User authentication and authorization

Responsive dashboard with course statistics

AI-Powered Chatbot
FAQ Mode: Answers specific questions about programs, duration, fees, certificates

Recommendation Mode: Suggests courses based on user interests and career goals

Vector Search: Uses FAISS for semantic search through course content

Auto-updating Knowledge Base: Automatically updates when courses are modified

Multi-turn Conversations: Maintains chat history for context

Dashboard Analytics
Total course count

Online vs Hybrid program statistics

Course overview with truncated descriptions

Quick access to add/edit/delete operations

🛠️ Technology Stack
Backend:

Django 4.x - Main web framework

FastAPI - Chatbot API server

SQLite - Database (default Django setup)

AI/ML Components:

FAISS - Vector similarity search

Sentence Transformers - Text embeddings

Groq API - Large Language Model integration

Llama 3.1 8B - Language model for responses

Frontend:

HTML5 - Structure

CSS3 - Styling

JavaScript - Interactive chatbot interface

📋 Prerequisites
Python 3.8+

pip (Python package manager)

Virtual environment (recommended)

🔧 Installation
1. Clone and Setup Environment
bash
git clone <your-repository-url>
cd iron-lady-course-management
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
2. Install Dependencies
bash
pip install -r requirements.txt
3. Environment Variables
Create a .env file in the root directory:

text
# Groq API key (required for chatbot)
GROQ_API_KEY=your_groq_api_key_here

# Knowledge base settings
KB_FILE=knowledgebase.md
TOP_K=8

# Optional: Model configurations
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
GEN_MODEL=llama-3.1-8b-instant
⚠️ Important: Never commit your actual API keys to version control. Use the .env.example template.

4. Django Setup
bash
# Run database migrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Collect static files (if needed)
python manage.py collectstatic
🚀 Running the Application
Start Django Development Server
bash
python manage.py runserver
The course management interface will be available at http://127.0.0.1:8000

Start FastAPI Chatbot Server
bash
python app.py
The chatbot interface will be available at http://127.0.0.1:8000/chatbot

📖 Usage Guide
Course Management
Login/Signup: Access the authentication system at /accounts/login/

Dashboard: View all courses with statistics at /

Add Course: Click "Add New Program" to create courses

Edit Course: Click edit buttons on course cards

Delete Course: Use delete buttons with confirmation prompts

AI Chatbot
Access: Navigate to /chatbot for the chat interface

FAQ Mode: Ask direct questions about programs

"What programs do you offer?"

"What is the duration of courses?"

"Are certificates provided?"

Recommendation Mode: Get personalized course suggestions

Describe your background and goals

Receive tailored program recommendations

🎯 Core Models
Course Model
python
class Course(models.Model):
    name = models.CharField(max_length=200)
    overview = models.TextField()
    target_audience = models.TextField()
    duration = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)
    fee = models.CharField(max_length=100)
    certificate_provided = models.BooleanField(default=False)
    interests_aligned = models.TextField()
🤖 Chatbot Architecture
The chatbot uses a RAG (Retrieval Augmented Generation) approach:

Vector Embeddings: Course content is embedded using Sentence Transformers

FAISS Index: Enables fast semantic search across course content

Context Retrieval: Finds relevant course information based on user queries

LLM Generation: Groq API generates contextual responses

Auto-sync: Knowledge base updates automatically when courses change

🔐 Security Features
User Authentication: Login required for course management

CSRF Protection: Django's built-in CSRF middleware

Environment Variables: Sensitive data stored in .env files

Input Validation: Form validation for course creation/editing

🚀 Deployment Considerations
Environment Variables for Production
text
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=your-production-database-url
GROQ_API_KEY=your-production-groq-key
Static Files
bash
python manage.py collectstatic
🧪 API Endpoints
FastAPI Chatbot Endpoints
GET / - Serves main interface

GET /chatbot - Chatbot interface

POST /chat - Chat API endpoint

Django URLs
/accounts/login/ - User login

/accounts/signup/ - User registration

/ - Course dashboard

/add/ - Add new course

/<id>/edit/ - Edit course

/<id>/delete/ - Delete course

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

Built with ❤️ for Iron Lady Leadership Programs
