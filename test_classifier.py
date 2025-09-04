import asyncio
import json
from classifier import IntelligentServiceClassifier
from models import ClassificationRequest
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_classifier():
    """Test the intelligent service classifier with various scenarios"""
    
    # Initialize classifier
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("Please set MISTRAL_API_KEY in your .env file")
        return
    
    classifier = IntelligentServiceClassifier(api_key=api_key)
    
    # Test cases
    test_cases = [
        {
            "message": "Hello, good morning!",
            "expected": "no ticket"
        },
        {
            "message": "I need coffee urgently for my meeting",
            "expected": "service_fb ticket"
        },
        {
            "message": "My AC is broken and I need fresh towels",
            "expected": "maintenance + housekeeping tickets"
        },
        {
            "message": "Can you help me with my luggage and book a taxi?",
            "expected": "porter + concierge tickets"
        },
        {
            "message": "Thank you so much for the excellent service",
            "expected": "no ticket"
        },
        {
            "message": "What time is breakfast served?",
            "expected": "no ticket"
        },
        {
            "message": "EMERGENCY! Water is flooding my bathroom!",
            "expected": "urgent maintenance ticket"
        },
        {
            "message": "I'd like room service - pasta and wine please",
            "expected": "service_fb ticket"
        },
        {
            "message": "My key card isn't working and I'm locked out",
            "expected": "reception ticket"
        },
        {
            "message": "Could you recommend a good restaurant nearby?",
            "expected": "concierge ticket"
        }
    ]
    
    print("🤖 Testing Intelligent Hotel Service Request Classifier\n")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}:")
        print(f"📝 Message: '{test_case['message']}'")
        print(f"🎯 Expected: {test_case['expected']}")
        print("-" * 40)
        
        try:
            result = await classifier.classify_message(
                guest_message=test_case['message'],
                guest_id=f"guest_{i}",
                room_number=f"10{i:02d}"
            )
            
            print(f"✅ Should Create Ticket: {result.should_create_ticket}")
            print(f"🔍 Confidence: {result.confidence:.2f}")
            print(f"⚡ Priority: {result.suggested_priority}")
            print(f"⏱️ Est. Time: {result.estimated_completion_time or 'N/A'}")
            print(f"💭 Reasoning: {result.reasoning}")
            
            if result.categories:
                print("📋 Categories:")
                for cat in result.categories:
                    print(f"   • {cat.category.value}: {cat.message} (urgency: {cat.urgency})")
            else:
                print("📋 Categories: None")
            
            # Get insights
            try:
                insights = await classifier.get_service_insights(test_case['message'])
                print(f"🧠 Insights: {json.dumps(insights, indent=2)}")
            except Exception as e:
                print(f"🚨 Insights error: {str(e)}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("=" * 80)
    
    print("\n🎉 Testing completed!")

async def interactive_test():
    """Interactive testing mode"""
    print("🤖 Interactive Hotel Service Request Classifier")
    print("Type 'quit' to exit\n")
    
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("Please set MISTRAL_API_KEY in your .env file")
        return
    
    classifier = IntelligentServiceClassifier(api_key=api_key)
    
    while True:
        try:
            message = input("Enter guest message: ").strip()
            
            if message.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not message:
                continue
            
            print("\n🔄 Processing...")
            result = await classifier.classify_message(message)
            
            print(f"\n✨ Results:")
            print(f"   Ticket Required: {result.should_create_ticket}")
            print(f"   Confidence: {result.confidence:.2f}")
            print(f"   Priority: {result.suggested_priority}")
            print(f"   Reasoning: {result.reasoning}")
            
            if result.categories:
                print("   Categories:")
                for cat in result.categories:
                    print(f"      • {cat.category.value}: {cat.message}")
            
            print("\n" + "-" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        asyncio.run(interactive_test())
    else:
        asyncio.run(test_classifier())
