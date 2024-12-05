import unittest
from flask_login import current_user
from app import create_app, db
from app.users.models import User


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app = create_app()
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        self.app = app
        with self.app.app_context():
            db.create_all()

    def test_greetings_page(self):
        """Тест маршруту /hi/<name>."""
        response = self.client.get("user/hi/John?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        """Тест маршруту /admin, який перенаправляє."""
        response = self.client.get("user/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"45", response.data)

    def tearDown(self):
        """Очистка після тестів."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registration_page(self):
        """Тестування завантаження сторінки реєстрації."""
        response = self.client.get("user/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)

    def test_login_page(self):
        """Тестування завантаження сторінки входу."""
        response = self.client.get("user/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_register_user(self):
        """Тестування коректного збереження користувача в БД при реєстрації."""
        with self.app.app_context():
            response = self.client.post("user/register", data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "confirm_password": "password123"
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Account for testuser was created!", response.data)

            user = User.query.filter_by(username="testuser").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "test@example.com")

    def test_login_user(self):
        """Тестування входу користувача на сайт."""
        with self.app.app_context():
            self.client.post("user/register", data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "confirm_password": "password123"
            })

            response = self.client.post("user/login", data={
                "username": "testuser",
                "password": "password123",
                "remember": False
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You logged in successfully!", response.data)

    def test_logout_user(self):
        """Тестування виходу користувача з сайту."""
        with self.app.app_context():
            self.client.post("user/register", data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "confirm_password": "password123"
            })

            self.client.post("user/login", data={
                "username": "testuser",
                "password": "password123",
                "remember": False
            })

            response = self.client.get("user/logout", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            with self.app.test_request_context():
                self.assertFalse(current_user.is_authenticated)

    def test_account_page_access(self):
        """Тестування доступу до сторінки акаунта."""
        with self.app.app_context():
            self.client.post("user/register", data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "confirm_password": "password123"
            })

            self.client.post("user/login", data={
                "username": "testuser",
                "password": "password123",
                "remember": False
            })

            response = self.client.get("user/account")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Account", response.data)

    def test_unauthorized_account_access(self):
        """Тестування доступу до сторінки акаунта без авторизації."""
        response = self.client.get("user/account", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Account", response.data)


if __name__ == "__main__":
    unittest.main()
