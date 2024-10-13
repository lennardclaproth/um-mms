import os
import zipfile


class ExportService:

    def backup(path):
        folder_to_zip = "data"
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_to_zip):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_to_zip)
                    zipf.write(file_path, relative_path)
