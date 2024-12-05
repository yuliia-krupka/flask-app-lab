import unittest
from app import create_app, db
from app.users.models import User


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app = create_app()
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
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
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)

    def test_login_page(self):
        """Тестування завантаження сторінки входу."""
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_register_user(self):
        """Тестування коректного збереження користувача в БД при реєстрації."""
        response = self.client.post("/register", data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "test@example.com")

    def test_login_user(self):
        """Тестування входу користувача на сайт."""
        self.client.post("/register", data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        response = self.client.post("/login", data={
            "username": "testuser",
            "password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome, testuser!", response.data)

    def test_logout_user(self):
        """Тестування виходу користувача з сайту."""
        self.client.post("/register", data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        self.client.post("/login", data={
            "username": "testuser",
            "password": "password123"
        })
        response = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You have been logged out.", response.data)


if __name__ == "__main__":
    unittest.main()
