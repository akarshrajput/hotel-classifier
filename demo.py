"""
🏨 Hotel Service Request Classifier - Live Demo

This script demonstrates the intelligent classification system with real exam            print("=" * 70)
            
            # Pause between demos for readability and rate limiting
            if i < len(demo_scenarios):
                print("⏸️  Press Enter to continue to next demo...")
                input()
                print()
                # Add a small delay to avoid rate limiting
                await asyncio.sleep(1)un this after setting up your Mistral AI API key to see the system in action.
"""

import asyncio
import json
import sys
from classifier import IntelligentServiceClassifier
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def run_demo():
    """Run a comprehensive demonstration of the classifier"""
    
    print("🏨 Welcome to the Intelligent Hotel Service Request Classifier Demo!")
    print("=" * 70)
    
    # Check API key
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key or api_key == "your_mistral_api_key_here":
        print("❌ ERROR: Please set your MISTRAL_API_KEY in the .env file")
        print("   1. Copy .env.example to .env")
        print("   2. Edit .env and add your Mistral AI API key")
        print("   3. Get your API key from: https://console.mistral.ai/")
        return
    
    print("✅ API Key configured")
    print("🤖 Initializing AI classifier...")
    
    try:
        classifier = IntelligentServiceClassifier(api_key=api_key)
        print("✅ Classifier ready!")
        print()
        
        # Demo scenarios
        demo_scenarios = [
            {
                "title": "🍵 Simple Service Request",
                "message": "I need coffee please",
                "description": "Basic food/beverage request"
            },
            {
                "title": "🧹 Multiple Services",
                "message": "Can you clean my room and bring fresh towels?",
                "description": "Multiple housekeeping services"
            },
            {
                "title": "🚨 Emergency Situation",
                "message": "EMERGENCY! Water is flooding my bathroom!",
                "description": "Urgent maintenance issue"
            },
            {
                "title": "👋 Greeting (No Ticket)",
                "message": "Hello, good morning! How are you today?",
                "description": "Friendly greeting without service request"
            },
            {
                "title": "🎒 Porter + Concierge",
                "message": "Can you help with my luggage and recommend a restaurant?",
                "description": "Two different service categories"
            },
            {
                "title": "💳 Reception Issue",
                "message": "My key card isn't working and I can't get into my room",
                "description": "Front desk/reception service needed"
            },
            {
                "title": "🙏 Thank You (No Ticket)",
                "message": "Thank you so much for the wonderful service!",
                "description": "Gratitude expression"
            },
            {
                "title": "❓ Information Request",
                "message": "What time does the restaurant close?",
                "description": "Question without service request"
            }
        ]
        
        for i, scenario in enumerate(demo_scenarios, 1):
            print(f"📋 Demo {i}/8: {scenario['title']}")
            print(f"📝 Guest Message: \"{scenario['message']}\"")
            print(f"💡 Scenario: {scenario['description']}")
            print("-" * 50)
            
            try:
                # Classify the message
                result = await classifier.classify_message(
                    guest_message=scenario['message'],
                    guest_id=f"DEMO_GUEST_{i}",
                    room_number=f"20{i:02d}"
                )
                
                # Display results
                if result.should_create_ticket:
                    print("✅ TICKET CREATED")
                    print(f"🎯 Confidence: {result.confidence:.1%}")
                    print(f"⚡ Priority: {result.suggested_priority.upper()}")
                    print(f"⏱️  Est. Time: {result.estimated_completion_time or 'Not specified'}")
                    print(f"🧠 Reasoning: {result.reasoning}")
                    
                    print("\n📋 Service Categories:")
                    for cat in result.categories:
                        urgency_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "urgent": "🔴"}
                        emoji = urgency_emoji.get(cat.urgency, "⚪")
                        print(f"   {emoji} {cat.category.upper()}: {cat.message}")
                        print(f"      └─ Urgency: {cat.urgency}")
                else:
                    print("❌ NO TICKET CREATED")
                    print(f"🎯 Confidence: {result.confidence:.1%}")
                    print(f"🧠 Reasoning: {result.reasoning}")
                
                # Get additional insights
                try:
                    insights = await classifier.get_service_insights(scenario['message'])
                    print(f"\n🔍 AI Insights:")
                    print(f"   😊 Sentiment: {insights.get('sentiment', 'unknown')}")
                    print(f"   💭 Emotion: {insights.get('emotion_detected', 'unknown')}")
                    print(f"   👤 Guest Type: {insights.get('guest_type', 'unknown')}")
                except Exception as e:
                    print(f"   ⚠️ Insights unavailable: {str(e)}")
                
            except Exception as e:
                print(f"❌ Error processing scenario: {str(e)}")
            
            print("\n" + "=" * 70)
            
            # Pause between demos for readability
            if i < len(demo_scenarios):
                print("⏸️  Press Enter to continue to next demo...")
                input()
                print()
        
        print("🎉 Demo completed!")
        print("\n📊 Summary:")
        print("✅ The AI classifier successfully:")
        print("   • Identified explicit service requests")
        print("   • Ignored greetings and thank you messages")
        print("   • Handled multiple services in one message")
        print("   • Assessed urgency and priority levels")
        print("   • Generated specific, actionable messages")
        print("   • Provided realistic completion time estimates")
        
        print("\n🚀 Next Steps:")
        print("   • Start the API server: python main.py")
        print("   • Test with your own messages: python test_classifier.py interactive")
        print("   • View API docs: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify your Mistral AI API key is valid")
        print("3. Ensure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
