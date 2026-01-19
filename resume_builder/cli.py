"""
Command Line Interface for Resume Builder.

This module provides a command-line interface using Typer for generating
tailored resumes from text prompts. It orchestrates the complete workflow:
1. Reading the prompt text file
2. Generating YAML resume content via Claude AI
3. Parsing the YAML data
4. Creating a formatted Word document

The CLI requires a prompt file, Claude API key, and AI model specification
as arguments, with an optional output filename.

Usage:
    build-resume <prompt_file> <claude_api_key> <ai_model> --output-file resume.docx
"""
from pathlib import Path
from typing import Annotated

import typer
import yaml
from docx import Document as doc
from docx.shared import Inches

from .prompt_generator import LLMResumeGenerator
from .yaml_docx import (
    ContactInfo,
    Resume,
    # contact,
    formattingstyles,
    paragraph_formatting,
    renderermap,
)

app = typer.Typer()

@app.command()
def main(
    prompt_file: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True, 
            readable=True,
            help='Path to the prompt text file [Required]'
        )
    ],
    claude_api_key: Annotated[str, typer.Argument(
        min=100,
        envvar="claude_api_key",
        help='API key generated from claude account'
    )],

    ai_model: Annotated[str, typer.Argument(
        min=13,
        help="Type in the name of a Claude's API model - See this link for all models - https://platform.claude.com/docs/en/about-claude/models/overview"
    )],
    output_file: Annotated[str, typer.Option(help='Resume name of newly generated resume file')] = 'resume.docx' 
):
    """
    Generate a tailored resume from a text prompt using Claude AI.
    
    This command orchestrates the complete resume generation workflow:
    1. Reads the input prompt file containing resume info and job description
    2. Sends the prompt to Claude AI to generate structured YAML content
    3. Saves the YAML to 'points.yaml' file
    4. Parses the YAML data into resume models
    5. Creates a formatted Word document with professional styling
    
    Args:
        prompt_file: Path to a text file containing resume information and target job description.
                    The prompt guides Claude AI in tailoring the resume content.
        claude_api_key: API key for authenticating with Anthropic's Claude API.
                       Can also be set via claude_api_key environment variable.
        ai_model: Name of the Claude AI model to use (e.g., 'claude-sonnet-4-20250514').
                 Must be at least 13 characters. See Claude documentation for available models.
        output_file: Name of the output Word document file (default: 'resume.docx').
    
    Raises:
        FileNotFoundError: If the prompt file doesn't exist.
        PermissionError: If there are permission issues accessing files.
        IOError: If any I/O operation fails during file reading/writing.
    
    Note:
        The function uses placeholder URLs for GitHub and LinkedIn in the contact info.
        These should be customized based on actual data in future versions.
    """
    

    try:
        with open(prompt_file, "r") as file:
            config_data = file.read()
        print("Successfully read prompt text file.")
    except FileNotFoundError:
        print("Prompt text file not found. Please make sure the file exists")
    except PermissionError:
        print("Permission denied when accessing the file. Please make sure you can access the file")
    except IOError as e:
        print(f"An I/O error occurred: {e}")

    resume_generator = LLMResumeGenerator(ai_model, claude_api_key)
    yaml_content = resume_generator.generate_yaml_from_prompt(prompt_text=config_data) # pyright: ignore[reportPossiblyUnboundVariable]
    resume_generator.save_yaml_to_file('points.yaml', yaml_content)

    try:
        with open('points.yaml', "r") as file:
            data = yaml.safe_load(file)
        print("Successfully read yaml file.")
    except FileNotFoundError:
        print("Points yaml file not found. Please make sure the file exists")
    except PermissionError:
        print("Permission denied when accessing the file. Please make sure you can access the file")
    except IOError as e:
        print(f"An I/O error occured {e}")

    resume = Resume.model_validate(data['resume'][0]) # pyright: ignore[reportPossiblyUnboundVariable]

    initialdoc = doc()

    contact = ContactInfo(
        name = data['personal_details'][0]['name'], # pyright: ignore[reportPossiblyUnboundVariable]
        email= data['personal_details'][0]['email'], # pyright: ignore[reportPossiblyUnboundVariable]
        github = "https://google.com", # pyright: ignore[reportArgumentType]
        linkedin = "https://google.com" # pyright: ignore[reportArgumentType]
    )

    main_section_margin = initialdoc.sections[0]
    main_section_margin.left_margin = Inches(0.5)
    main_section_margin.right_margin = Inches(0.5)
    main_section_margin.top_margin = Inches(0.437)
    main_section_margin.bottom_margin = Inches(0.287)

    nametext = paragraph_formatting(initialdoc, contact.name, formattingstyles['Name'])
    nametext.paragraph_format.space_after = 0

    paragraph_formatting(initialdoc, f"{contact.email} | LinkedIn | GitHub", formattingstyles['Links'])

    for section in data['resume_sections']: # pyright: ignore[reportPossiblyUnboundVariable]
        heading = initialdoc.add_paragraph(section['type'])
        formattingstyles['SectionHeading'].apply(heading.runs[0])
        renderermap[section['type']].render(initialdoc, resume) # pyright: ignore[reportPossiblyUnboundVariable]

    initialdoc.save(output_file)

if __name__ == "__main__":
    app()
