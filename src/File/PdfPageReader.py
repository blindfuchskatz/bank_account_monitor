from pypdf import PdfReader


class PdfPageReader:
    def read_file_content(self, path):
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text
