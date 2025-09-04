import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from models import ClassificationRequest, ClassificationResponse, HealthResponse
from classifier import IntelligentServiceClassifier

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global classifier instance
classifier = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global classifier
    try:
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is required")
        
        model_name = os.getenv("MODEL_NAME", "mistral-large-latest")
        classifier = IntelligentServiceClassifier(api_key=api_key, model_name=model_name)
        logger.info("Intelligent Service Classifier initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize classifier: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Application shutting down")

# Create FastAPI app
app = FastAPI(
    title="Intelligent Hotel Service Request Classifier",
    description="AI-powered system to classify and prioritize hotel guest service requests",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_classifier():
    """Dependency to get the classifier instance"""
    if classifier is None:
        raise HTTPException(status_code=503, detail="Classifier not initialized")
    return classifier

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    model_status = "healthy" if classifier is not None else "unavailable"
    return HealthResponse(
        status="healthy",
        model_status=model_status,
        timestamp=datetime.now().isoformat()
    )

@app.post("/classify", response_model=ClassificationResponse)
async def classify_service_request(
    request: ClassificationRequest,
    classifier_instance: IntelligentServiceClassifier = Depends(get_classifier)
):
    """
    Classify a guest service request message
    
    This endpoint uses advanced AI to:
    - Determine if a ticket should be created using pure AI analysis
    - Identify service categories dynamically  
    - Generate specific messages for each category using AI intelligence
    - Assess urgency and priority through natural language understanding
    - Estimate completion times using AI reasoning
    - Provide insights with zero hardcoded rules
    """
    try:
        logger.info(f"Classifying message: {request.guest_message[:100]}...")
        
        result = await classifier_instance.classify_message(
            guest_message=request.guest_message,
            guest_id=request.guest_id,
            room_number=request.room_number
        )
        
        logger.info(f"Classification result: ticket={result.should_create_ticket}, "
                   f"categories={len(result.categories)}, confidence={result.confidence}")
        
        return result
        
    except Exception as e:
        logger.error(f"Classification failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.post("/insights")
async def get_service_insights(
    request: ClassificationRequest,
    classifier_instance: IntelligentServiceClassifier = Depends(get_classifier)
):
    """
    Get detailed insights about a guest message
    
    Provides additional context including:
    - Sentiment analysis
    - Emotion detection
    - Guest type identification
    - Implicit needs analysis
    """
    try:
        insights = await classifier_instance.get_service_insights(request.guest_message)
        return insights
        
    except Exception as e:
        logger.error(f"Insights generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

@app.get("/categories")
async def get_service_categories():
    """Get all available service categories with descriptions"""
    if classifier is None:
        raise HTTPException(status_code=503, detail="Classifier not initialized")
    
    return {
        "categories": classifier.service_definitions,
        "description": "Available service categories for classification"
    }

@app.post("/batch-classify")
async def batch_classify_requests(
    requests: list[ClassificationRequest],
    background_tasks: BackgroundTasks,
    classifier_instance: IntelligentServiceClassifier = Depends(get_classifier)
):
    """
    Classify multiple service requests in batch
    
    Useful for processing multiple guest messages simultaneously
    """
    try:
        results = []
        for req in requests:
            result = await classifier_instance.classify_message(
                guest_message=req.guest_message,
                guest_id=req.guest_id,
                room_number=req.room_number
            )
            results.append(result)
        
        return {"results": results, "total_processed": len(results)}
        
    except Exception as e:
        logger.error(f"Batch classification failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch classification failed: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment (Render sets PORT automatically)
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    environment = os.getenv("ENVIRONMENT", "development")
    
    logger.info(f"Starting server on {host}:{port} in {environment} mode")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug and environment == "development",
        log_level="info"
    )
