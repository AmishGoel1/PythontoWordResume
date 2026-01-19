# Resume Builder

An AI-powered resume builder that uses Claude AI to generate tailored resumes from YAML configurations and outputs professional Word documents (.docx).

## Features

- **AI-Powered Generation**: Uses Claude AI to tailor your resume to specific job descriptions
- **YAML Configuration**: Define your resume structure in a clean, readable YAML format
- **Word Document Output**: Generates professionally formatted .docx files
- **Customizable Sections**: Support for:
  - Professional Summary
  - Skills (categorized)
  - Work Experience
  - Education & Credentials
  - Certificates
  - Projects
- **Command Line Interface**: Easy-to-use CLI built with Typer

## Requirements

- Python 3.10 or higher (< 4.0)
- Claude API key from [Anthropic](https://www.anthropic.com/)

## Installation

1. Clone the repository:

   ```bash
      git clone https://github.com/AmishGoel1/PythontoWordResume.git
      cd PythontoWordResume
   ```

2. Set up the virtual environment and install dependencies:

   ```bash
   source activate.sh
   ```

   Or manually:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

## Usage

### Basic Usage

Run the resume builder with your prompt file and Claude API credentials:

```bash

build-resume <prompt_file> <claude_api_key> <ai_model> --output-file resume.docx

```

### Arguments

| Argument        | Description                                                                         |
|-----------------|-------------------------------------------------------------------------------------|
| `prompt_file`   | Path to the prompt text file containing your resume information and job description |
| `claude_api_key`| Your Claude API key (can also be set via `claude_api_key` environment variable)     |
| `ai_model`      | Claude model name (e.g., `claude-sonnet-4-20250514`)                                |

### Options

| Option           | Default      | Description                       |
|------------------|--------------|-----------------------------------|
| `--output-file`  | `resume.docx`| Name of the generated resume file |

### Example

```bash
build-resume resume_builder/templates/prompt.txt $CLAUDE_API_KEY claude-sonnet-4-20250514 --output-file my_resume.docx
```

## Project Structure

```console
PythontoWordResume/
├── resume_builder/
│   ├── __init__.py
│   ├── cli.py                 # Command line interface
│   ├── prompt_generator.py    # Claude AI integration
│   ├── yaml_docx.py           # YAML parsing and docx generation
│   └── templates/
│       ├── prompt.txt         # Example prompt template
│       └── points.yaml        # Example YAML schema
├── activate.sh                # Virtual environment setup script
├── pyproject.toml             # Project configuration and dependencies
├── LICENSE                    # GNU GPL v3 License
└── README.md
```

## How It Works

1. **Input**: Provide a prompt file containing your current resume and the target job description
2. **AI Processing**: Claude AI analyzes your resume and tailors it to match the job requirements
3. **YAML Generation**: The AI outputs a structured YAML file with your resume content
4. **Document Creation**: The tool parses the YAML and generates a professionally formatted Word document

## Prompt Template

The prompt file should include:

- Your current resume in text format
- The job description you're targeting
- The tool will automatically format it using the YAML schema defined in `templates/points.yaml`

See `resume_builder/templates/prompt.txt` for a complete example.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Author

**Amish Goel** - [GitHub](https://github.com/AmishGoel1)

## Acknowledgments

- [python-docx](https://python-docx.readthedocs.io/) for Word document generation
- [Typer](https://typer.tiangolo.com/) for the CLI framework
- [Anthropic Claude](https://www.anthropic.com/) for AI capabilities
- [Pydantic](https://docs.pydantic.dev/) for data validation
