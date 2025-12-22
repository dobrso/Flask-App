from werkzeug.security import generate_password_hash, check_password_hash

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

    def getProfileID(self, userID):
        id = self.profileRepository.getProfileID(userID)
        return id

    @staticmethod
    def validatePassword(password):
        pass

    @staticmethod
    def validateUsername(username):
        pass
