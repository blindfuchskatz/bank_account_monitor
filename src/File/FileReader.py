from src.File.FileReaderException import FileReaderException


class FileReader:
    @staticmethod
    def read_file_content(path: str) -> str:
        try:
            input_file = open(path)
            file_content = input_file.read()
            input_file.close()

            return file_content
        except Exception:
            raise FileReaderException(
                f"File reader error|Could not open file|file:<{path}>")

    @staticmethod
    def get_lines(path: str) -> list:
        line_list = []

        for line in FileReader.read_file_content(path).splitlines():
            if len(line) == 0:
                continue

            line_list.append(line.strip())
        return line_list
