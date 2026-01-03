from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
import yaml

with open('points.yaml', 'r') as f:
    data = yaml.safe_load(f)

name = 'AMISH GOEL'
email = 'Jobs@lets.workwithamish.me'
linkedinLink = 'https://www.linkedin.com/in/amish-goyal-096066b4/'
github = 'https://github.com/AmishGoel1'

sections = ('Professional Summary', 'Core Skills', 'Work Experience', 'Education & Certificates', 'Projects')

doc = Document()

nametext = doc.add_paragraph('AMISH GOEL')
nametextrun = nametext.runs[0]
nametextrun.font.name = 'Times New Roman'
nametextrun.bold = True
nametextrun.font.size = Pt(18)
nametext.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

linkspara = doc.add_paragraph(f"{email} | LinkedIn | GitHub")
linkspara.runs[0].font.name = 'Times New Roman'
linkspara.runs[0].font.size = Pt(14)
linkspara.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

for section in sections:
    currentsection = doc.add_paragraph(section)
    currentrun = currentsection.runs[0]
    currentrun.font.name = 'Times New Roman'
    currentrun.font.size = Pt(13)

    if section == 'Professional Summary':
        summarytext = doc.add_paragraph(f"\n{data['summary']}")
        summarytext.runs[0].font.size = Pt(12)
        summarytext.runs[0].font.name = 'Times New Roman'
    
    elif section == 'Core Skills':
        for skill in data['skills']:
           for key, value in skill.items():
                doc.add_paragraph(f"{key}: {value}", style='List Bullet')
    
    elif section == 'Work Experience':
        for work in data['work']:
            for key, value in work.items():
                doc.add_paragraph(f"{value[0]['Title']}, {value[1]['Company']} {value[2]['Date']}")

    elif section == 'Projects':
        for project in data['projects']:
           for key, value in project.items():
                doc.add_paragraph(key)
                for point in value:
                    doc.add_paragraph(f"{point}", style='List Bullet')

doc.save('sapmle1.docx')

