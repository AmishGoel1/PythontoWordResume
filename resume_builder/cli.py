import argparse
from yaml_docx import *
from prompt_generator import *

def main():
    ai_model = 'claude-sonnet-4-5-20250929'

    parser = argparse.ArgumentParser(
        description="Generate tailored resumes using AI"
    )
    parser.add_argument("-p", '--prompt', type=str,default='prompt.txt', help="File path that contains the prompt as a txt file")
    parser.add_argument("-o", "--output", type=str, default='resume.docx', help="Filename for the newly generated docx file")
    args = parser.parse_args()

    try:
        with open(args.prompt, "r") as file:
            config_data = file.read()
        print("Successfully read prompt text file.")
    except FileNotFoundError:
        print("Prompt text file not found. Please make sure the file exists")
    except PermissionError:
        print("Permission denied when accessing the file. Please make sure you can access the file")
    except IOError as e:
        print(f"An I/O error occurred: {e}")

    resume_generator = LLMResumeGenerator(ai_model)
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

    main_section_margin = initialdoc.sections[0]
    main_section_margin.left_margin = Inches(0.5)
    main_section_margin.right_margin = Inches(0.5)
    main_section_margin.top_margin = Inches(0.437)
    main_section_margin.bottom_margin = Inches(0.287)

    nametext = paragraph_formatting(initialdoc, contact.name, formattingstyles['Name'])
    nametext.paragraph_format.space_after = 0

    linkspara = paragraph_formatting(initialdoc, f"{contact.email} | LinkedIn | GitHub", formattingstyles['Links'])

    for section in data['resume_sections']: # pyright: ignore[reportPossiblyUnboundVariable]
        heading = initialdoc.add_paragraph(section['type'])
        formattingstyles['SectionHeading'].apply(heading.runs[0])
        renderermap[section['type']].render(initialdoc, resume) # pyright: ignore[reportPossiblyUnboundVariable]

    initialdoc.save(args.output)

if __name__ == "__main__":
    main()