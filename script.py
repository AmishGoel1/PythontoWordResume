from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches
from docx.text.run import Run
from docx.text.paragraph import Paragraph
from pydantic import BaseModel
from typing import List
import yaml

with open('points.yaml', 'r') as f:
    data = yaml.safe_load(f)

class skillsclass(BaseModel):
    category: str
    skill: str

class workclass(BaseModel):
    Title: str
    Company: str
    Date: str
    Points: List[str]

class projectclass(BaseModel):
    Name: str
    Points: List[str]

class certificateclass(BaseModel):
    Name: str
    Issuer: str

class credentialclass(BaseModel):
    Name: str
    Points: List[str]

class educationclass(BaseModel):
    Name: str
    Credential: List[credentialclass]

class Resume(BaseModel):
    summary: str
    skills: List[skillsclass]
    education: List[educationclass]
    certificates: List[certificateclass]
    work: List[workclass]
    projects: List[projectclass]

resume = Resume.model_validate(data)
name = 'AMISH GOEL'
email = 'Jobs@lets.workwithamish.me'
linkedinLink = 'https://www.linkedin.com/in/amish-goyal-096066b4/'
github = 'https://github.com/AmishGoel1'

sections = ('Professional Summary', 'Core Skills', 'Work Experience', 'Education & Certificates', 'Projects')

doc = Document()

def formatting(pararun: Run, bold_or_not=True, font_size=Pt(12), font_name='Times New Roman'):
    pararun.font.name = font_name
    pararun.bold = bold_or_not
    pararun.font.size = font_size

def spacing(paragraph: Paragraph, space_before: Pt, space_after: Pt):
    paragraph.paragraph_format.space_after = space_after
    paragraph.paragraph_format.space_before = space_before

nametext = doc.add_paragraph('AMISH GOEL')
formatting(nametext.runs[0], font_size=Pt(18))
nametext.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
nametext.paragraph_format.space_after = Pt(0)

linkspara = doc.add_paragraph(f"{email} | LinkedIn | GitHub")
formatting(linkspara.runs[0], False, Pt(14))
linkspara.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

for section in sections:
    currentsection = doc.add_paragraph(f"{section}\n")
    formatting(currentsection.runs[0], True, Pt(13))
    spacing(currentsection, Pt(0), Pt(0))
    if section == 'Professional Summary':
        summarytext = doc.add_paragraph(f"{resume.summary}\n")
        formatting(summarytext.runs[0], False)     
        spacing(summarytext, Pt(0), Pt(0))
    
    elif section == 'Core Skills':
        for skill in resume.skills:
            currentpoint = doc.add_paragraph(f"{skill.category}: ")
            formatting(currentpoint.runs[0])
            for i, point in enumerate(skill.skill):
                if i == len(skill.skill) - 1:
                    valuerun = currentpoint.add_run(f"{point}")
                else:
                    valuerun = currentpoint.add_run(f"{point}, ")
                formatting(valuerun, False)
                currentpoint.paragraph_format.space_after = Pt(3)
        doc.add_paragraph()
    
    elif section == 'Education & Certificates':
        for university in resume.education:
                universityname = doc.add_paragraph(university.Name)
                formatting(universityname.runs[0], True)
                for credential in university.Credential:
                        credentialname = doc.add_paragraph(credential.Name)
                        credentialname.paragraph_format.space_after = Pt(0)
                        formatting(credentialname.runs[0], True)
                        for point in credential.Points:
                            currentpoint = doc.add_paragraph(point, style='List Bullet')
                            formatting(currentpoint.runs[0], False)
                            currentpoint.paragraph_format.space_after = Pt(0)
        doc.add_paragraph()
        for certificate in resume.certificates:
            certificatename = doc.add_paragraph(f"{certificate.Name}: {certificate.Issuer}", style='List Bullet')
            formatting(certificatename.runs[0], False)
            certificatename.paragraph_format.space_after = Pt(2)

    elif section == 'Work Experience':
        for work in resume.work:
            doc.add_paragraph(f"{work.Title}, {work.Company} {work.Date}")
            for point in work.Points:
                currentworkpoint = doc.add_paragraph(f"{point}", style='List Bullet')
                formatting(currentworkpoint.runs[0], False)
                currentworkpoint.paragraph_format.space_after = Pt(3)
            doc.add_paragraph()
    
    elif section == 'Projects':
        for project in resume.projects:
            projectname = doc.add_paragraph(project.Name)
            formatting(projectname.runs[0])
            if project.Name == 'Project 1 Name':
                projectname.paragraph_format.space_before = Pt(0)
            else: 
                projectname.paragraph_format.space_before = Pt(9)
            for point in project.Points:
                currentpoint = doc.add_paragraph(f"{point}", style='List Bullet')
                formatting(currentpoint.runs[0], False)
                spacing(currentpoint, Pt(15), Pt(3))

section = doc.sections[0]
section.left_margin = Inches(0.5)
section.right_margin = Inches(0.5)
section.top_margin = Inches(0.437)
section.bottom_margin = Inches(0.287)

doc.save('sapmle1.docx')

