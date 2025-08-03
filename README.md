# URL Shortener Service

## Overview
This is a lightweight URL shortener service built using Flask, simulating services like Bitly or TinyURL. It generates a 6-character alphanumeric short code for any valid long URL, supports redirection, and provides click analytics — all using an in-memory data store (no external DB).

## Features
- Shorten URLs via `POST /api/shorten`
- Redirect to original URL via `GET /<short_code>`
- View Analytics for a short URL via `GET /api/stats/<short_code>`
- All data is stored in memory, meaning it's fast but temporary (resets on restart)
- Full test coverage with `pytest`

## Getting Started

### Prerequisites
- Python 3.8+ installed
- 3 hours of uninterrupted time

### Setup (Should take < 5 minutes)
```bash
# Clone/download this repository
# Navigate to the assignment directory
cd url-shortener

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the application
python -m flask --app app run

# The API will be available at http://localhost:5000
# Run tests with: pytest
```

### Core Functionality

1. **Shorten URL Endpoint**
   - `POST /api/shorten`
   - Accept a long URL in the request body
   - Return a short code (e.g., "abc123")
   - Store the mapping for later retrieval

2. **Redirect Endpoint**
   - `GET /<short_code>`
   - Redirect to the original URL
   - Return 404 if short code doesn't exist
   - Track each redirect (increment click count)

3. **Analytics Endpoint**
   - `GET /api/stats/<short_code>`
   - Return click count for the short code
   - Return creation timestamp
   - Return the original URL

### Technical Requirements

- URLs must be validated before shortening
- Short codes should be 6 characters (alphanumeric)
- Handle concurrent requests properly
- Include basic error handling
- Write at least 5 tests covering core functionality

### Example API Usage

```bash
# Shorten a URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'

# Response: {"short_code": "abc123", "short_url": "http://localhost:5000/abc123"}

# Use the short URL (this redirects)
curl -L http://localhost:5000/abc123

# Get analytics
curl http://localhost:5000/api/stats/abc123

# Response: {"url": "https://www.example.com/very/long/url", "clicks": 5, "created_at": "2024-01-01T10:00:00"}
```