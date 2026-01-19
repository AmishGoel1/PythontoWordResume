"""
Resume Generation Module using Claude AI.

This module provides functionality to generate structured resume content using
Anthropic's Claude AI API. It converts text prompts containing resume information
and job descriptions into YAML-formatted resume data.

Classes:
    LLMResumeGenerator: Main class for interfacing with Claude AI to generate resumes.

Dependencies:
    - anthropic: For Claude AI API integration
    - yaml: For YAML parsing and serialization
"""
# import os
from dataclasses import dataclass

import yaml
from anthropic import Anthropic, APIConnectionError, APIStatusError

# from dotenv import find_dotenv, load_dotenv

# load_dotenv('../.env')
# def get_env_variable(key, default=None):
#     """
#     Checks if .env file exists and if the key is present.
#     Returns the value if found, otherwise returns a default.
#     """
#     env_file = find_dotenv()
#     if not env_file:
#         print("Warning: .env file not found.")
#         return default

#     # Load the variables from the discovered .env file
#     load_dotenv(env_file)

#     # Check for existence of the key within os.environ
#     if key in os.environ:
#         return os.getenv(key)
    
#     print(f"Warning: Key '{key}' not found in the environment.")
#     return default

# api_key = get_env_variable(key='API_KEY')

@dataclass
class LLMResumeGenerator: 
    """
    Generate tailored resume using Claude AI.
    
    This class interfaces with Anthropic's Claude API to generate structured
    resume content from text prompts. It takes a prompt containing resume
    information and job requirements, then returns a YAML-formatted resume.
    
    Attributes:
        llmmodel: The name of the Claude AI model to use (e.g., 'claude-sonnet-4-20250514').
        claude_api_key: API key for authenticating with Anthropic's Claude API.
    """
    llmmodel: str
    claude_api_key: str = ''
   
    
    
    def generate_yaml_from_prompt(self, prompt_text: str):
        """
        Generate YAML-formatted resume content from a text prompt using Claude AI.
        
        This method sends the prompt to Claude AI, which analyzes the content and
        generates a structured resume in YAML format. The method extracts the YAML
        content from the API response by removing markdown code block markers.
        
        Args:
            prompt_text: Text prompt containing resume information and job description.
                        Should include all details needed to generate a complete resume.
        
        Returns:
            dict: Parsed YAML content as a Python dictionary containing resume structure.
        
        Raises:
            APIStatusError: If the API returns an error status code (e.g., invalid key, rate limit).
            APIConnectionError: If there's a network connection issue with the API.
            ValueError: If the response contains invalid YAML that cannot be parsed.
        
        Note:
            The method expects the Claude API response to wrap YAML content in markdown
            code blocks (```yaml...```). It strips the first 7 and last 4 characters to
            remove these markers before parsing.
        """
        client = Anthropic(api_key = self.claude_api_key) # pyright: ignore[reportUnboundVariable]
        try: 
            message = client.messages.create(
                max_tokens= 3096, 
                messages=[{'role': 'user', 'content': f"{prompt_text}"}], 
                model= self.llmmodel
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

    def save_yaml_to_file(self, file, yaml_text):
        """
        Save YAML content to a file.
        
        Writes the provided YAML data to a file without sorting keys, preserving
        the original order of fields in the YAML structure.
        
        Args:
            file: Path to the file where YAML content should be saved.
            yaml_text: YAML data (typically a dictionary) to be written to the file.
        
        Note:
            The method uses sort_keys=False to maintain the original order of
            dictionary keys in the output file.
        """
        with open(file, 'w') as f:
            yaml.dump(yaml_text, f, sort_keys=False)