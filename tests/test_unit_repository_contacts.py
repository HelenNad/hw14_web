import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactResponse
from src.repository.contacts import (
    search_contacts,
    search_birthday,
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    remove_contact
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username='test_user', password='qwerty', confirmed=True)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter_by().offset().limit().all.return_value = contacts
        result = await get_contacts(offset=0, limit=100, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_note_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_note(self):
        body = ContactBase(name="Test1",
                           fullname="Test1Big",
                           email="test@exampl.com",
                           phone_number="123456789",
                           birthday="2000-12-03",
                           description="test")
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.fullname, body.fullname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactBase(name="Test1",
                           fullname="Test1Big",
                           email="test@exampl.com",
                           phone_number="123456789",
                           birthday="2000-12-03",
                           description="test",
                           user=self.user)
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactBase(name="Test1",
                           fullname="Test1Big",
                           email="test@exampl.com",
                           phone_number="123456789",
                           birthday="2000-12-03",
                           description="test",
                           user=self.user)
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_search_contacts(self):
        # name = ContactBase(name="Test1",
        #                    user=self.user)
        # fullname = ContactBase(fullname="Test1Big",
        #                        user=self.user)
        # email = ContactBase(email="test@exampl.com",
        #                     user=self.user)
        contacts = [Contact(name="Test1"), Contact(), Contact(), Contact()]
        self.session.query().filter_by().all.return_value = contacts
        result = await search_contacts(name="Test1", fullname="Test1Big", email="test@exampl.com", user=self.user,
                                       db=self.session)
        self.assertEqual(result, contacts)

    async def test_search_birthday(self):
        contacts = [Contact(), Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await search_birthday(user=self.user, db=self.session)
        self.assertEqual(result, contacts)


if __name__ == '__main__':
    unittest.main()
