import argparse
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


def fetch_questions(url):
    response = requests.get(url)
    response.raise_for_status()
    questions = response.json()
    return questions


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, 
        training_phrases=training_phrases, 
        messages=[message]
    )

    response = intents_client.create_intent(
        request={
            "parent": parent, 
            "intent": intent
        }
    )

    return response


def main():
    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(BASE_DIR / ".env")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(BASE_DIR / "credentials.json")

    parser = argparse.ArgumentParser(description="Создание интентов")
    parser.add_argument(
        "url",
        nargs="?",
        default="https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json",
        help="Путь к файлу с вопросами",
    )
    args = parser.parse_args() 

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    questions_data = fetch_questions(args.url)

    for display_name, info in questions_data.items():
        response = create_intent(
            project_id=project_id,
            display_name=display_name,
            training_phrases_parts=info["questions"],
            message_texts=[info["answer"]],
        )
        print("Intent created: {}".format(response))


if __name__ == '__main__':
    main()