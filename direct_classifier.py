import os
import json
import httpx
import logging
from typing import List, Dict, Any
from models import ClassificationResponse, CategoryResponse, ServiceCategory

logger = logging.getLogger(__name__)

class DirectMistralClassifier:
    """Direct Mistral AI integration without LangChain"""
    
    def __init__(self, api_key: str, model_name: str = "mistral-large-latest"):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        
        self.service_definitions = {
            "service_fb": "Food, beverages, room service, restaurant requests, coffee, tea, meals, drinks, dining, kitchen, bar, alcohol, snacks, water, ice",
            "housekeeping": "Room cleaning, towels, linens, bathroom supplies, bed making, trash removal, vacuum, dusting, room tidying, fresh sheets, pillows, blankets",
            "maintenance": "Repairs, technical issues, broken items, AC/heating, plumbing, electrical, lights, TV, WiFi, locks, windows, fixtures, appliances",
            "porter": "Luggage assistance, heavy item moving, transportation of bags, carrying items, bell services, package delivery",
            "concierge": "External services, directions, recommendations, bookings outside hotel, tours, tickets, transportation, local information, attractions",
            "reception": "Check-in/out, billing, room changes, hotel policies, complaints, front desk services, reservations, account issues, key cards"
        }
        
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        return f"""You are an AI-powered hotel service request classifier with advanced natural language understanding. Your task is to analyze guest messages with surgical precision.

SERVICE CATEGORIES AND DEFINITIONS:
{json.dumps(self.service_definitions, indent=2)}

CLASSIFICATION RULES:
1. ONLY create tickets for explicit service requests or problem reports
2. NO tickets for: greetings, pleasantries, thank you messages, general questions without service requests
3. Multiple categories ONLY when guest explicitly mentions multiple distinct services
4. Generate intelligent, contextual messages for each category
5. Assess urgency and priority based on context and language used
6. Estimate completion times based on service complexity

URGENCY LEVELS:
- low: routine requests, non-urgent maintenance, general services
- medium: comfort issues, moderate problems, standard room service
- high: safety concerns, significant discomfort, urgent repairs
- urgent: emergencies, security issues, critical breakdowns

RESPONSE FORMAT (JSON only, no markdown):
{{
  "should_create_ticket": boolean,
  "categories": [
    {{
      "category": "service_category_key",
      "message": "Specific, actionable message for staff",
      "urgency": "urgency_level"
    }}
  ],
  "confidence": 0.0-1.0,
  "reasoning": "detailed explanation of classification decision",
  "suggested_priority": "overall_priority_level",
  "estimated_completion_time": "time_estimate_or_null"
}}

EXAMPLES:
Input: "Hello, good morning!"
Output: {{"should_create_ticket": false, "categories": [], "confidence": 0.98, "reasoning": "Greeting without service request", "suggested_priority": "none", "estimated_completion_time": null}}

Input: "I need coffee urgently for my meeting"
Output: {{"should_create_ticket": true, "categories": [{{"category": "service_fb", "message": "Guest requires urgent coffee delivery for business meeting", "urgency": "high"}}], "confidence": 0.95, "reasoning": "Explicit urgent food/beverage request", "suggested_priority": "high", "estimated_completion_time": "10-15 minutes"}}

Analyze ONLY explicit content. Generate intelligent, contextual responses. Return valid JSON only."""

    async def classify_message(self, guest_message: str, guest_id: str = None, room_number: str = None) -> ClassificationResponse:
        try:
            # Create context-aware prompt
            context = f"Guest Message: '{guest_message}'"
            if guest_id:
                context += f"\nGuest ID: {guest_id}"
            if room_number:
                context += f"\nRoom Number: {room_number}"
            
            # Prepare the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"{context}\n\nClassify this guest message and provide the JSON response:"}
                ],
                "temperature": 0.1,
                "max_tokens": 1000
            }
            
            # Make the API request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                
                # Parse the response
                response_data = response.json()
                ai_response = response_data["choices"][0]["message"]["content"]
                
                # Clean and parse JSON
                ai_response = ai_response.strip()
                # Remove markdown formatting
                if ai_response.startswith('```json'):
                    ai_response = ai_response[7:-3].strip()
                elif ai_response.startswith('```'):
                    ai_response = ai_response[3:-3].strip()
                
                # Clean control characters
                ai_response = ''.join(char for char in ai_response if ord(char) >= 32 or char in '\n\r\t')
                
                result_dict = json.loads(ai_response)
                
                # Convert to Pydantic models
                categories = [
                    CategoryResponse(
                        category=ServiceCategory(cat["category"]),
                        message=cat["message"],
                        urgency=cat["urgency"]
                    )
                    for cat in result_dict.get("categories", [])
                ]
                
                return ClassificationResponse(
                    should_create_ticket=result_dict["should_create_ticket"],
                    categories=categories,
                    confidence=result_dict["confidence"],
                    reasoning=result_dict["reasoning"],
                    suggested_priority=result_dict.get("suggested_priority", "low"),
                    estimated_completion_time=result_dict.get("estimated_completion_time")
                )
                
        except Exception as e:
            logger.error(f"Classification error: {str(e)}")
            # Return safe fallback
            return ClassificationResponse(
                should_create_ticket=False,
                categories=[],
                confidence=0.0,
                reasoning=f"Classification failed: {str(e)}",
                suggested_priority="low",
                estimated_completion_time=None
            )
    
    async def get_service_insights(self, message: str) -> Dict[str, Any]:
        """Additional method to get detailed insights about the service request"""
        insights_prompt = f"""Analyze this guest message and provide detailed insights:
        
        Message: "{message}"
        
        Provide insights in JSON format (no markdown):
        {{
            "sentiment": "positive/neutral/negative",
            "emotion_detected": "calm/frustrated/angry/urgent/polite",
            "language_complexity": "simple/moderate/complex",
            "implicit_needs": ["list of potential unstated needs"],
            "guest_type": "business/leisure/family/vip",
            "contextual_hints": ["relevant context clues"]
        }}"""
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": insights_prompt}],
                "temperature": 0.1,
                "max_tokens": 500
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                
                response_data = response.json()
                ai_response = response_data["choices"][0]["message"]["content"]
                
                # Clean and parse JSON
                ai_response = ai_response.strip()
                if ai_response.startswith('```json'):
                    ai_response = ai_response[7:-3].strip()
                elif ai_response.startswith('```'):
                    ai_response = ai_response[3:-3].strip()
                
                # Clean control characters
                ai_response = ''.join(char for char in ai_response if ord(char) >= 32 or char in '\n\r\t')
                
                return json.loads(ai_response)
                
        except Exception as e:
            logger.error(f"Insights generation error: {str(e)}")
            return {"error": str(e)}
