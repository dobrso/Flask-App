from werkzeug.security import generate_password_hash, check_password_hash

from repositories.userRepository import UserRepository


class UserService:
    def __init__(self):
        self.userRepository = UserRepository()

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
        return True, "Вы успешно зарегистрировались", user.id

    @staticmethod
    def validatePassword(password):
        pass

    @staticmethod
    def validateUsername(username):
        pass
