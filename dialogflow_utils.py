import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(BASE_DIR / "credentials.json")

from google.cloud import dialogflow


def detect_intent_texts(project_id: str, session_id: str, text: str, language_code: str = "ru"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text