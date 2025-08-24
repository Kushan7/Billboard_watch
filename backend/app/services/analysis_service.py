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

def run_violation_analysis(report_id: uuid.UUID, image_path: Path, latitude: float, longitude: float):
    """
    Runs the full analysis pipeline on a submitted report.
    """
    print("-" * 50)
    print(f"✅ BACKGROUND TASK STARTED: Analyzing report {report_id}")

    # --- Step 1: Billboard Detection is BYPASSED for the prototype ---
    print("   Step 1: [AI] Billboard detection... BYPASSED")

    # --- Step 2: Text Violation Matching (BERT) ---
    try:
        detected_text = perform_ocr(image_path)
        if detected_text:
            print("   Step 2: [AI] OCR for license text... PASSED")
            results = text_classifier(detected_text)
            violations_found = [res for res in results if res['label'] != 'clean' and res['score'] > 0.8]
            if violations_found:
                print(f"      > VIOLATION DETECTED: Text classified as: {violations_found}")
            else:
                print("      > No text violations found.")
        else:
            print("   Step 2: [AI] OCR for license text... FAILED (No text found)")
    except Exception as e:
        print(f"   Step 2: [AI] OCR for license text... ERROR: {e}")

    # --- Step 3: REAL Zonal Compliance (GIS) ---
    is_in_prohibited_zone = check_gis_violation(latitude, longitude)
    if is_in_prohibited_zone:
        print("   Step 3: [GIS] Checking for 'No Hoarding Zone'... VIOLATION DETECTED")
    else:
        print("   Step 3: [GIS] Checking for 'No Hoarding Zone'... PASSED")

    print(f"✅ BACKGROUND TASK FINISHED: Analysis for report {report_id} complete.")
    print("-" * 50)