import os
import time

from flask import current_app
from werkzeug.utils import secure_filename

from config import Config


class FileHandler:
    @staticmethod
    def isFileAllowed(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def saveFile(file):
        if file and FileHandler.isFileAllowed(file.filename):
            filename = secure_filename(file.filename)

            name, extension = os.path.splitext(filename)
            newFilename = f"{name}_{int(time.time())}{extension}"

            uploadFolder = current_app.config['UPLOAD_FOLDER']
            filePath = os.path.join(uploadFolder, newFilename)
            file.save(filePath)
            return newFilename
        return None