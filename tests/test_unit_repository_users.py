import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import UserSchema, UserResponse, RequestEmail
from src.repository.users import (
    get_user_by_email,
    create_user,
    confirmed_email,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username='test_user', password="qwerty", confirmed=True)

    async def test_create_user(self):
        mok_gravatar = MagicMock()
        body = UserSchema(username='test_user', password="12345678", email="ex@example.com", avatar=mok_gravatar)
        result = await create_user(body=body, db=self.session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.password, body.password)
        self.assertEqual(result.email, body.email)
        self.assertTrue(hasattr(result, "id"))

    async def test_not_confirmed_email(self):
        mok_gravatar = MagicMock()
        body = User(username='test_user', password="12345678", email="ex@example.com", avatar=mok_gravatar,
                    confirmed=False)
        result = await confirmed_email(email=body.email, db=self.session)
        self.assertNotEqual(result, body.confirmed)

    async def test_confirmed_email(self):
        mok_gravatar = MagicMock()
        body = User(username='test_user', password="12345678", email="ex@example.com", avatar=mok_gravatar,
                    confirmed=True)
        result = await confirmed_email(email=body.email, db=self.session)
        self.assertNotEqual(result, body.confirmed)

    async def test_get_user_by_email(self):
        mok_gravatar = MagicMock()
        user = User(username='test_user_1', password="12345678", email="ex@example.com", avatar=mok_gravatar)
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(user.email, self.session)
        self.assertEqual(result, user)


if __name__ == '__main__':
    unittest.main()

