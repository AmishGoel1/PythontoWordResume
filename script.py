from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches
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
nametext.paragraph_format.space_after = Pt(0)

linkspara = doc.add_paragraph(f"{email} | LinkedIn | GitHub")
linkspara.runs[0].font.name = 'Times New Roman'
linkspara.runs[0].font.size = Pt(14)
linkspara.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

for section in sections:
    currentsection = doc.add_paragraph(f"{section}\n")
    currentrun = currentsection.runs[0]
    currentrun.font.name = 'Times New Roman'
    currentrun.font.size = Pt(13)
    currentrun.bold= True
    currentsection.paragraph_format.space_after = Pt(0)
    
    if section == 'Professional Summary':
        summarytext = doc.add_paragraph(f"{data['summary']}")
        
        summarytext.runs[0].font.size = Pt(12)
        summarytext.runs[0].font.name = 'Times New Roman'
        
        # summarytext.paragraph_format.line_spacing = 1.05
    
    elif section == 'Core Skills':
        for skill in data['skills']:
           for key, value in skill.items():
                currentpoint = doc.add_paragraph(f"{key}: ")
                currentpoint.runs[0].bold = True
                currentpoint.runs[0].font.name = 'Times New Roman'
                currentpoint.runs[0].font.size = Pt(12)
                valuerun = currentpoint.add_run(f"{value}")
                valuerun.font.size = Pt(12)
                valuerun.font.name = 'Times New Roman'
                currentpoint.paragraph_format.space_after = Pt(6)
                currentpoint.paragraph_format.space_after = Pt(3)
        
        doc.add_paragraph()
    
    elif section == 'Work Experience':
        for work in data['work']:
            for key, value in work.items():
                doc.add_paragraph(f"{value[0]['Title']}, {value[1]['Company']} {value[2]['Date']}")
                for point in value[3]['Points']:
                    currentworkpoint = doc.add_paragraph(f"{point}", style='List Bullet')
                    currentworkpoint.runs[0].font.size = Pt(12)
                    currentworkpoint.runs[0].font.name = 'Times New Roman'
                    currentworkpoint.paragraph_format.space_after = Pt(3)
            doc.add_paragraph()
    
    elif section == 'Projects':
        for i, project in enumerate(data['projects']):
           for key, value in project.items():
                projectname = doc.add_paragraph(key)
                projectname.runs[0].bold = True
                projectname.runs[0].font.size = Pt(12)
                projectname.runs[0].font.name = 'Times New Roman'
                if i == 0:
                    projectname.paragraph_format.space_before = Pt(0)
                else: 
                    projectname.paragraph_format.space_before = Pt(9)
                for point in value:
                    currentpoint = doc.add_paragraph(f"{point}", style='List Bullet')
                    currentpoint.runs[0].font.name = 'Times New Roman'
                    currentpoint.runs[0].font.size = Pt(12)
                    currentpoint.paragraph_format.space_after = Pt(3)
                    currentpoint.paragraph_format.space_before = Pt(15)

section = doc.sections[0]

section.left_margin = Inches(0.5)
section.right_margin = Inches(0.5)
section.top_margin = Inches(0.437)
section.bottom_margin = Inches(0.287)

doc.save('sapmle1.docx')

