import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format('postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        

        self.new_question = {
            'question': 'newquestion1',
            'answer': 'newanswer to newquestion1',
            'category': 2,
            'difficulty': 5
        }

        self.new_question_null = {
            'question': '',
            'answer': 'newanswer to newquestion1',
            'category': 2,
            'difficulty': 5
        }

        self.searchTerm1 = {
            'searchTerm': 'q7'
        }
        
        self.searchTerm2 = {
            'searchTerm': 'title name'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_list_categories(self):
        """List existance categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
    
    
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
    
    def test_search_questions(self):
        res = self.client().post('/questions', json=self.searchTerm1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_200_search_not_found_questions(self):
        res = self.client().post('/questions', json=self.searchTerm2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalQuestions'], 0)
        self.assertEqual(len(data['questions']), 0)
        self.assertTrue(len(data['categories']))
    
    def test_delete_question(self):
        res = self.client().delete('/questions/24')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id==1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 24)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(question, None)
    
    def test_404_delete_requesting_beyond_valid_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    
    def test_create_new_question(self):
        """Create a new question"""
        res = self.client().post('/add', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
    

    def test_422_create_null_question(self):
        res = self.client().post('/add', json=self.new_question_null)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_play_categories(self):
        res = self.client().get('play')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()