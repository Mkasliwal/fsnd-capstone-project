import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from app import create_app
from models import setup_db, Question, Category

JWT_ADMIN = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IndUT3NzelNiOEswQ01NdlRzQlJ6SSJ9.eyJpc3MiOiJodHRwczovL21rZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0NGQ3YjRiNWQzOWQwMDcwNDg0NzQ2IiwiYXVkIjoiY2Fwc3RvbmV0ZXN0IiwiaWF0IjoxNjE2NjYwMTExLCJleHAiOjE2MTY3MzIxMTEsImF6cCI6Iml0WlhEd1F4OVlHMkpOUDlYSlFybmRpZTc5SXE5ZmcyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6cXVlc3Rpb25zIiwiZ2V0OmNhdGVnb3JpZXMiLCJnZXQ6cXVlc3Rpb25zIiwicGF0Y2g6cXVlc3Rpb25zIiwicG9zdDpxdWVzdGlvbnMiXX0.sX7ruSE6o14q3QMe79efLAnc1JaRGvtvmZwItXRNpvEs2kQvaSYaUvpgYssiME8iwwHgrzk4lO6iUghg1BDeOFPo5nciySxuIIzRDZr6G_yZGqq1dBap8j8pO5mMXa3GdLhSn_aEKqqSAQSI9rmDlZ-McDQbDEnUUdO8lVhj33ft1KuabQBo0K35kt1ElmqH0HBM6wLtqjjwsxuqOa-Hv_3f_I09qzvOEmSRrouAw5bxaUAtAlSo9WUa28NkKMfQfeMs6ketsiUKeTwCO4g3wpFzWVqCRhcTunowS0h9doQivfKHiAnt6K4ncKVOD6QrrrhG2SgNZyQwggzh4qjiSA'
JWT_NORMAL_USER = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IndUT3NzelNiOEswQ01NdlRzQlJ6SSJ9.eyJpc3MiOiJodHRwczovL21rZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1MjBjYTdmYjM4MDMwMDY4MTM0MGJjIiwiYXVkIjoiY2Fwc3RvbmV0ZXN0IiwiaWF0IjoxNjE2NjYwMjg4LCJleHAiOjE2MTY3MzIyODgsImF6cCI6Iml0WlhEd1F4OVlHMkpOUDlYSlFybmRpZTc5SXE5ZmcyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6Y2F0ZWdvcmllcyIsImdldDpxdWVzdGlvbnMiXX0.XVFi3HnZofX4ZESwVW5fNDefFXdKbYi7Y8O3EFcIkaHvWw_Pwmyozd0DFtFzrJG9QIHznBgJ64gV9jfpuVnad_5fRWN2SdUGzHr77H8SwLpSbkSJLX5SEw26SeG3HxGcC9sGzwTQAlauMoiQiXppRrcGLi2xL0Om5Ion44uoCLUk_RwEwcmn1GwWX_S-tZ2SI8UZCcn_lWg0ND2GUjvf423CEKWrg34EAFdxtQN9ENxXIhPJeajGXKk4o9kZUJPxdBycC8i0VAqQRzh8hEMNgTKzhcJyc6pT6ZDjlPtcB-o4cEt-xT3igufjO5uOc34p_-y8_s3WM0J1gqsm8BGikA'

header_admin = {
    'Content-Type': 'application_json',
    'Authorization': JWT_ADMIN
}
header_normal_user = {
    'Content-Type': 'application_json',
    'Authorization': JWT_NORMAL_USER
}


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:131252118@{}/{}".format(
            'localhost:5432',
            self.database_name
            )
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

    def test_successful_get_questions(self):
        res = self.client().get('/questions?page=1', headers=header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])

    def test_unsuccessful_questions_get_request(self):
        res = self.client().get('/questions?page=100', headers=header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page Not Found')

    def test_successful_get_categories(self):
        res = self.client().get('/categories', headers=header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_unsuccessful_categories_get_request(self):
        res = self.client().get('/categories/10', headers=header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page Not Found')

    def test_successful_questions_delete_request(self):
        question = Question(
            question='Test Question',
            answer='Test answer',
            difficulty=4,
            category=5
            )
        question.insert()
        res = self.client().delete(
            f'/questions/{question.id}',
            headers=header_admin
            )
        data = json.loads(res.data)

        question = Question.query.get(question.id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_unsuccessful_questions_delete_request(self):
        res = self.client().delete('/questions/50', headers=header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_successful_update_question(self):
        update_question = {
            'question': 'Updated Question',
            'answer': 'Updated Anwer',
            'difficulty': 2,
            'category': 3,
        }
        res = self.client().patch(
            '/questions/23', json=update_question,
            headers=header_admin
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_unsuccessful_update_question(self):
        res = self.client().patch('/questions/50', headers=header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_successful_create_question(self):
        test_question = {
            'question': 'Test Question 26',
            'answer': 'Test answer 298',
            'difficulty': 3,
            'category': 2
        }
        res = self.client().post(
            '/questions', json=test_question,
            headers=header_admin
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_unsuccessful_questions_post_request(self):
        test_question = {
            'question': 'Test Question 2',
            'answer': 'Test answer 2'
        }
        res = self.client().post(
            '/questions', json=test_question,
            headers=header_admin
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # RBAC Tests

    def test_delete_question_normal_user(self):
        question = Question(
            question='Test Question',
            answer='Test answer',
            difficulty=4,
            category=5
            )
        question.insert()
        res = self.client().delete(
            f'/questions/{question.id}',
            headers=header_normal_user
            )
        data = json.loads(res.data)

        question = Question.query.get(question.id)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], {
            'code': 'unauthorized',
            'description': 'Permission not found.'
            })

    def test_delete_capstone_admin(self):
        question = Question(
            question='Test Question',
            answer='Test answer',
            difficulty=4,
            category=5
            )
        question.insert()
        res = self.client().delete(
            f'/questions/{question.id}',
            headers=header_admin
            )
        data = json.loads(res.data)

        question = Question.query.get(question.id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
