from dataclasses import dataclass
import yaml
from anthropic import Anthropic, APIConnectionError, APIStatusError

def save_yaml_to_file(file, yaml_text):
    with open(file, 'w') as f:
        yaml.dump(yaml_text, f, sort_keys=False)


@dataclass
class LLMResumeGenerator: 
    """Generate tailored resume using Claude AI"""
    model: str
    claude_api_key: str = ''
    
    def generate_yaml_from_prompt(self, prompt_text: str):
        client = Anthropic(api_key = self.claude_api_key) # pyright: ignore[reportUnboundVariable]
        try: 
            message = client.messages.create(
                max_tokens= 3096, 
                messages=[{'role': 'user', 'content': f"{prompt_text}"}],
                model= self.model
            )
            yaml_content = message.content[0].text[7:-4] # pyright: ignore[reportAttributeAccessIssue, reportPossiblyUnboundVariable]
            print(yaml.dump(yaml_content))
            return yaml.safe_load(yaml_content) 
        except APIStatusError as e:
            print(f"API Error ({e.status_code}): {e.message}")
        except APIConnectionError:
            print("Network error. Check your connection.")
        except yaml.YAMLError as e:
            raise ValueError(e)
