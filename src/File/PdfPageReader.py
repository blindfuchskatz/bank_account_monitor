from pypdf import PdfReader


class PdfPageReader:
    def read_file_content(self, path):
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text

    def is_pdf(self, path):
        try:
            with open(path, 'rb') as file:
                header = file.read(4)
                return header == b'%PDF'
        except Exception:
            return False
