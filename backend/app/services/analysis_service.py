import uuid
from pathlib import Path
from google.cloud import vision
from transformers import pipeline
import json
from shapely.geometry import shape, Point

# --- GIS CHECK SETUP ---
GIS_DATA_PATH = Path("gis_data/no_hoarding_zones.geojson")

def check_gis_violation(latitude: float, longitude: float) -> bool:
    """
    Checks if the given coordinates fall within a prohibited zone.
    """
    try:
        with open(GIS_DATA_PATH) as f:
            geojson_data = json.load(f)
        
        point = Point(longitude, latitude) # Note: GeoJSON is (lon, lat)

        for feature in geojson_data['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                return True # Violation found
        return False # No violation
    except Exception:
        # If file is not found or invalid, assume no violation
        return False

# Load the text classification model
text_classifier = pipeline('text-classification', model='unitary/toxic-bert')

def perform_ocr(image_path: Path) -> str:
    """Detects text in the image file using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else ""

# In services/analysis_service.py

# ... (keep all the imports and the model loading line) ...

def run_violation_analysis(report_id: uuid.UUID, image_path: Path, latitude: float, longitude: float):
    """
    Runs the full analysis pipeline on a submitted report.
    """
    print("-" * 50)
    print(f"✅ BACKGROUND TASK STARTED: Analyzing report {report_id}")

    # --- Step 1: Billboard Detection (YOLOv8) ---
    try:
        # Define all the classes we want to detect
        TARGET_CLASSES = {'billboard', 'tv'}
        
        results = model.predict(source=str(image_path), verbose=False)
        
        # Check if any of the target classes were detected
        detected = any(model.names[int(c)] in TARGET_CLASSES for r in results for c in r.boxes.cls)
        
        if detected:
            print(f"   Step 1: [AI] Billboard detection... PASSED (Found a target object)")
        else:
            print("   Step 1: [AI] Billboard detection... FAILED (No billboard or tv found)")
            
    except Exception as e:
        print(f"   Step 1: [AI] Billboard detection... ERROR: {e}")

    # --- Step 2 and 3 will remain the same ---
    # ... (rest of the file) ...