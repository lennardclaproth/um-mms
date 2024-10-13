import os
import zipfile


class ImportService:

    def restore(path):
        tmp_path = "data"
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(tmp_path)
