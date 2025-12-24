import os

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from repositories.profileRepository import ProfileRepository
from repositories.userRepository import UserRepository
from utilities.fileHandler import FileHandler


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

            image = FileHandler.saveFile(imageFile)
        self.profileRepository.update(id, bio, phoneNumber, image)

    @staticmethod
    def validatePassword(password):
        pass

    @staticmethod
    def validateUsername(username):
        pass
