# Hotel Service Request Classifier

An intelligent AI-powered system for classifying hotel guest service requests using FastAPI, LangChain, and Mistral AI.

## Features

🤖 **AI-Powered Classification**: Uses Mistral AI for intelligent message analysis
📊 **Dynamic Categorization**: No hardcoded rules - everything determined by AI
🎯 **Precision Targeting**: Only creates tickets for explicit service requests
⚡ **Priority Assessment**: Automatically determines urgency and priority levels
🔍 **Deep Insights**: Sentiment analysis, emotion detection, and contextual understanding
📦 **Batch Processing**: Handle multiple requests simultaneously
🚀 **Production Ready**: FastAPI with proper error handling and logging

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd guestflowmvp-model

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Mistral AI API key
MISTRAL_API_KEY=your_mistral_api_key_here
```

### 3. Run the API

```bash
# Start the FastAPI server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. Test the System

```bash
# Run automated tests
python test_classifier.py

# Interactive testing
python test_classifier.py interactive

# Test API endpoints
python api_client.py
```

## API Endpoints

### POST `/classify`

Classify a guest service request message.

**Request:**

```json
{
  "guest_message": "I need coffee and clean my room",
  "guest_id": "G001",
  "room_number": "101"
}
```

**Response:**

```json
{
  "should_create_ticket": true,
  "categories": [
    {
      "category": "service_fb",
      "message": "Guest requests coffee delivery",
      "urgency": "medium"
    },
    {
      "category": "housekeeping",
      "message": "Guest requests room cleaning service",
      "urgency": "low"
    }
  ],
  "confidence": 0.95,
  "reasoning": "Guest explicitly requested two distinct services",
  "suggested_priority": "medium",
  "estimated_completion_time": "20-30 minutes"
}
```

### POST `/insights`

Get detailed insights about a guest message.

### POST `/batch-classify`

Classify multiple messages simultaneously.

### GET `/categories`

Get all available service categories.

### GET `/health`

API health check.

## Service Categories

- **service_fb**: Food, beverages, room service, restaurant requests
- **housekeeping**: Room cleaning, towels, linens, bathroom supplies
- **maintenance**: Repairs, technical issues, broken items, AC, heating
- **porter**: Luggage assistance, heavy item moving, transportation
- **concierge**: External services, directions, recommendations, bookings
- **reception**: Check-in/out, billing, room changes, hotel policies

## Classification Rules

The AI follows these intelligent rules:

✅ **Creates tickets for:**

- Explicit service requests ("I need coffee")
- Problem reports ("My AC is broken")
- Urgent situations ("Emergency! Water flooding!")

❌ **Does NOT create tickets for:**

- Greetings ("Hello, good morning")
- Pleasantries ("Thank you so much")
- General questions ("What time is breakfast?")

## Advanced Features

### Intelligent Message Generation

Each category gets a specific, contextual message:

- Input: "Coffee urgently for meeting"
- Output: "Guest requires urgent coffee delivery for business meeting"

### Urgency Assessment

AI determines urgency levels:

- **Low**: Routine requests
- **Medium**: Standard comfort issues
- **High**: Significant problems, urgent needs
- **Urgent**: Emergencies, safety concerns

### Priority Calculation

Overall priority considers:

- Service complexity
- Guest tone and language
- Time sensitivity
- Safety implications

### Completion Time Estimation

AI estimates realistic completion times based on:

- Service type complexity
- Staff availability patterns
- Urgency level

## Example Classifications

```python
# No ticket - greeting
"Hello, good morning!" → No ticket created

# Single service
"I need coffee" → service_fb ticket

# Multiple services
"My AC is broken and I need towels" → maintenance + housekeeping tickets

# Emergency
"EMERGENCY! Water flooding!" → urgent maintenance ticket

# Information request
"What time is breakfast?" → No ticket created
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   LangChain      │    │   Mistral AI    │
│   Web Server    │───▶│   Orchestration  │───▶│   Language      │
│                 │    │                  │    │   Model         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Pydantic      │    │   Intelligent    │    │   JSON          │
│   Data Models   │    │   Classifier     │    │   Responses     │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Development

### Project Structure

```
guestflowmvp-model/
├── main.py              # FastAPI application
├── classifier.py        # AI classifier logic
├── models.py           # Pydantic data models
├── test_classifier.py  # Testing utilities
├── api_client.py       # API client example
├── requirements.txt    # Dependencies
├── .env.example       # Environment template
└── README.md          # This file
```

### Adding New Features

1. **New Service Categories**: Update `service_definitions` in `classifier.py`
2. **Custom Rules**: Modify the system prompt in `_create_system_prompt()`
3. **Additional Insights**: Extend `get_service_insights()` method
4. **New Endpoints**: Add routes to `main.py`

## Production Deployment

### Environment Variables

```bash
MISTRAL_API_KEY=your_production_key
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG_MODE=False
MODEL_NAME=mistral-large-latest
TEMPERATURE=0.1
MAX_TOKENS=1000
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

### Performance Considerations

- Use connection pooling for high throughput
- Implement request caching for repeated messages
- Monitor API rate limits
- Set up proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:

- Create GitHub issues for bugs
- Check logs for debugging information
- Review test cases for usage examples
