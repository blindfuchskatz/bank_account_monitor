from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.platypus import SimpleDocTemplate, Paragraph # type: ignore
from reportlab.lib.styles import getSampleStyleSheet # type: ignore



class PdfCreator:
    def write(self, pdf_filename, text):

        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']
        paragraphs = text.split('\n')
        for paragraph_text in paragraphs:
            paragraph = Paragraph(paragraph_text, normal_style, encoding='utf-8')
            story.append(paragraph)

        doc.build(story)
