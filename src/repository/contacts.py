from datetime import timedelta, datetime
from sqlalchemy.orm import Session

from sqlalchemy import extract
from src.database.models import Contact, User
from src.schemas import ContactBase


async def search_contacts(name: str, fullname: str, email: str, db: Session, user: User):

    """
    The search_contacts function searches for contacts in the database.
        Args:
            name (str): The contact's name.
            fullname (str): The contact's fullname.
            email (str): The contact's email address.

    :param name: str: Search for a contact by name
    :param fullname: str: Search for a contact by fullname
    :param email: str: Search for a contact by email address
    :param db: Session: Pass in the database session
    :param user: User: Filter the results by user
    :return: A list of contacts
    :doc-author: Trelent
    """
    if name:
        contact = db.query(Contact).filter_by(name=name, user=user).all()
        return contact
    if fullname:
        contact = db.query(Contact).filter_by(fullname=fullname, user=user).all()
        return contact
    if email:
        contact = db.query(Contact).filter_by(email=email, user=user).all()
        return contact


async def search_birthday(db: Session, user: User):
    """
    The search_birthday function searches the database for contacts whose birthday is within a week of today's date.
        It returns a list of all such contacts.

    :param db: Session: Pass the database session to the function
    :param user: User: Identify the user that is currently logged in
    :return: A list of contacts with birthdays in the next 7 days
    :doc-author: Trelent
    """
    today = datetime.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
            ((extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day)) |
            ((extract('month', Contact.birthday) == end_date.month) & (
                    extract('day', Contact.birthday) <= end_date.day)), user=user
        ).all()

    return contacts


async def get_contacts(offset: int, limit: int, db: Session, user: User):
    """
    The get_contacts function returns a list of contacts for the user.

    :param offset: int: Specify the number of contacts to skip
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Access the database
    :param user: User: Filter the contacts by user
    :return: A list of contacts
    :doc-author: Trelent
    """
    return db.query(Contact).filter_by(user=user).offset(offset).limit(limit).all()


async def get_contact(contact_id: int, db: Session, user: User):
    """
    The get_contact function takes in a contact_id and returns the corresponding Contact object.
        Args:
            contact_id (int): The id of the Contact to be retrieved.
            db (Session): A database session for querying Contacts from the database.
            user (User): The User who is requesting this information, used to ensure that they are authorized to access it.

    :param contact_id: int: Specify the id of the contact to be retrieved
    :param db: Session: Pass the database session to the function
    :param user: User: Ensure that the user is authorized to access this contact
    :return: A contact object
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.id == contact_id, user=user).first()


async def create_contact(body: ContactBase, db: Session, user: User):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactBase: Get the data from the request body
    :param db: Session: Pass a database session to the function
    :param user: User: Get the user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(name=body.name,
                      fullname=body.fullname,
                      email=body.email,
                      phone_number=body.phone_number,
                      birthday=body.birthday,
                      description=body.description,
                      user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactBase, db: Session, user: User):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactBase): The updated information for the specified contact.

    :param contact_id: int: Identify the contact to be deleted
    :param body: ContactBase: Pass the contact information to update
    :param db: Session: Pass the database session to the function
    :param user: User: Check if the user is logged in
    :return: The contact that was updated
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(Contact.id == contact_id, user=user).first()
    if contact:
        contact.name = body.name
        contact.fullname = body.fullname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.description = body.description
    db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, user: User):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session): A connection to the database.
            user (User): The user who is removing this contact.

    :param contact_id: int: Identify the contact to be deleted
    :param db: Session: Pass the database session to the function
    :param user: User: Ensure that the user is authorized to delete a contact
    :return: The contact that was removed
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(Contact.id == contact_id, user=user).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
