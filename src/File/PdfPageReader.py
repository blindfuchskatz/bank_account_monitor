from pypdf import PdfReader


class PdfPageReader:
    @staticmethod
    def read_file_content(path):
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text

    @staticmethod
    def is_pdf(path):
        try:
            with open(path, 'rb') as file:
                header = file.read(4)
                return header == b'%PDF'
        except Exception:
            return False
