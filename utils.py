"""
    Utils class for necessary  utilization functions such as saving, loading chat sessions as json files.
"""

import json
from langchain.schema.messages import HumanMessage, AIMessage
from datetime import datetime


# To save current chat history in chat_session directory (or any desired one).
def save_chat_history_json(chat_history, file_path):
    with open(file_path, "w") as f :
        json_data = [message.dict() for message in chat_history]
        json.dump(json_data,f)


# To load chat history from chat_sessions directory (or any desired one).
def load_chat_history_json(file_path):
    with open(file_path, "r") as f :
        json_data = json.load(f)
        messages =  [HumanMessage(**message) if message["type"] == "human" else AIMessage(**message) for message in json_data]
        return messages


# To create a unique json file so we can get every single chat session.
# Extra Update Note for Future : Can be added a new llm model which can summarize the output with 1 sentence
# then create or rename our json file with it.
def get_timestamp():
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")