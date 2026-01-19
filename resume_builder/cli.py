from .prompt_generator import LLMResumeGenerator
import yaml
from docx import Document as doc
from docx.shared import Inches
from pathlib import Path
import typer
from typing import Annotated
from .yaml_docx import (
    Resume,
    ContactInfo,
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
