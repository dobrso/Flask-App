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
        user = self.userRepository.getByName(username)
        if not user:
            return False, "Неверный пароль или имя пользователя", ""

        if check_password_hash(user.password_hash, password):
            return True, "", user.id
        else:
            return False, "Неверный пароль", ""

    def register(self, username, password):
        if self.userRepository.getByName(username):
            return False, "Данное имя пользователя уже занято", ""

        passwordHash = generate_password_hash(password)
        user = self.userRepository.create(username, passwordHash)
        self.profileRepository.create(user.id)
        return True, "", user.id

    def getUser(self, userId):
        user = self.userRepository.getById(userId)
        return user

    def getProfile(self, id):
        profile = self.profileRepository.get(id)
        return profile

    def getProfileId(self, id):
        id = self.profileRepository.getId(id)
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
