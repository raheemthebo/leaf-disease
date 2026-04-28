import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional

from groq import Groq
from .config import GROQ_API_KEY, MODEL


@dataclass
class DiseaseAnalysisResult:
    disease_detected: bool
    disease_name: str
    disease_type: str
    severity: str
    confidence: int

    disease_details: Dict
    symptoms: List[str]
    causes: List[str]

    treatment_plan: Dict
    local_recommendations_sindh: List[str]

    roman_urdu_explanation: str
    timestamp: str


class LeafDiseaseDetector:
    """Production-ready Leaf Disease Detection using Groq API"""

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY is required. Add it to your .env file.")

        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = MODEL

    def _extract_json(self, text: str) -> dict:
        """Extract valid JSON from LLM response safely"""
        if not text:
            raise ValueError("❌ Empty response from Groq API")

        # Try direct parse first
        try:
            return json.loads(text)
        except:
            pass

        # Extract JSON using regex
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError(f"❌ No JSON found in response:\n{text}")

        json_str = match.group()

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ JSON parsing failed: {str(e)}\nRaw:\n{text}")

    def analyze_leaf(self, image_base64: str) -> DiseaseAnalysisResult:
        """Analyze leaf image using Groq Vision API"""

        if not image_base64 or not image_base64.strip():
            raise ValueError("❌ Invalid image data provided")

        prompt = """You are an expert agricultural scientist specializing in plant diseases in South Asia, especially Pakistan (Sindh region).

CRITICAL INSTRUCTION: Perform a strict, detailed visual inspection of the leaf. Differentiate precisely between similar diseases by looking at the color, shape, borders, and distribution of spots/lesions. DO NOT provide generic or repetitive answers. Your diagnosis and confidence score MUST accurately reflect the unique visual symptoms in THIS specific image.

First, check if the image contains a plant leaf. If not, return invalid_image format.

If it is a valid leaf, analyze deeply and return JSON in the following format:

{
    "disease_detected": true/false,
    "disease_name": "disease name or Healthy",
    "disease_type": "fungal|bacterial|viral|pest|nutrient_deficiency|healthy",
    "severity": "none|mild|moderate|severe",
    "confidence": 0-100,

    "disease_details": {
        "introduction": "Explain what this disease is",
        "how_it_spreads": "Explain causes and spread",
        "impact_on_plant": "Explain damage to plant"
    },

    "symptoms": ["clear visible symptoms"],
    "causes": ["realistic causes"],

    "treatment_plan": {
        "immediate_actions": ["what farmer should do"],
        "chemical_treatment": ["Mancozeb, Copper Oxychloride, Imidacloprid"],
        "fertilizer_suggestions": ["urea, potash, DAP"],
        "organic_solutions": ["Neem oil etc"]
    },

    "local_recommendations_sindh": ["Sindh-specific advice"],

    "roman_urdu_explanation": "2 paragraphs Roman Urdu explanation"
}

Rules:
- Be practical and farmer-friendly
- Use Pakistan-available fertilizers (urea, potash, DAP)
- Keep response realistic

Return ONLY valid JSON.
No markdown, no explanation, no extra text.
Start with { and end with }.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=1800,
                temperature=0.6,
            )

            result_text = response.choices[0].message.content.strip()

            # Debug (optional)
            # print("RAW RESPONSE:\n", result_text)

            result_json = self._extract_json(result_text)

            return DiseaseAnalysisResult(
                disease_detected=bool(result_json.get("disease_detected", False)),
                disease_name=result_json.get("disease_name", "Unknown"),
                disease_type=result_json.get("disease_type", "unknown"),
                severity=result_json.get("severity", "unknown"),
                confidence=int(result_json.get("confidence", 0)),

                disease_details=result_json.get("disease_details", {}),
                symptoms=result_json.get("symptoms", []),
                causes=result_json.get("causes", []),

                treatment_plan=result_json.get("treatment_plan", {}),
                local_recommendations_sindh=result_json.get("local_recommendations_sindh", []),

                roman_urdu_explanation=result_json.get(
                    "roman_urdu_explanation",
                    "Roman Urdu explanation available nahi hai."
                ),

                timestamp=datetime.utcnow().isoformat() + "Z"
            )

        except Exception as e:
            raise Exception(f"❌ Groq API analysis failed: {str(e)}")