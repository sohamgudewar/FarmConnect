from google import genai
from google.genai import types
import os
import base64
import json
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_client():
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not found in environment variables.")
        return None
    return genai.Client(api_key=GEMINI_API_KEY)

def analyze_crop_image(image_base64: str):
    """
    Uses the new google-genai library to analyze a crop image for diseases with fallback models.
    """
    client = get_client()
    if not client:
        return {"error": "Gemini API key not configured"}

    # List of models to try in order of preference
    models_to_try = [
        'gemini-2.5-flash',
        'gemini-2.5-flash-lite'
    ]

    try:
        # Decode base64 image (handle potential data URL prefix)
        if "," in image_base64:
            logger.info("Stripping data URL prefix from base64 string")
            image_base64 = image_base64.split(",")[1]
            
        image_bytes = base64.b64decode(image_base64)
        
        # In the new SDK, we can pass bytes directly via types.Part
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/jpeg" # Defaulting to jpeg, but genai is usually smart
        )

        prompt = """
        Analyze this agricultural image. Act as an expert plant pathologist.
        Identify:
        1. The crop name.
        2. Whether it is healthy or diseased.
        3. If diseased, provide the disease name, a brief description, and a recommended remedy.
        4. Your confidence level as a percentage (0-1).

        Return the response ONLY as a JSON object with these keys:
        {
            "crop_name": "string",
            "is_healthy": boolean,
            "disease_name": "string or 'None'",
            "description": "string",
            "remedy": "string or 'None'",
            "confidence": float
        }
        """

        last_error = None
        for model_id in models_to_try:
            try:
                logger.info(f"Attempting analysis with model: {model_id}")
                
                response = client.models.generate_content(
                    model=model_id,
                    contents=[prompt, image_part],
                    config=types.GenerateContentConfig(
                        temperature=0.4,
                        top_p=1.0,
                        max_output_tokens=2048,
                        response_mime_type="application/json" # New feature: forced JSON output
                    )
                )
                
                # The new SDK might return a parsed object if response_mime_type is set
                # or we can extract it from the text
                if response.text:
                    return json.loads(response.text.strip())
                elif response.parsed:
                    return response.parsed
                else:
                    raise Exception("No text or parsed content in Gemini response")
                
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Error with model {model_id}: {last_error}")
                if "429" in last_error or "quota" in last_error.lower():
                    continue
                elif "404" in last_error or "not found" in last_error.lower():
                    continue
                else:
                    # For other errors, still try next model
                    continue

        return {"error": f"All Gemini models failed. Last error: {last_error}"}

    except Exception as e:
        logger.error(f"Error in Gemini analysis pipeline: {e}", exc_info=True)
        return {"error": str(e)}
