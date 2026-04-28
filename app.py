from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import image_to_base64
from Leaf_Disease.main import LeafDiseaseDetector

try:
    app = FastAPI(title="Leaf Disease Detection API", version="1.0.0")
    detector = LeafDiseaseDetector()
except ValueError as e:
    raise RuntimeError(f"❌ Cannot start API: {str(e)}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/disease-detection")
async def detect_disease(file: UploadFile = File(...)):
    """Detect leaf disease from uploaded image using Groq API."""
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="❌ File must be an image")
        
        image_base64 = image_to_base64(file.file)
        result = detector.analyze_leaf(image_base64)
        
        return JSONResponse(content={
            "disease_detected": result.disease_detected,
            "disease_name": result.disease_name,
            "disease_type": result.disease_type,
            "severity": result.severity,
            "confidence": result.confidence,
            "symptoms": result.symptoms,
            "causes": result.causes,
            "treatment": result.treatment,
            "roman_urdu_explanation": result.roman_urdu_explanation,
            "timestamp": result.timestamp
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ {str(e)}")

@app.get("/health")
async def health_check():
    """API health check."""
    return {"status": "ok", "message": "API requires valid Groq API key"}
