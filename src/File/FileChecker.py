import os


class FileChecker:
    @staticmethod
    def file_exists(file: str) -> bool:
        return os.path.exists(file) and os.path.isfile(file)

    @staticmethod
    def dir_of_file_exists(file: str) -> bool:
        directory = os.path.dirname(file)
        file = os.path.basename(file)

        if not file:
            return False

        if os.path.exists(directory) and os.path.isdir(directory):
            return True
        return False
