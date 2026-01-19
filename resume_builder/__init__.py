"""
Resume Builder Package.

This package provides functionality to generate tailored resumes using Claude AI.
It converts prompt text files into structured YAML format and generates professional
Word documents (.docx) with customizable formatting.

Main components:
- LLMResumeGenerator: AI-powered resume content generation using Claude
- Resume models: Pydantic models for structured resume data
- Document renderers: Section-specific rendering for Word documents
- CLI: Command-line interface for the resume builder

Usage:
    From command line:
        build-resume <prompt_file> <claude_api_key> <ai_model> --output-file resume.docx
"""
