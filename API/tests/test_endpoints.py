"""
This file holds the tests for endpoints.py.
"""

from unittest import TestCase, skip 
from flask_restx import Resource, Api
import random

import API.endpoints as ep
import db.data as db

HUGE_NUM = 10000000000000  # any big number will do!


def new_entity_name(entity_type):
    int_name = random.randint(0, HUGE_NUM)
    return f"new {entity_type}" + str(int_name)


class EndpointTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hello(self):
        hello = ep.HelloWorld(Resource)
        ret = hello.get()
        self.assertIsInstance(ret, dict)
        self.assertIn(ep.HELLO, ret)

    @skip("In the middle of making this work.")
    def test_create_user(self):
        """
        See if we can successfully create a new user.
        Post-condition: user is in DB.
        """

        cu = ep.CreateUser(Resource)
        new_user = new_entity_name("user")
        ret = cu.post(new_user)
        users = db.get_users()
        self.assertIn(new_user, users)

    def test_create_problem(self):
        """
        See if we can successfully create a new test.
        Post-condition: test is in DB.
        """
        problem = {'equ':  new_entity_name('x+8'),
                    "direction": 'solve',
                    "rule": "x=ints",
                    "answer": "x+8"}
        
        response = ep.app.test_client().post('/problems/create/', json=problem)
        print(f'post {response=}')
        self.assertEqual(response.status_code, 200)
        found = False
        # make sure the new record is in there somewhere:
        for prob in db.get_problems():
            if prob[db.EQU] == problem[db.EQU]:
                found = True
        self.assertTrue(found)
        

    def test_list_questions(self):
        """
        Post-condition 1: return is a list.
        """
        lr = ep.ListProblems(Resource)
        ret = lr.get()
        self.assertIsInstance(ret, list)
