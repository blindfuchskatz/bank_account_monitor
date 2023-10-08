from src.File.FileWriterException import FileWriterException


FILE_WRITER_ERROR = "Could not open cve output file"


class FileWriter:
    @staticmethod
    def write(output_file: str, content: str) -> None:
        try:
            f = open(output_file, 'w')
            f.write(content)
            f.close()
        except Exception:
            raise FileWriterException(FILE_WRITER_ERROR)
