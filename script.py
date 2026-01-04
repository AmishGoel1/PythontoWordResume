from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches
from docx.text.run import Run
from docx.text.paragraph import Paragraph
import yaml

with open('points.yaml', 'r') as f:
    data = yaml.safe_load(f)

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
    currentsection.paragraph_format.space_after = Pt(0)
    
    if section == 'Professional Summary':
        summarytext = doc.add_paragraph(f"{data['summary']}")
        formatting(summarytext.runs[0], False)     
        # summarytext.paragraph_format.line_spacing = 1.05
    
    elif section == 'Core Skills':
        for skill in data['skills']:
           for key, value in skill.items():
                currentpoint = doc.add_paragraph(f"{key}: ")
                formatting(currentpoint.runs[0])
                valuerun = currentpoint.add_run(f"{value}")
                formatting(valuerun, False)
                currentpoint.paragraph_format.space_after = Pt(3)
        
        doc.add_paragraph()
    
    elif section == 'Work Experience':
        for work in data['work']:
            for key, value in work.items():
                doc.add_paragraph(f"{value[0]['Title']}, {value[1]['Company']} {value[2]['Date']}")
                for point in value[3]['Points']:
                    currentworkpoint = doc.add_paragraph(f"{point}", style='List Bullet')
                    formatting(currentworkpoint.runs[0], False)
                    currentworkpoint.paragraph_format.space_after = Pt(3)
            doc.add_paragraph()
    
    elif section == 'Projects':
        for i, project in enumerate(data['projects']):
           for key, value in project.items():
                projectname = doc.add_paragraph(key)
                formatting(projectname.runs[0])
                if i == 0:
                    projectname.paragraph_format.space_before = Pt(0)
                else: 
                    projectname.paragraph_format.space_before = Pt(9)
                for point in value:
                    currentpoint = doc.add_paragraph(f"{point}", style='List Bullet')
                    formatting(currentpoint.runs[0], False)
                    spacing(currentpoint, Pt(15), Pt(3))

section = doc.sections[0]

section.left_margin = Inches(0.5)
section.right_margin = Inches(0.5)
section.top_margin = Inches(0.437)
section.bottom_margin = Inches(0.287)

doc.save('sapmle1.docx')

