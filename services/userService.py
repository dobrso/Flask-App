import os
import time

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config
from repositories.profileRepository import ProfileRepository
from repositories.userRepository import UserRepository


class UserService:
    def __init__(self):
        self.userRepository = UserRepository()
        self.profileRepository = ProfileRepository()

    def login(self, username, password):
        user = self.userRepository.getByUsername(username)
        if not user:
            return False, "Неверный пароль или имя пользователя", ""

        if check_password_hash(user.password_hash, password):
            return True, "Вы успешно вошли", user.id
        else:
            return False, "Неверный пароль", ""

    def register(self, username, password):
        if self.userRepository.getByUsername(username):
            return False, "Данное имя пользователя уже занято", ""

        hashedPassword = generate_password_hash(password)
        user = self.userRepository.create(username, hashedPassword)
        self.profileRepository.create(user.id)
        return True, "Вы успешно зарегистрировались", user.id

    def getUser(self, id):
        user = self.userRepository.getById(id)
        return user

    def getProfile(self, id):
        profile = self.profileRepository.getProfile(id)
        return profile

    def getProfileId(self, id):
        id = self.profileRepository.getProfileId(id)
        return id

    def updateProfile(self, id, bio, phoneNumber, imageFile, oldImage):
        image = oldImage
        if imageFile.filename != "":
            if oldImage:
                oldImagePath = os.path.join(current_app.config['UPLOAD_FOLDER'], oldImage)
                if os.path.exists(oldImagePath):
                    os.remove(oldImagePath)

            image = UserService.saveFile(imageFile)
        self.profileRepository.update(id, bio, phoneNumber, image)

    @staticmethod
    def validatePassword(password):
        pass

    @staticmethod
    def validateUsername(username):
        pass

    @staticmethod
    def isFileAllowed(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def saveFile(file):
        if file and UserService.isFileAllowed(file.filename):
            filename = secure_filename(file.filename)

            name, extension = os.path.splitext(filename)
            newFilename = f"{name}_{int(time.time())}{extension}"

            uploadFolder = current_app.config['UPLOAD_FOLDER']
            filePath = os.path.join(uploadFolder, newFilename)
            file.save(filePath)
            return newFilename
        return None