from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

name = 'AMISH GOEL'
email = 'Jobs@lets.workwithamish.me'
linkedinLink = 'https://www.linkedin.com/in/amish-goyal-096066b4/'
github = 'https://github.com/AmishGoel1'
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
doc.save('sapmle1.docx')
