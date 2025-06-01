from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from Topic_extractor.extractor import TopicExtractor # Make sure this import path is correct
import tempfile
import os
import logging

# Configure logging for better error visibility
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# NEW: This is the route that will respond when you just visit the base URL (e.g., http://127.0.0.1:9100/)
@app.get("/")
async def read_root():
    """
    Provides a welcome message and directs users to the API documentation.
    """
    return {"message": "Welcome to the Topic Extractor API! Go to /docs for interactive documentation."}

@app.post("/extract-topics/")
async def extract_topics_api(
    file: UploadFile = File(..., description="The document file (e.g., .docx) to extract topics from."),
    num_topics: int = Form(10, ge=1, description="The number of topics to extract. Must be at least 1.")
):
    """
    Extracts a specified number of topics from an uploaded document file.

    Args:
        file (UploadFile): The uploaded document file (e.g., .docx).
        num_topics (int): The desired number of topics to extract.

    Returns:
        dict: A dictionary containing the extracted topics as a list of formatted strings.
    """
    tmp_path = None # Initialize tmp_path to None
    try:
        # Create a temporary file to store the uploaded content
        # Using delete=False initially, so we can explicitly control deletion
        # The suffix helps ensure the file is treated as a docx
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            contents = await file.read() # Read the content of the uploaded file
            tmp.write(contents)          # Write content to the temporary file
            tmp_path = tmp.name          # Store the path for later deletion

        logger.info(f"Temporary file created at: {tmp_path}")

        # Initialize and run the topic extractor
        # IMPORTANT: Ensure your TopicExtractor class is correctly implemented
        # and can handle the document path provided.
        extractor = TopicExtractor(tmp_path, num_topics)
        topics = extractor.run_pipeline()

        # Format the extracted topics for the response
        formatted = [f"{i+1}) {t}" for i, t in enumerate(topics)]

        logger.info(f"Successfully extracted {len(topics)} topics from {file.filename}")
        return {"topics": formatted}

    except Exception as e:
        # Catch any exception that occurs during the process
        logger.error(f"An error occurred during topic extraction for {file.filename}: {e}", exc_info=True)
        # Raise an HTTPException to send a proper error response to the client
        raise HTTPException(status_code=500, detail=f"Failed to extract topics: {e}")
    finally:
        # Ensure the temporary file is deleted, even if an error occurred
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
                logger.info(f"Temporary file deleted: {tmp_path}")
            except OSError as e:
                logger.error(f"Error deleting temporary file {tmp_path}: {e}")