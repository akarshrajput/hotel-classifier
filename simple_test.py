#!/usr/bin/env python3
"""
Simple Interactive Test - Pure AI Hotel Service Classifier
Shows the AI working with clean JSON responses
"""

import asyncio
import json
import os
from classifier import IntelligentServiceClassifier
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def simple_test():
    """Simple test with clean AI responses"""
    
    print("🤖 Pure AI Hotel Service Classifier - Interactive Test")
    print("=" * 60)
    
    # Initialize classifier
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("❌ Please set MISTRAL_API_KEY in .env file")
        return
    
    classifier = IntelligentServiceClassifier(api_key=api_key)
    
    # Simple test cases
    test_messages = [
        "I need coffee",
        "Hello good morning", 
        "My AC is broken",
        "Thank you very much"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🧪 Test {i}: '{message}'")
        print("-" * 40)
        
        try:
            # Test classification
            result = await classifier.classify_message(
                guest_message=message,
                guest_id=f"G{i}",
                room_number=f"10{i}"
            )
            
            print(f"🎫 Create Ticket: {result.should_create_ticket}")
            print(f"🔍 Confidence: {result.confidence:.1%}")
            print(f"⚡ Priority: {result.suggested_priority}")
            print(f"💭 Reasoning: {result.reasoning[:100]}...")
            
            if result.categories:
                print("📋 Categories:")
                for cat in result.categories:
                    print(f"   • {cat.category.value}: {cat.message[:80]}...")
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:100]}...")
        
        print()
        
        # Small delay to avoid rate limiting
        await asyncio.sleep(2)
    
    print("✨ Pure AI Analysis Complete!")
    print("\n🎯 Key Features Demonstrated:")
    print("   • Zero hardcoded rules - pure AI intelligence")
    print("   • Dynamic service category detection")
    print("   • Intelligent reasoning and explanation")
    print("   • Context-aware message generation")
    print("   • Smart confidence and priority assessment")

if __name__ == "__main__":
    try:
        asyncio.run(simple_test())
    except KeyboardInterrupt:
        print("\n👋 Test stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
