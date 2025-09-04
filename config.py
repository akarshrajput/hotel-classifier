# Configuration file for the Hotel Service Request Classifier

# AI Model Configuration
MODEL_CONFIG = {
    "name": "mistral-large-latest",
    "temperature": 0.1,
    "max_tokens": 1000,
    "fallback_model": "mistral-medium-latest"  # Backup model if primary fails
}

# Service Categories Configuration
SERVICE_CATEGORIES = {
    "service_fb": {
        "name": "Food & Beverage",
        "description": "Food, beverages, room service, restaurant requests, coffee, tea, meals, drinks, dining, kitchen, bar, alcohol, snacks, water, ice",
        "typical_completion_time": "15-30 minutes",
        "department": "F&B"
    },
    "housekeeping": {
        "name": "Housekeeping",
        "description": "Room cleaning, towels, linens, bathroom supplies, bed making, trash removal, vacuum, dusting, room tidying, fresh sheets, pillows, blankets",
        "typical_completion_time": "20-45 minutes",
        "department": "Housekeeping"
    },
    "maintenance": {
        "name": "Maintenance",
        "description": "Repairs, technical issues, broken items, AC/heating, plumbing, electrical, lights, TV, WiFi, locks, windows, fixtures, appliances",
        "typical_completion_time": "30-120 minutes",
        "department": "Engineering"
    },
    "porter": {
        "name": "Porter Services",
        "description": "Luggage assistance, heavy item moving, transportation of bags, carrying items, bell services, package delivery",
        "typical_completion_time": "5-15 minutes",
        "department": "Bell Services"
    },
    "concierge": {
        "name": "Concierge",
        "description": "External services, directions, recommendations, bookings outside hotel, tours, tickets, transportation, local information, attractions",
        "typical_completion_time": "10-60 minutes",
        "department": "Concierge"
    },
    "reception": {
        "name": "Reception",
        "description": "Check-in/out, billing, room changes, hotel policies, complaints, front desk services, reservations, account issues, key cards",
        "typical_completion_time": "5-20 minutes",
        "department": "Front Office"
    }
}

# Classification Thresholds
CLASSIFICATION_THRESHOLDS = {
    "min_confidence": 0.7,  # Minimum confidence to create a ticket
    "high_confidence": 0.9,  # Threshold for high confidence classifications
    "emergency_keywords": ["emergency", "urgent", "flooding", "fire", "broken", "help", "immediately"],
    "greeting_patterns": ["hello", "hi", "good morning", "good evening", "how are you"],
    "thanks_patterns": ["thank", "thanks", "appreciate", "grateful"]
}

# Priority Mapping
PRIORITY_MAPPING = {
    "low": {
        "response_time": "Within 2 hours",
        "urgency_keywords": ["whenever", "later", "no rush"]
    },
    "medium": {
        "response_time": "Within 1 hour",
        "urgency_keywords": ["soon", "please", "when possible"]
    },
    "high": {
        "response_time": "Within 30 minutes",
        "urgency_keywords": ["quickly", "asap", "important", "need now"]
    },
    "urgent": {
        "response_time": "Immediately",
        "urgency_keywords": ["emergency", "urgent", "immediately", "critical", "help"]
    }
}

# System Prompts Configuration
SYSTEM_PROMPTS = {
    "classification": """You are an AI-powered hotel service request classifier with advanced natural language understanding. 
    Your task is to analyze guest messages with surgical precision and determine if service tickets should be created.""",
    
    "insights": """Analyze this guest message and provide detailed psychological and contextual insights 
    to help hotel staff better understand and serve the guest."""
}

# API Configuration
API_CONFIG = {
    "default_host": "0.0.0.0",
    "default_port": 8000,
    "cors_origins": ["*"],  # Configure for production
    "rate_limit": "100/minute",
    "timeout": 30  # seconds
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/classifier.log",
    "max_file_size": "10MB",
    "backup_count": 5
}
