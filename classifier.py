import os
from typing import List, Dict, Any
from langchain_mistralai import ChatMistralAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
import json
import logging
from models import ClassificationResponse, CategoryResponse, ServiceCategory

logger = logging.getLogger(__name__)

class IntelligentServiceClassifier:
    def __init__(self, api_key: str, model_name: str = "mistral-large-latest"):
        self.llm = ChatMistralAI(
            api_key=api_key,
            model=model_name,
            temperature=0.1,
            max_tokens=2000
        )
        
        # NO HARDCODED SERVICE DEFINITIONS - Let AI determine everything
        self.system_prompt = self._create_system_prompt()
        
        # Setup output parser for structured JSON
        self.output_parser = PydanticOutputParser(pydantic_object=ClassificationResponse)
    
    def _create_system_prompt(self) -> str:
        return """You are an extremely intelligent AI hotel service classifier. You have complete autonomy to:

1. DYNAMICALLY determine what constitutes a service request
2. INTELLIGENTLY categorize services without any predefined rules
3. AUTONOMOUSLY assess urgency, priority, and completion times
4. GENERATE all service categories, messages, and metadata from scratch

YOUR INTELLIGENCE GUIDELINES:
- Analyze guest messages with complete contextual understanding
- Create service categories dynamically based on the actual request
- Generate intelligent, specific messages for hotel staff
- Determine urgency levels using natural language understanding
- Estimate realistic completion times based on service complexity
- Use your knowledge of hotel operations to make intelligent decisions

AVAILABLE SERVICE CATEGORY KEYS (use these exact keys when applicable):
- "service_fb": Food & Beverage services
- "housekeeping": Room cleaning and maintenance
- "maintenance": Repairs and technical issues  
- "porter": Luggage and transport assistance
- "concierge": External services and recommendations
- "reception": Front desk and administrative services

CRITICAL RULES:
1. ONLY create tickets for explicit service requests or problems that require staff action
2. NO tickets for: greetings ("hello", "good morning"), thank you messages, simple informational questions ("what time does X close?"), general compliments
3. Multiple categories when guest explicitly requests multiple distinct services (e.g., "room service + extra pillows + taxi booking")
4. ALL data must be AI-generated - no hardcoded responses
5. Generate contextual, intelligent messages for each category
6. For non-actionable messages, set should_create_ticket: false and provide empty categories array

RESPONSE FORMAT - Return ONLY valid JSON (no markdown, no formatting, clean structure):
{
  "should_create_ticket": boolean,
  "categories": [
    {
      "category": "appropriate_category_key",
      "message": "Single line message for hotel staff without special characters",
      "urgency": "low/medium/high/urgent"
    }
  ],
  "confidence": 0.0-1.0,
  "reasoning": "Single line explanation without line breaks or special characters",
  "suggested_priority": "low/medium/high/urgent",
  "estimated_completion_time": "Simple time estimate or null"
}

Use your complete intelligence to analyze the guest message and generate appropriate responses. No hardcoded rules - pure AI analysis."""

    async def classify_message(self, guest_message: str, guest_id: str = None, room_number: str = None) -> ClassificationResponse:
        try:
            # Create context-aware prompt - let AI analyze everything
            user_prompt = f"""
GUEST MESSAGE: "{guest_message}"

CONTEXT:
- Guest ID: {guest_id or 'Unknown'}
- Room Number: {room_number or 'Unknown'}

TASK: Analyze this hotel guest message with complete AI intelligence. Use your understanding of:
- Hotel service operations
- Guest communication patterns  
- Service urgency assessment
- Natural language nuances
- Contextual implications

Generate a complete classification response using ONLY your AI analysis. Do not rely on any predefined rules - use your intelligence to determine everything dynamically.

Return response as valid JSON only.
"""
            
            # Create messages for LangChain
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            # Get AI response through LangChain
            response = await self.llm.ainvoke(messages)
            
            # Extract content from LangChain response
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            # Clean the response to extract pure JSON
            content = content.strip()
            
            # Remove any markdown formatting
            if content.startswith('```json'):
                content = content[7:-3].strip()
            elif content.startswith('```'):
                content = content[3:-3].strip()
            
            # Remove any non-printable characters that could break JSON
            content = ''.join(char for char in content if char.isprintable() or char in '\n\r\t')
            
            # Also remove problematic characters that can cause JSON issues
            content = content.replace('\x00', '').replace('\x08', '').replace('\x0c', '')
            
            # Ensure no unescaped quotes in strings
            lines = content.split('\n')
            cleaned_lines = []
            for line in lines:
                if '"message":' in line or '"reasoning":' in line:
                    # Extract the value part and clean it
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        key_part = parts[0]
                        value_part = parts[1].strip()
                        if value_part.startswith('"') and value_part.endswith('"') or value_part.endswith('",'):
                            # Remove internal quotes and clean the text
                            if value_part.endswith('",'):
                                end_char = '",'
                                value_content = value_part[1:-2]
                            else:
                                end_char = '"'
                                value_content = value_part[1:-1]
                            
                            # Clean the content
                            value_content = value_content.replace('"', "'").replace('\n', ' ').replace('\r', ' ')
                            value_content = ' '.join(value_content.split())  # Normalize whitespace
                            
                            line = f'{key_part}: "{value_content}"{end_char[1:]}'
                
                cleaned_lines.append(line)
            
            content = '\n'.join(cleaned_lines)
            
            # Parse the AI-generated JSON
            try:
                result_dict = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing failed: {e}. Content: {content[:300]}")
                # Let AI try to fix the JSON
                return await self._handle_json_error(content, guest_message)
            
            # Convert AI response to Pydantic models
            categories = []
            for cat_data in result_dict.get("categories", []):
                try:
                    category = ServiceCategory(cat_data["category"])
                    categories.append(CategoryResponse(
                        category=category,
                        message=cat_data["message"],
                        urgency=cat_data["urgency"]
                    ))
                except (KeyError, ValueError) as e:
                    logger.warning(f"Invalid category data: {cat_data}, error: {e}")
                    continue

            return ClassificationResponse(
                should_create_ticket=result_dict.get("should_create_ticket", False),
                categories=categories,
                confidence=result_dict.get("confidence", 0.0),
                reasoning=result_dict.get("reasoning", "AI classification completed"),
                suggested_priority=result_dict.get("suggested_priority") or "low",
                estimated_completion_time=result_dict.get("estimated_completion_time")
            )
                
        except Exception as e:
            logger.error(f"Classification error: {str(e)}")
            # Return AI-informed fallback
            return ClassificationResponse(
                should_create_ticket=False,
                categories=[],
                confidence=0.0,
                reasoning=f"AI classification failed: {str(e)}",
                suggested_priority="low",
                estimated_completion_time=None
            )
    
    async def _handle_json_error(self, broken_content: str, original_message: str) -> ClassificationResponse:
        """Let AI fix broken JSON responses"""
        try:
            fix_prompt = f"""
The following JSON response is malformed:
{broken_content}

Original guest message: "{original_message}"

Please provide a corrected, valid JSON response for this hotel service classification. 
Return ONLY valid JSON without any markdown or explanation.
"""
            
            messages = [HumanMessage(content=fix_prompt)]
            response = await self.llm.ainvoke(messages)
            
            content = response.content if hasattr(response, 'content') else str(response)
            content = content.strip()
            
            # Clean again
            if content.startswith('```json'):
                content = content[7:-3].strip()
            elif content.startswith('```'):
                content = content[3:-3].strip()
            
            result_dict = json.loads(content)
            
            # Convert to response format
            categories = []
            for cat_data in result_dict.get("categories", []):
                try:
                    categories.append(CategoryResponse(
                        category=ServiceCategory(cat_data["category"]),
                        message=cat_data["message"],
                        urgency=cat_data["urgency"]
                    ))
                except (KeyError, ValueError):
                    continue
            
            return ClassificationResponse(
                should_create_ticket=result_dict.get("should_create_ticket", False),
                categories=categories,
                confidence=result_dict.get("confidence", 0.0),
                reasoning=result_dict.get("reasoning", "AI JSON repair completed"),
                suggested_priority=result_dict.get("suggested_priority", "low"),
                estimated_completion_time=result_dict.get("estimated_completion_time")
            )
            
        except Exception as e:
            logger.error(f"JSON repair failed: {e}")
            return ClassificationResponse(
                should_create_ticket=False,
                categories=[],
                confidence=0.0,
                reasoning="AI unable to process request - JSON repair failed",
                suggested_priority="low",
                estimated_completion_time=None
            )
    
    def _parse_fallback_response(self, content: str) -> Dict[str, Any]:
        """Fallback parsing for malformed JSON responses"""
        # Basic fallback - this could be enhanced with regex parsing
        return {
            "should_create_ticket": False,
            "categories": [],
            "confidence": 0.0,
            "reasoning": "Unable to parse AI response",
            "suggested_priority": "low",
            "estimated_completion_time": None
        }
    
    async def get_service_insights(self, message: str) -> Dict[str, Any]:
        """AI-powered insights generation with no hardcoded data"""
        insights_prompt = f"""
GUEST MESSAGE: "{message}"

TASK: Using your complete AI intelligence, analyze this hotel guest message and provide detailed psychological and operational insights. Generate everything dynamically based on your understanding of:

- Human communication patterns
- Emotional intelligence
- Hotel service psychology  
- Guest behavior analysis
- Cultural and linguistic nuances

Provide insights in pure JSON format (no markdown):
{{
    "sentiment": "AI-determined sentiment",
    "emotion_detected": "AI-identified primary emotion",
    "urgency_indicators": ["AI-identified urgency signals"],
    "service_complexity": "AI-assessed complexity level",
    "guest_profile": "AI-inferred guest characteristics",
    "communication_style": "AI-analyzed communication pattern",
    "implicit_needs": ["AI-detected unstated requirements"],
    "recommended_approach": "AI-suggested staff approach",
    "priority_justification": "AI reasoning for priority level",
    "contextual_hints": ["AI-identified relevant context"],
    "risk_factors": ["AI-identified potential issues"],
    "success_indicators": ["AI-suggested fulfillment metrics"]
}}

Use pure AI analysis - no predefined categories or hardcoded responses.
"""
        
        try:
            response = await self.llm.ainvoke([HumanMessage(content=insights_prompt)])
            
            # Handle different response formats
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            # Clean and parse JSON
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:-3].strip()
            elif content.startswith('```'):
                content = content[3:-3].strip()
            
            # Clean control characters
            content = ''.join(char for char in content if ord(char) >= 32 or char in '\n\r\t')
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Insights generation error: {str(e)}")
            return {
                "error": f"AI insights generation failed: {str(e)}",
                "fallback_analysis": "Unable to provide detailed insights due to processing error"
            }
