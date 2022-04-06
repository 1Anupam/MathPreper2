"""
This file holds the tests for db.py.
"""

from unittest import TestCase, skip
# import random

import db.data as db

FAKE_USER = "Fake user"


class DBTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


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

    def test_get_tests(self):
        """
        Can we fetch user db?
        """
        tests = db.get_tests()
        self.assertIsInstance(tests, list)

    def test_add_problem(self):
        problem = ({'equ': "Fake equation!", 'direction': 'Fake directions!', 'rule': 'Fake rule!'})
        db.add_problem(problem)
        self.assertTrue(db.get_problems()[-1]['equ'] == problem['equ'])
        db.del_problem(problem['equ'])
        

    def test_add_test(self):
        test = {'equ': "Fake equation!", "direction": 'Fake directions!'}
        db.add_test(test)
        self.assertTrue(db.get_tests()[-1]['equ'] == test['equ'])
        db.del_test(test['equ'])

    def test_add_user(self):
        db.add_user("Fake username", "Fake password!")
        self.assertTrue(db.get_users()[-1]['userName'] == "Fake username")
        db.del_user("Fake username")
    
    

    
        
