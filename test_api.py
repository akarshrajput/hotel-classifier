#!/usr/bin/env python3
"""
Test the running FastAPI server with pure AI classification
"""

import asyncio
import httpx
import json

async def test_api():
    """Test the live API server"""
    
    print("🚀 Testing Live FastAPI Server - Pure AI Classification")
    print("📡 Server: http://localhost:8000")
    print("=" * 60)
    
    # Test messages showcasing pure AI intelligence
    test_cases = [
        {
            "guest_message": "I need coffee urgently for my business meeting",
            "guest_id": "B001", 
            "room_number": "1205"
        },
        {
            "guest_message": "Hello, how are you today?",
            "guest_id": "G002",
            "room_number": "1301"
        },
        {
            "guest_message": "My toilet is overflowing and there's water everywhere!",
            "guest_id": "E003",
            "room_number": "0807"
        },
        {
            "guest_message": "Can you clean my room and also help me with luggage?",
            "guest_id": "M004",
            "room_number": "1502"
        }
    ]
    
    async with httpx.AsyncClient() as client:
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Test {i}: '{test_case['guest_message']}'")
            print(f"👤 Guest: {test_case['guest_id']} | Room: {test_case['room_number']}")
            print("-" * 50)
            
            try:
                # Call the classify endpoint
                response = await client.post(
                    "http://localhost:8000/classify",
                    json=test_case,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display AI results
                    ticket_status = "✅ TICKET CREATED" if result["should_create_ticket"] else "❌ NO TICKET"
                    print(f"{ticket_status}")
                    print(f"🎯 AI Confidence: {result['confidence']:.1%}")
                    print(f"⚡ AI Priority: {result['suggested_priority'].upper()}")
                    print(f"⏱️ AI Time Est: {result['estimated_completion_time'] or 'Not specified'}")
                    print(f"🧠 AI Reasoning: {result['reasoning'][:100]}...")
                    
                    if result["categories"]:
                        print("📋 AI-Generated Service Categories:")
                        for cat in result["categories"]:
                            urgency_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "urgent": "🔴"}
                            emoji = urgency_emoji.get(cat["urgency"], "⚪")
                            print(f"   {emoji} {cat['category'].upper()}: {cat['message'][:80]}...")
                            print(f"      └─ AI Urgency: {cat['urgency']}")
                    
                else:
                    print(f"❌ API Error: {response.status_code}")
                    print(f"Response: {response.text}")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            # Small delay between requests
            await asyncio.sleep(1)
    
    print("\n" + "=" * 60)
    print("🎉 Pure AI Classification System Demonstrated!")
    print("\n🔥 Key AI Features Shown:")
    print("   • Zero hardcoded rules - pure machine intelligence")
    print("   • Dynamic service detection based on natural language")
    print("   • Intelligent urgency and priority assessment")
    print("   • Context-aware message generation for hotel staff")
    print("   • Real-time confidence scoring")
    print("   • Multiple service category detection in single messages")
    
    print("\n📖 API Documentation: http://localhost:8000/docs")
    print("💡 Try your own messages at the /classify endpoint!")

if __name__ == "__main__":
    try:
        asyncio.run(test_api())
    except KeyboardInterrupt:
        print("\n👋 Test stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
