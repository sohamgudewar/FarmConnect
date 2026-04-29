import logging
from sqlalchemy.orm import Session
from backend.services.weather_service import get_weather_data
from backend.models.market_price import MarketPrice
from backend.services.analysis_service import get_client
from google.genai import types
import json

logger = logging.getLogger(__name__)


def generate_market_advisory(db: Session, commodity: str, city: str, district: str = None):
    """
    Combines market price trends and weather data to provide farmer advisory.
    """
    # 1. Fetch Price Data
    # Get latest price for this commodity in the district (or anywhere in MH as fallback)
    price_query = db.query(MarketPrice).filter(MarketPrice.commodity.ilike(f"%{commodity}%"))
    if district:
        price_query = price_query.filter(MarketPrice.district.ilike(f"%{district}%"))

    latest_price_record = price_query.order_by(MarketPrice.updated_at.desc()).first()

    current_price = latest_price_record.modal_price if latest_price_record else None

    # Simple trend logic (in a real app, we'd compare with previous records)
    # For now, let's assume "Stable" or use dummy comparison if multiple records exist
    price_trend = "Stable"

    # 2. Fetch Weather Data
    weather_data = get_weather_data(city)
    if not weather_data:
        weather_summary = "Weather data unavailable."
        alerts = []
    else:
        weather_summary = f"{weather_data['current']['temp']}°C, {weather_data['current']['description']}"
        alerts = weather_data.get("alerts", [])

    # 3. Generate Advisory using Gemini
    client = get_client()
    advisory_text = "Advisory could not be generated at this time."

    if client:
        try:
            prompt = f"""
            As an expert agricultural consultant, provide a brief advice to a farmer based on the following:
            - Commodity: {commodity}
            - Current Market Price: {current_price if current_price else 'Unknown'}
            - Price Trend: {price_trend}
            - Weather Forecast: {weather_summary}
            - Weather Alerts: {', '.join(alerts) if alerts else 'None'}

            Provide advice in 2-3 sentences regarding whether they should harvest, wait, or take precautions.
            Be specific and helpful.
            """

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=500,
                )
            )
            if response.text:
                advisory_text = response.text.strip()
        except Exception as e:
            logger.error(f"Error generating advisory with Gemini: {e}")
            advisory_text = f"Consultant is busy. Basic logic: {'Watch for rain!' if 'rain' in weather_summary.lower() else 'Conditions are normal.'}"

    return {
        "commodity": commodity,
        "city": city,
        "current_price": current_price,
        "price_trend": price_trend,
        "weather_summary": weather_summary,
        "advisory": advisory_text,
        "alerts": alerts
    }
