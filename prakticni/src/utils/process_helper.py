import subprocess
import os
import platform

class ProcessHelper:

    @staticmethod
    def open_file_in_default_app(file_path):
        system_name = platform.system()

        try:
            if system_name == "Windows":
                os.startfile(file_path)
            elif system_name == "Darwin":
                subprocess.run(["open", file_path])
            else:
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            print(f"Error opening file {file_path}: {e}")

process_helper = ProcessHelper()