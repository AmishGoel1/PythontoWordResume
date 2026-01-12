import os
from dataclasses import dataclass

import yaml
from anthropic import Anthropic, APIConnectionError, APIStatusError
from dotenv import find_dotenv, load_dotenv

load_dotenv('../.env')
def get_env_variable(key, default=None):
    """
    Checks if .env file exists and if the key is present.
    Returns the value if found, otherwise returns a default.
    """
    env_file = find_dotenv()
    if not env_file:
        print("Warning: .env file not found.")
        return default

    # Load the variables from the discovered .env file
    load_dotenv(env_file)

    # Check for existence of the key within os.environ
    if key in os.environ:
        return os.getenv(key)
    
    print(f"Warning: Key '{key}' not found in the environment.")
    return default

api_key = get_env_variable(key='API_KEY')

@dataclass
class LLMResumeGenerator: 
    """Generate tailored resume using Claude AI"""
    llmmodel: str
    client: Anthropic = Anthropic(api_key=api_key)
   
    def generate_yaml_from_prompt(self, prompt_text: str):
        try: 
            message = self.client.messages.create(
                max_tokens= 3096, 
                messages=[{'role': 'user', 'content': f"{prompt_text}"}], 
                model= self.llmmodel
            )
        except APIStatusError as e:
            print(f"API Error ({e.status_code}): {e.message}")
        except APIConnectionError:
            print("Network error. Check your connection.")

        try: 
            yaml_content = message.content[0].text[7:-4] # pyright: ignore[reportAttributeAccessIssue, reportPossiblyUnboundVariable]
            print(yaml.dump(yaml_content))
            return yaml.safe_load(yaml_content) 
        except yaml.YAMLError as e:
            raise ValueError(print(e))

    def save_yaml_to_file(self, file, yaml_text):
        with open(file, 'w') as f:
            yaml.dump(yaml_text, f, sort_keys=False)