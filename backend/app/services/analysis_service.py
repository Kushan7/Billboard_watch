import time
import uuid
from pathlib import Path
from ultralytics import YOLO
from google.cloud import vision
from transformers import pipeline # Import the pipeline from transformers

# Load your custom fine-tuned model for billboard detection
model = YOLO('ml_models/best.pt')

# Load a pre-trained text classification model for content analysis
# This model is trained to detect toxic comments, which is a good fit for our use case.
# It will be downloaded automatically the first time it's run.
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

def run_violation_analysis(report_id: uuid.UUID, image_path: Path):
    """
    Runs the full AI/GIS analysis pipeline on a submitted report.
    """
    print("-" * 50)
    print(f"✅ BACKGROUND TASK STARTED: Analyzing report {report_id}")
    print(f"   Image to be processed: {image_path}")

    # Step 1: Billboard Detection (YOLOv8) is already implemented.
    try:
        results = model.predict(source=str(image_path), verbose=False)
        detected = any(model.names[int(c)] == 'billboard' for r in results for c in r.boxes.cls)
        if detected:
            print("   Step 1: [AI] Billboard detection... PASSED (Custom model found a billboard)")
        else:
            print("   Step 1: [AI] Billboard detection... FAILED (No billboard found)")
    except Exception as e:
        print(f"   Step 1: [AI] Billboard detection... ERROR: {e}")

    # Step 2: UPGRADED Text Violation Matching (BERT)
    try:
        detected_text = perform_ocr(image_path)
        if detected_text:
            print("   Step 2: [AI] OCR for license text... PASSED")
            
            # Use the BERT model to analyze the text
            results = text_classifier(detected_text)
            
            # The model returns a list of labels and scores. We'll check for high-confidence violations.
            violations_found = []
            for result in results:
                if result['label'] != 'clean' and result['score'] > 0.8: # High confidence threshold
                    violations_found.append(f"{result['label']} (score: {result['score']:.2f})")
            
            if violations_found:
                print(f"      > VIOLATION DETECTED: Text classified as: {violations_found}")
            else:
                print("      > No text violations found.")
        else:
            print("   Step 2: [AI] OCR for license text... FAILED (No text found)")
    except Exception as e:
        print(f"   Step 2: [AI] OCR for license text... ERROR: {e}")

    # Step 3: Zonal Compliance (GIS)
    time.sleep(1)
    print("   Step 3: [GIS] Checking for 'No Hoarding Zone'... (pending implementation)")

    print(f"✅ BACKGROUND TASK FINISHED: Analysis for report {report_id} complete.")
    print("-" * 50)