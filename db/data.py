"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import os

import db.db_connect as dbc

# DEMO_HOME = os.environ["DEMO_HOME"]

PROBLEMS = "Problems"
USERS = "users"
TESTS = 'tests'

# field names in our DB:
USER_NM = "userName"

NUM_USERS = "num_users"

OK = 0
NOT_FOUND = 1
DUPLICATE = 2


client = dbc.get_client()
if client is None:
    print("Failed to connect to MongoDB.")
    exit(1)


def get_problems():
    """
    A function to return a list of all rooms.
    """
    return dbc.fetch_all(PROBLEMS)

def get_tests():
    """
    A function to return a list of all rooms.
    """
    return dbc.fetch_all(TESTS)

def get_rooms_as_dict():
    """
    A function to return a dictionary of all rooms.
    """
    return dbc.fetch_all_as_dict(ROOMS, ROOM_NM)


def room_exists(roomname):
    """
    See if a room with roomname is in the db.
    Returns True of False.
    """
    rec = dbc.fetch_one(ROOMS, filters={ROOM_NM: roomname})
    print(f"{rec=}")
    return rec is not None


def del_room(roomname):
    """
    Delete roomname from the db.
    """
    if not room_exists(roomname):
        return NOT_FOUND
    else:
        dbc.del_one(ROOMS, filters={ROOM_NM: roomname})
        return OK


def add_room(roomname):
    """
    Add a room to the room database.
    """
    print(f"{roomname=}")
    if room_exists(roomname):
        return DUPLICATE
    else:
        dbc.insert_doc(ROOMS, {ROOM_NM: roomname, NUM_USERS: 0})
        return OK

def add_problem(problem):

    print(f"{problem=}")
    return dbc.insert_doc(PROBLEMS, {"equ": problem['equ'], "direction": problem['direction'],
                                     "rule": problem['rule']})
    
def add_test(test):

    print(f"{test=}")
    return dbc.insert_doc(TESTS, {"equ": test['equ'], "direction": test['direction']})


def user_exists(username):
    """
    See if a user with username is in the db.
    Returns True of False.
    """
    rec = dbc.fetch_one(USERS, filters={USER_NM: username})
    print(f"{rec=}")
    return rec is not None


def get_users():
    """
    A function to return a list of all users.
    """
    return dbc.fetch_all(USERS)


def add_user(username, password):
    """
    Add a user to the user database.
    Until we are using a real DB, we have a potential
    race condition here.
    """
    if user_exists(username):
        return DUPLICATE
    else:
        dbc.insert_doc(USERS, {USER_NM: username, "password": password})
        return OK


def del_user(username):
    """
    Delete username from the db.
    """
    if not user_exists(username):
        return NOT_FOUND
    else:
        dbc.del_one(USERS, filters={USER_NM: username})
        return OK
