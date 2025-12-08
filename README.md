# Hybrid-Analyzer

🔬 **AI-Powered Text Analysis Platform**

Hybrid-Analyzer is an industrial-grade fullstack application that orchestrates Hugging Face Zero-Shot Classification and Google Gemini API to provide automated article analysis with categorization, summarization, and tone detection.

## Features

- 🤖 **Dual AI Integration**: Combines Hugging Face BART for classification with Gemini for intelligent summarization
- 🔐 **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- 📊 **Comprehensive Analysis**: Category prediction, confidence scoring, summary generation, and tone detection
- 🗄️ **PostgreSQL Database**: Persistent storage for users and analysis history
- 🐳 **Docker Ready**: One-command deployment with Docker Compose
- ✅ **Fully Tested**: Comprehensive unit and integration tests with mocked services
- 🎨 **Modern UI**: Responsive React frontend with dark theme

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │─────▶│   FastAPI    │─────▶│  PostgreSQL │
│  Frontend   │      │   Backend    │      │  Database   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ├─────▶ Hugging Face API
                            │       (Classification)
                            │
                            └─────▶ Gemini API
                                    (Summarization)
```

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed
- Hugging Face API token ([Get one here](https://huggingface.co/settings/tokens))
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Hybrid-Analyzer
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   HUGGINGFACE_API_TOKEN=your_token_here
   GEMINI_API_KEY=your_key_here
   JWT_SECRET=your_random_secret_min_32_chars
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Setup (Without Docker)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb hybrid_analyzer
   
   # Run schema
   psql hybrid_analyzer < ../database/schema.sql
   ```

5. **Configure environment**
   ```bash
   cp ../.env.example .env
   # Edit .env with your configuration
   ```

6. **Run the backend**
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   echo "VITE_API_URL=http://localhost:8000" > .env
   ```

4. **Run the frontend**
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and receive JWT token

### Analysis (Protected)

- `POST /analyze` - Analyze text (requires JWT token)

### Health

- `GET /health` - Health check endpoint
- `GET /` - API information

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=. --cov-report=html
```

### Test Coverage

- Authentication (register, login, JWT validation)
- Hugging Face service (with mocks)
- Gemini service (with mocks)
- Analysis orchestration
- Error handling

## Project Structure

```
Hybrid-Analyzer/
├── backend/
│   ├── auth/                 # Authentication module
│   │   ├── models.py         # User model
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── routes.py         # Auth endpoints
│   │   ├── utils.py          # Password & JWT utils
│   │   └── middleware.py     # JWT middleware
│   ├── analysis/             # Analysis module
│   │   ├── services/
│   │   │   ├── huggingface.py
│   │   │   └── gemini.py
│   │   ├── orchestrator.py   # Workflow coordination
│   │   ├── routes.py         # Analysis endpoint
│   │   └── schemas.py        # Request/response models
│   ├── tests/                # Test suite
│   ├── main.py               # FastAPI app
│   ├── config.py             # Configuration
│   ├── database.py           # Database setup
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── hooks/            # Custom hooks
│   │   ├── utils/            # Utilities
│   │   ├── App.jsx           # Main app
│   │   └── index.css         # Styles
│   ├── package.json
│   └── vite.config.js
├── database/
│   ├── schema.sql            # Database schema
│   └── seed.sql              # Sample data
├── docs/                     # Documentation
├── docker-compose.yml
└── .env.example
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET` | Secret key for JWT signing | Yes |
| `HUGGINGFACE_API_TOKEN` | Hugging Face API token | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `CORS_ORIGINS` | Allowed CORS origins | No |

## Security Features

- ✅ Bcrypt password hashing
- ✅ JWT token authentication
- ✅ Protected API endpoints
- ✅ CORS configuration
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Input validation (Pydantic)

## Error Handling

The application handles:
- Network timeouts
- Invalid API responses
- Authentication failures
- Database errors
- Rate limiting (API-dependent)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation in `/docs`
- Review API docs at `/docs` endpoint

## Acknowledgments

- Hugging Face for zero-shot classification
- Google for Gemini API
- FastAPI and React communities
