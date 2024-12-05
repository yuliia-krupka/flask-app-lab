import unittest

from flask import session
from app import create_app, db, bcrypt
from app.users.models import User


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="config_test")
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        hashed_password = bcrypt.generate_password_hash("password123").decode('utf-8')
        self.user = User(username="testuser", email="test@example.com", password=hashed_password)
        db.session.add(self.user)
        db.session.commit()

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
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    # --- Views Tests ---

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
        response = self.client.post("user/register", data={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
            "confirm_password": "password123"
        })
        self.assertEqual(response.status_code, 302)

        user = User.query.filter_by(username="newuser").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "new@example.com")
        self.assertTrue(bcrypt.check_password_hash(user.password, "password123"))

    def test_login_user(self):
        """Тестування входу користувача на сайт."""
        response = self.client.post("user/login", data={
            "username": "testuser",
            "password": "password123",
            "remember": False
        })

        self.assertEqual(response.status_code, 302)

        with self.client:
            self.client.get("/")
            self.assertIn("_user_id", session)

    def test_logout_user(self):
        """Тестування виходу користувача з сайту."""
        self.client.post("user/login", data={
            "username": "testuser",
            "password": "password123",
            "remember": False
        })

        response = self.client.get("user/logout")
        self.assertEqual(response.status_code, 302)

        with self.client:
            self.client.get("/")
            self.assertNotIn("_user_id", session)


if __name__ == "__main__":
    unittest.main()
