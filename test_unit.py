import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from classifier import IntelligentServiceClassifier
from models import ClassificationResponse, CategoryResponse, ServiceCategory

@pytest.fixture
def classifier():
    """Create a test classifier instance"""
    with patch('classifier.ChatMistralAI'):
        return IntelligentServiceClassifier(api_key="test_key")

@pytest.mark.asyncio
async def test_greeting_no_ticket(classifier):
    """Test that greetings don't create tickets"""
    
    # Mock the AI response
    mock_response = AsyncMock()
    mock_response.content = '''
    {
        "should_create_ticket": false,
        "categories": [],
        "confidence": 0.98,
        "reasoning": "greeting message",
        "suggested_priority": "low",
        "estimated_completion_time": null
    }
    '''
    
    with patch.object(classifier.llm, 'ainvoke', return_value=mock_response):
        result = await classifier.classify_message("Hello, good morning!")
    
    assert result.should_create_ticket == False
    assert len(result.categories) == 0
    assert result.confidence >= 0.9

@pytest.mark.asyncio
async def test_coffee_request_creates_ticket(classifier):
    """Test that coffee requests create appropriate tickets"""
    
    mock_response = AsyncMock()
    mock_response.content = '''
    {
        "should_create_ticket": true,
        "categories": [
            {
                "category": "service_fb",
                "message": "Guest requests coffee delivery",
                "urgency": "medium"
            }
        ],
        "confidence": 0.95,
        "reasoning": "explicit food/beverage request",
        "suggested_priority": "medium",
        "estimated_completion_time": "10-15 minutes"
    }
    '''
    
    with patch.object(classifier.llm, 'ainvoke', return_value=mock_response):
        result = await classifier.classify_message("I need coffee")
    
    assert result.should_create_ticket == True
    assert len(result.categories) == 1
    assert result.categories[0].category == ServiceCategory.SERVICE_FB
    assert "coffee" in result.categories[0].message.lower()

@pytest.mark.asyncio
async def test_multiple_services_request(classifier):
    """Test that multiple service requests create multiple tickets"""
    
    mock_response = AsyncMock()
    mock_response.content = '''
    {
        "should_create_ticket": true,
        "categories": [
            {
                "category": "maintenance",
                "message": "Air conditioning unit malfunction requiring repair",
                "urgency": "high"
            },
            {
                "category": "housekeeping",
                "message": "Guest requests fresh towel delivery",
                "urgency": "medium"
            }
        ],
        "confidence": 0.92,
        "reasoning": "Two distinct services: urgent maintenance and routine housekeeping",
        "suggested_priority": "high",
        "estimated_completion_time": "30-60 minutes"
    }
    '''
    
    with patch.object(classifier.llm, 'ainvoke', return_value=mock_response):
        result = await classifier.classify_message("My AC is broken and I need towels")
    
    assert result.should_create_ticket == True
    assert len(result.categories) == 2
    
    categories = [cat.category for cat in result.categories]
    assert ServiceCategory.MAINTENANCE in categories
    assert ServiceCategory.HOUSEKEEPING in categories

@pytest.mark.asyncio
async def test_emergency_high_priority(classifier):
    """Test that emergencies get high priority"""
    
    mock_response = AsyncMock()
    mock_response.content = '''
    {
        "should_create_ticket": true,
        "categories": [
            {
                "category": "maintenance",
                "message": "EMERGENCY: Water flooding in bathroom requires immediate attention",
                "urgency": "urgent"
            }
        ],
        "confidence": 0.99,
        "reasoning": "Emergency situation requiring immediate response",
        "suggested_priority": "urgent",
        "estimated_completion_time": "immediately"
    }
    '''
    
    with patch.object(classifier.llm, 'ainvoke', return_value=mock_response):
        result = await classifier.classify_message("EMERGENCY! Water flooding my bathroom!")
    
    assert result.should_create_ticket == True
    assert result.suggested_priority == "urgent"
    assert result.categories[0].urgency == "urgent"

@pytest.mark.asyncio
async def test_thank_you_no_ticket(classifier):
    """Test that thank you messages don't create tickets"""
    
    mock_response = AsyncMock()
    mock_response.content = '''
    {
        "should_create_ticket": false,
        "categories": [],
        "confidence": 0.96,
        "reasoning": "gratitude expression without service request",
        "suggested_priority": "low",
        "estimated_completion_time": null
    }
    '''
    
    with patch.object(classifier.llm, 'ainvoke', return_value=mock_response):
        result = await classifier.classify_message("Thank you so much for the excellent service")
    
    assert result.should_create_ticket == False
    assert len(result.categories) == 0

@pytest.mark.asyncio
async def test_information_request_no_ticket(classifier):
    """Test that information requests don't create tickets"""
    
    mock_response = AsyncMock()
    mock_response.content = '''
    {
        "should_create_ticket": false,
        "categories": [],
        "confidence": 0.85,
        "reasoning": "information request, no service needed",
        "suggested_priority": "low",
        "estimated_completion_time": null
    }
    '''
    
    with patch.object(classifier.llm, 'ainvoke', return_value=mock_response):
        result = await classifier.classify_message("What time is breakfast served?")
    
    assert result.should_create_ticket == False
    assert len(result.categories) == 0

@pytest.mark.asyncio
async def test_error_handling(classifier):
    """Test error handling when AI fails"""
    
    with patch.object(classifier.llm, 'ainvoke', side_effect=Exception("AI Error")):
        result = await classifier.classify_message("Test message")
    
    assert result.should_create_ticket == False
    assert len(result.categories) == 0
    assert result.confidence == 0.0
    assert "Classification failed" in result.reasoning

@pytest.mark.asyncio
async def test_service_insights(classifier):
    """Test service insights functionality"""
    
    mock_response = AsyncMock()
    mock_response.content = '''
    {
        "sentiment": "frustrated",
        "emotion_detected": "urgent",
        "language_complexity": "simple",
        "implicit_needs": ["immediate attention", "comfort restoration"],
        "guest_type": "business",
        "contextual_hints": ["emergency language", "urgent tone"]
    }
    '''
    
    with patch.object(classifier.llm, 'ainvoke', return_value=mock_response):
        insights = await classifier.get_service_insights("URGENT! My AC is broken!")
    
    assert insights["sentiment"] == "frustrated"
    assert insights["emotion_detected"] == "urgent"
    assert len(insights["implicit_needs"]) > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
