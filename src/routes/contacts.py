from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactBase, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/search_by_elem_body", response_model=list[ContactResponse],
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def search_contacts(name: str = None, fullname: str = None, email: str = None,
                          db: Session = Depends(get_db), user: User = Depends(auth_service.get_current_user)):

    """
    The search_contacts function searches for contacts in the database.
        It takes three optional parameters: name, fullname and email.
        If no parameter is given, it returns all contacts of the user.

    :param name: str: Search for a contact by name
    :param fullname: str: Search for a contact by fullname
    :param email: str: Search for a contact by email
    :param db: Session: Get the database session
    :param user: User: Get the current user from the auth_service
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.search_contacts(name, fullname, email, db, user)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get("/search_by_birthday", response_model=list[ContactResponse],
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def search_contacts(db: Session = Depends(get_db), user: User = Depends(auth_service.get_current_user)):

    """
    The search_contacts function is used to search for contacts that have a birthday in the next 7 days.
        The function takes in a database session and an authenticated user as parameters.
        It then calls the repository_contacts.search_birthday function, which returns all contacts with birthdays within 7 days of today's date.

    :param db: Session: Get the database session
    :param user: User: Get the user id from the token
    :return: A list of contacts with a birthday in the next month
    :doc-author: Trelent
    """
    contacts = await repository_contacts.search_birthday(db, user)

    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get("/", response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def read_contacts(offset: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts function returns a list of contacts.

    :param offset: int: Specify the starting point of the query
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Get the database session
    :param user: User: Get the user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(offset, limit, db, user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact function is used to retrieve a single contact from the database.
    It takes in an integer representing the ID of the contact, and returns a Contact object.

    :param contact_id: int: Specify the contact id that is passed in the url
    :param db: Session: Pass the database session to the function
    :param user: User: Get the current user, and the db: session parameter is used to get a database session
    :return: A contact object, which is defined in the models
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def create_contact(body: ContactBase, db: Session = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactBase: Specify the type of data that will be passed to the function
    :param db: Session: Pass the database session into the function
    :param user: User: Get the user id from the current user
    :return: The new contact
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, db, user)


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            - body: A ContactBase object containing the new values for the contact.
            - contact_id: An integer representing the ID of an existing contact to be updated.
            - db (optional): A Session object used to connect to and query a database, if not provided, one will be created automatically using get_db().

    :param body: ContactBase: Get the data from the request body
    :param contact_id: int: Identify the contact to be deleted
    :param db: Session: Pass the database session to the repository function
    :param user: User: Get the current user
    :return: A contactbase object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse,
               dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the id of the contact to be removed
    :param db: Session: Pass the database session to the repository layer
    :param user: User: Get the current user
    :return: The contact that was removed
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
