import re
import time
import json
from typing import List

import streamlit as st


markdown_template = """
##### 📌{title}

📰 *Source: {source}*

{content}

"""


def get_current_time():
    return time.strftime('%c')


def extract_title_and_source(log):
    regex = r"Thought\s*\d*\s*:(.*?)\nAction\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
    match = re.search(regex, log, re.DOTALL)
    action = match.group(2).strip()
    action_input = json.loads(match.group(3).strip())
    
    if action == "Browse website with question":
        title = action_input["question"]
        source = action_input["url"]
    elif action == "Google Search":
        title = action_input["input"]
        source = "Google"
    elif action == "Wikipedia with question":
        title = action_input["question"]
        source = f"Wikipedia-{action_input['input']}"
    elif action == "LLM Code":
        title = action_input["question"]
        source = "Code Language Model"
    else:
        raise NotImplementedError
    
    return title, source
    
        
def get_thoughts_from_intermediate_steps(intermediate_steps, save_to_file=True):
    thoughts = ""
    for action, observation in intermediate_steps:
        thoughts += action.log
        thoughts += f"\nObservation: {observation}"
    if save_to_file:
        try:
            title, source = extract_title_and_source(action.log)
            observation = observation.strip()
            text = markdown_template.format(title=title, content=observation, source=source)
            st.session_state.amazing_note += text
        except Exception as e:
            pass
    return thoughts


def convert_messages_to_conversation(messages: List[dict]) -> str:
    if len(messages) == 0:
        return "\n"
    else:
        conv_prompt = "\n\nPrevious chat history:\n{content}\n\n"
        content = ""
        for _, message in enumerate(messages):
            if message["role"] == "user":
                content += f"user: {message['content']}\n"
            elif message["role"] == "assistant":
                content += f"assistant: {message['content']}\n"
        
        return conv_prompt.format(content=content.strip())