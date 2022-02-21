import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
from settings import TEST_DB_NAME, TEST_DB_USER, TEST_DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(TEST_DB_USER, TEST_DB_PASSWORD, 'localhost:5432', TEST_DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])


    def test_get_question_with_valid_page(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])


    def test_get_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')


    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])


    def test_list_questions_by_category_with_result(self):
        res = self.client().get('categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])


    def test_list_questions_by_category_without_result(self):
        res = self.client().get('categories/50/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")



    def test_create_question(self):
        res = self.client().post('/questions', json={"question": "my question 4", "answer": "my answer", "category": "2", "difficulty": "2"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions category'])



    def test_question_search(self):
        res = self.client().post('/questions/search', json={"searchTerm": "who"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])


    def test_question_search_no_match(self):
        res = self.client().post('/questions/search', json={"searchTerm": "no match"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")



    def test_quizzes(self):
        res = self.client().post('/quizzes', json={"previous_questions": ["2"], "quiz_category": {"type": "History", "id": 4}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


    def test_quizzes_fail(self):
        res = self.client().post('/quizzes', json={"previous_questions": ["2"], "quiz_category": {"type": "History", "id": 14}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable_entity")


    def test_delete_questions(self):
        res = self.client().delete('/questions/9')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 9).one_or_none()

        self.assertTrue(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])


    def test_delete_questions_not_exist(self):
        res =self.client().delete('/questions/9')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()