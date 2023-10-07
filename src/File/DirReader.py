import os


class DirReader:
    @staticmethod
    def get_files_in_dir(dir: str) -> list:
        files_in_folder = [os.path.abspath(os.path.join(dir, filename)) for filename in os.listdir(
            dir) if os.path.isfile(os.path.join(dir, filename))]

        return files_in_folder

    @staticmethod
    def is_dir(file: str) -> bool:
        return os.path.isdir(file)
