"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus
from flask import Flask, request
from flask_cors import CORS
from flask_restx import Resource, Api, fields
import werkzeug.exceptions as wz


import db.data as db

app = Flask(__name__)
CORS(app)
api = Api(app)

HELLO = 'Hola'
WORLD = 'mundo'


@api.route('/hello')
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO: WORLD}


@api.route('/problems/list')
class ListProblems(Resource):
    """
    This endpoint returns a list of all problems.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Returns a list of all  problems.
        """
        problem_types = db.get_problems()
        if problem_types is None:
            raise (wz.NotFound("Problems not found."))
        else:
            return problem_types




@api.route('/tests/list')
class ListTests(Resource):
    """
    This endpoint returns a list of all problems.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Returns a list of all  problems.
        """
        test_types = db.get_tests()
        if test_types is None:
            raise (wz.NotFound("Problems not found."))
        else:
            return test_types


problem_fields = api.model('Problem', {
    "equ": fields.String,
    "direction": fields.String,
    "rule": fields.String,
    "answer": fields.String,
    "user": fields.String,
})

test_fields = api.model('Test', {
    "equ": fields.String,
    "direction": fields.String,
    "answer": fields.String,
    "user": fields.String,
})

login_fields  = api.model('Login', {
    "userName": fields.String,
    "password": fields.String,
    
})


@api.route('/problems/create/')
class CreateProblem(Resource):
    """
    This class supports adding a problem to the database.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.expect(problem_fields)
    def post(self):

        """
        This method adds a problem to the database.
        """
        args = request.json
        print(f"{args=}")
        print(f"{args['equ']=} ")
        print(f"{args['direction']=} ")
        print(f"{args['rule']=} ")

        ret = db.add_problem(args)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("User db not found."))
        return f"{args} added."


@api.route('/tests/create/')
class CreateTest(Resource):
    """
    This class supports adding a problem to the database.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.expect(test_fields)
    def post(self):

        """
        This method adds a problem to the database.
        """
        args = request.json
        ret = db.add_test(args)
        print("args", args)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("User db not found."))
        return f"{args} added."


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    @api.response(HTTPStatus.OK, 'Success')
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route('/users/list')
class ListUsers(Resource):
    """
    This endpoint returns a list of all users.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Returns a list of all users.
        """
        users = db.get_users()
        if users is None:
            raise (wz.NotFound("User db not found."))
        else:
            return users


@api.route('/users/create')
class CreateUser(Resource):
    """
    This class supports adding a user to the database.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.expect(login_fields)
    def post(self):
        """
        This method adds a user to the database.
        """
        args = request.json
        ret = db.add_user(args['userName'], args['password'])
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("User db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("User name already exists."))
        return f"{args['userName']} added."


@api.route('/users/delete/<username>')
class DeleteUser(Resource):
    """
    This class enables deleting a chat user.
    While 'Forbidden` is a possible return value, we have not yet implemented
    a user privileges section, so it isn't used yet.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.FORBIDDEN, 'A user can only delete themselves.')
    def post(self, username):
        """
        This method deletes a user from the user db.
        """
        ret = db.del_user(username)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound(f"Chat participant {username} not found."))
        else:
            return f"{username} deleted."


@api.route('/problems/delete/<equation>')
class DeleteProblem(Resource):
    """
    This class enables deleting a problem.
    While 'Forbidden` is a possible return value, we have not yet implemented
    a user privileges section, so it isn't used yet.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.FORBIDDEN, 'A user can only delete themselves.')
    def post(self, equation):
        """
        This method deletes a user from the user db.
        """
        ret = db.del_problem(equation)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound(f"Chat participant {equation} not found."))
        else:
            return f"{equation} deleted."


@api.route('/tests/delete/<equation>')
class DeleteTest(Resource):
    """
    This class enables deleting a problem.
    While 'Forbidden` is a possible return value, we have not yet implemented
    a user privileges section, so it isn't used yet.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.FORBIDDEN, 'A user can only delete themselves.')
    def post(self, equation):
        """
        This method deletes a user from the user db.
        """
        ret = db.del_test(equation)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound(f"Chat participant {equation} not found."))
        else:
            return f"{equation} deleted."
