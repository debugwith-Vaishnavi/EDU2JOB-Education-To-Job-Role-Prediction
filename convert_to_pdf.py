from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import markdown2
import os

# read markdown
with open('documentation.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

# convert markdown to HTML fragments
html = markdown2.markdown(md_text, extras=["tables", "fenced-code-blocks"])

# prepare document
doc = SimpleDocTemplate("Edu2Job_documentation.pdf", pagesize=letter)
styles = getSampleStyleSheet()
normal = styles["Normal"]
heading = styles["Heading1"]
flow = []

# split html by lines and create paragraphs
for line in html.split("\n"):
    line = line.strip()
    if not line:
        flow.append(Spacer(1, 12))
        continue
    # handle image tags
    if line.startswith("<p><img") and "src=" in line:
        # extract src
        start = line.find('src="') + 5
        end = line.find('"', start)
        src = line[start:end]
        if os.path.exists(src):
            flow.append(Image(src, width=400, height=300))
            flow.append(Spacer(1,12))
        continue
    # remove enclosing <p> tags
    if line.startswith("<p>") and line.endswith("</p>"):
        line = line[3:-4]
    flow.append(Paragraph(line, normal))

# build PDF
if flow:
    doc.build(flow)
    print('PDF generated')
else:
    print('No content to generate PDF.')
