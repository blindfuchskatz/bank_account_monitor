from src.File.FileWriterException import FileWriterException


FILE_WRITER_ERROR = "Could not open cve output file"


class FileWriter:
    def write(self, output_file, content):
        try:
            f = open(output_file, 'w')
            f.write(content)
            f.close()
        except Exception:
            raise FileWriterException(FILE_WRITER_ERROR)
