"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

# import os

import db.db_connect as dbc

# DEMO_HOME = os.environ["DEMO_HOME"]

PROBLEMS = "Problems"
USERS = "users"
TESTS = 'tests'


# field names for users:
USER_NM = "userName"

# field names for problems:
EQU = 'equ'
DIRECT = 'direction'
RULE = 'rule'
ANSWER = 'answer'
USER = 'user'

OK = 0
NOT_FOUND = 1
DUPLICATE = 2


client = dbc.get_client()
if client is None:
    print("Failed to connect to MongoDB.")
    exit(1)


def get_problems():
    """
    A function to return a list of all problems.
    """
    return dbc.fetch_all(PROBLEMS)


def add_problem(problem):
    print(f"{problem=}")
    return dbc.insert_doc(PROBLEMS, {EQU: problem[EQU],
                                     DIRECT: problem[DIRECT],
                                     RULE: problem[RULE],
                                     ANSWER: problem[ANSWER],
                                     USER: problem[USER]
                                     })


def get_tests():
    """
    A function to return a list of all tests.
    """
    return dbc.fetch_all(TESTS)


def add_test(test):
    print(f"{test=}")
    return dbc.insert_doc(TESTS, {EQU: test[EQU],
                                  DIRECT: test[DIRECT],
                                  ANSWER: test[ANSWER],
                                  USER: test[USER]})


def user_exists(username):
    """
    See if a user with username is in the db.
    Returns True of False.
    """
    rec = dbc.fetch_one(USERS, filters={USER_NM: username})
    print(f"{rec=}")
    return rec is not None


def problem_exists(equation):
    rec = dbc.fetch_one(PROBLEMS, filters={EQU: equation})
    print(f"{rec=}")
    return rec is not None


def test_exists(equ):
    """
    See if a user with username is in the db.
    Returns True of False.
    """
    rec = dbc.fetch_one(TESTS, filters={EQU: equ})
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


def del_problem(equation):
    """
    Delete username from the db.
    """
    if not problem_exists(equation):
        return NOT_FOUND
    else:
        dbc.del_one(PROBLEMS, filters={EQU: equation})
        return OK


def del_test(equ):
    """
    Delete username from the db.
    """
    if not test_exists(equ):
        return NOT_FOUND
    else:
        dbc.del_one(TESTS, filters={EQU: equ})
        return OK
