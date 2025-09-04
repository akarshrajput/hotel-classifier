import httpx
import asyncio
import json
from typing import Dict, Any

class ServiceClassifierClient:
    """Client for interacting with the Hotel Service Request Classifier API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def classify_message(
        self,
        guest_message: str,
        guest_id: str = None,
        room_number: str = None
    ) -> Dict[str, Any]:
        """Classify a single guest message"""
        
        payload = {
            "guest_message": guest_message,
            "guest_id": guest_id,
            "room_number": room_number
        }
        
        response = await self.client.post(
            f"{self.base_url}/classify",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def get_insights(
        self,
        guest_message: str,
        guest_id: str = None,
        room_number: str = None
    ) -> Dict[str, Any]:
        """Get detailed insights about a guest message"""
        
        payload = {
            "guest_message": guest_message,
            "guest_id": guest_id,
            "room_number": room_number
        }
        
        response = await self.client.post(
            f"{self.base_url}/insights",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def batch_classify(
        self,
        messages: list[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Classify multiple messages in batch"""
        
        response = await self.client.post(
            f"{self.base_url}/batch-classify",
            json=messages
        )
        response.raise_for_status()
        return response.json()
    
    async def get_categories(self) -> Dict[str, Any]:
        """Get available service categories"""
        
        response = await self.client.get(f"{self.base_url}/categories")
        response.raise_for_status()
        return response.json()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        
        response = await self.client.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

# Demo usage
async def demo():
    """Demonstrate the API client"""
    
    client = ServiceClassifierClient()
    
    try:
        # Health check
        print("🏥 Health Check:")
        health = await client.health_check()
        print(json.dumps(health, indent=2))
        
        # Get categories
        print("\n📋 Available Categories:")
        categories = await client.get_categories()
        for category, description in categories["categories"].items():
            print(f"   • {category}: {description}")
        
        # Test classification
        test_messages = [
            {
                "message": "I need coffee and clean towels urgently",
                "guest_id": "G001",
                "room_number": "101"
            },
            {
                "message": "My TV is not working",
                "guest_id": "G002",
                "room_number": "102"
            },
            {
                "message": "Hello, how are you?",
                "guest_id": "G003",
                "room_number": "103"
            }
        ]
        
        print("\n🧪 Classification Tests:")
        for test in test_messages:
            print(f"\n📝 Message: '{test['message']}'")
            
            # Classify
            result = await client.classify_message(
                guest_message=test["message"],
                guest_id=test["guest_id"],
                room_number=test["room_number"]
            )
            
            print(f"✅ Ticket Required: {result['should_create_ticket']}")
            print(f"🔍 Confidence: {result['confidence']}")
            print(f"⚡ Priority: {result['suggested_priority']}")
            
            if result['categories']:
                print("📋 Categories:")
                for cat in result['categories']:
                    print(f"   • {cat['category']}: {cat['message']} (urgency: {cat['urgency']})")
            
            # Get insights
            try:
                insights = await client.get_insights(
                    guest_message=test["message"],
                    guest_id=test["guest_id"],
                    room_number=test["room_number"]
                )
                print(f"🧠 Insights: {json.dumps(insights, indent=2)}")
            except Exception as e:
                print(f"🚨 Insights error: {str(e)}")
            
            print("-" * 50)
        
        # Batch classification
        print("\n📦 Batch Classification:")
        batch_requests = [
            {"guest_message": msg["message"], "guest_id": msg["guest_id"], "room_number": msg["room_number"]}
            for msg in test_messages
        ]
        
        batch_result = await client.batch_classify(batch_requests)
        print(f"Total processed: {batch_result['total_processed']}")
        
    except httpx.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(demo())
