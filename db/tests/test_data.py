"""
This file holds the tests for db.py.
"""

from unittest import TestCase, skip
# import random

import db.data as db
import db.db_connect as dbc

FAKE_USER = "Fake user"


class DBTestCase(TestCase):
    def setUp(self):
        # insert a known problem here
        pass

    def tearDown(self):
        print(f'{dbc.db_nm=}')
        
        dbc.client[dbc.db_nm][db.PROBLEMS].delete_many({})
        dbc.client[dbc.db_nm][db.TESTS].delete_many({})

    def test_get_users(self):
        """
        Can we fetch user db?
        """
        users = db.get_users()
        self.assertIsInstance(users, list)

    def test_get_problems(self):
        """
        Can we fetch user db?
        """
        problems = db.get_problems()
        self.assertIsInstance(problems, list)
        # here see if known problem is in the results

    def test_get_tests(self):
        """
        Can we fetch user db?
        """
        tests = db.get_tests()
        self.assertIsInstance(tests, list)

    def test_add_problem(self):
        problem = ({db.EQU: "Fake equation!", 'direction': 'Fake directions!',
                    db.RULE: 'Fake rule!', "answer": "Fake answer"})
        db.add_problem(problem)
        found = False
        # make sure the new record is in there somewhere:
        for prob in db.get_problems():
            if prob[db.EQU] == problem[db.EQU]:
                found = True
        self.assertTrue(found)

    def test_add_test(self):
        sample_test = {db.EQU: "Fake equation!", "direction": 'Fake directions!', "answer": 100}
        db.add_test(sample_test)
        found = False
        # make sure the new record is in there somewhere:
        for test in db.get_tests():
            if test[db.EQU] == sample_test[db.EQU]:
                found = True
        self.assertTrue(found)
        

    def test_add_user(self):
        db.add_user("Fake username", "Fake password!")
        found = False
        # make sure the new record is in there somewhere:
        for user in db.get_users():
            if user["userName"] == "Fake username":
                found = True
        self.assertTrue(found)
