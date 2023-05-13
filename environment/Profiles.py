import os

from environment import schemas
from environment import utilities

Profiles = {
    'Admin': {
        'profile_username': "Admin",
        'profile_password': "admin123",
        'profile_schema1': schemas.SCHEMA1,
        'profile_book_token': os.environ["book_token"]
    }
}