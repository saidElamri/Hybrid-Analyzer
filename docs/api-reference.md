# API Reference

## Base URL

- Development: `http://localhost:8000`
- Production: `https://your-domain.com/api`

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints

### Health Check

#### GET `/`

Get API information.

**Response:**
```json
{
  "message": "Hybrid-Analyzer API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

#### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Hybrid-Analyzer API"
}
```

---

### Authentication

#### POST `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "username": "string (3-50 chars)",
  "email": "string (valid email)",
  "password": "string (min 8 chars)"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-01-01T12:00:00Z"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Username or email already exists
- `422 Unprocessable Entity`: Validation error

---

#### POST `/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-01-01T12:00:00Z"
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials

---

### Analysis

#### POST `/analyze`

Analyze text using AI services. **Requires authentication.**

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "text": "string (10-50000 chars)",
  "candidate_labels": ["string"] // Optional
}
```

**Example Request:**
```json
{
  "text": "Artificial intelligence is revolutionizing the technology industry with breakthrough innovations in machine learning and neural networks.",
  "candidate_labels": ["technology", "science", "business"]
}
```

**Response (200 OK):**
```json
{
  "category": "technology",
  "score": 0.95,
  "summary": "This article discusses recent advances in AI technology, focusing on machine learning and neural networks.",
  "tone": "positive"
}
```

**Default Categories:**
If `candidate_labels` is not provided, the following default categories are used:
- technology
- politics
- sports
- entertainment
- business
- health
- science

**Error Responses:**
- `401 Unauthorized`: Missing or invalid JWT token
- `422 Unprocessable Entity`: Validation error (text too short/long)
- `500 Internal Server Error`: Analysis failed (API errors, timeouts)

---

## Data Models

### User

```typescript
{
  id: number;
  username: string;
  email: string;
  created_at: string; // ISO 8601 datetime
}
```

### TokenResponse

```typescript
{
  access_token: string;
  token_type: "bearer";
  user: User;
}
```

### AnalyzeRequest

```typescript
{
  text: string; // 10-50000 characters
  candidate_labels?: string[]; // Optional custom categories
}
```

### AnalyzeResponse

```typescript
{
  category: string; // Predicted category
  score: number; // Confidence score (0-1)
  summary: string; // AI-generated summary
  tone: "positive" | "neutral" | "negative";
}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Insufficient permissions
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

---

## Rate Limiting

Rate limiting is dependent on external API providers:

- **Hugging Face**: Free tier has monthly character limits
- **Gemini**: Free tier has 60 requests/minute

Consider implementing client-side throttling for production use.

---

## Examples

### cURL Examples

**Register:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'
```

**Analyze Text:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "text": "Your article text here..."
  }'
```

### JavaScript Examples

**Using Axios:**

```javascript
import axios from 'axios';

// Register
const register = async () => {
  const response = await axios.post('http://localhost:8000/auth/register', {
    username: 'testuser',
    email: 'test@example.com',
    password: 'securepass123'
  });
  return response.data;
};

// Login
const login = async () => {
  const response = await axios.post('http://localhost:8000/auth/login', {
    username: 'testuser',
    password: 'securepass123'
  });
  localStorage.setItem('token', response.data.access_token);
  return response.data;
};

// Analyze
const analyze = async (text) => {
  const token = localStorage.getItem('token');
  const response = await axios.post(
    'http://localhost:8000/analyze',
    { text },
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  return response.data;
};
```

---

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all endpoints
- Test API calls directly
- See request/response schemas
- Try authentication flows
