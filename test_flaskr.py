import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from app import create_app
from models import setup_db, Question, Category

JWT_ADMIN = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IndUT3NzelNiOEswQ01NdlRzQlJ6SSJ9.eyJpc3MiOiJodHRwczovL21rZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0NGQ3YjRiNWQzOWQwMDcwNDg0NzQ2IiwiYXVkIjoiY2Fwc3RvbmV0ZXN0IiwiaWF0IjoxNjE2NjAxMDg5LCJleHAiOjE2MTY2MDgyODksImF6cCI6Iml0WlhEd1F4OVlHMkpOUDlYSlFybmRpZTc5SXE5ZmcyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6cXVlc3Rpb25zIiwiZ2V0OmNhdGVnb3JpZXMiLCJnZXQ6cXVlc3Rpb25zIiwicGF0Y2g6cXVlc3Rpb25zIiwicG9zdDpxdWVzdGlvbnMiXX0.c62ikJ4tVsNxBbyeNjQBhtbvW_x3nYp2Fxte_A7JP1MWL82csp7QcdAEd5cx-WfJzyvrzsRGvjROyRPVz97BzYRREfeYKU0LY7AIxIeZvDNK3H1RIfzC_vyY2gKIOc6zf5EsVpjAcGkAi0HtIJRahTR58cZhC-eh8wpALrpYh1GKC7k1itoRchFo2CrtiH5PHaapps1Nm5SJFkHfadB_TJsfzfJuMm27pp8Mhbsn2vT7MLHAt8Hup5CG5dwixyK90AVh77NhcZ-2IAe7p2830Lt5LS3Na2EGz_4Wsokspb-qPpN0N601RdMXSomV7OMQQLh1yIAtZ_6akxcLFy__7g'
JWT_NORMAL_USER = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IndUT3NzelNiOEswQ01NdlRzQlJ6SSJ9.eyJpc3MiOiJodHRwczovL21rZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1MjBjYTdmYjM4MDMwMDY4MTM0MGJjIiwiYXVkIjoiY2Fwc3RvbmV0ZXN0IiwiaWF0IjoxNjE2NjAxMjIzLCJleHAiOjE2MTY2MDg0MjMsImF6cCI6Iml0WlhEd1F4OVlHMkpOUDlYSlFybmRpZTc5SXE5ZmcyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6Y2F0ZWdvcmllcyIsImdldDpxdWVzdGlvbnMiXX0.dXYa-njhCrvjWCYkHQAkg4ti8cz5U68bvy--myij0OzWVb4hvcAdjmiNI82nReNZNlfoWP9ZVts09yiWCjrzfn1a2yQMsHi26wkoi1pkzixU-4mp0bzKlTnD5dWmT_pTdghQYHul64oCOTvgkSHLORmMfY9exLdPs0gU0qz5MClrwDpJon-Se3LKdzNDN7BNzIB6YEtG_cOFP-YsEVQx9xFI_i4kM6GjQD5xGpybzZh5d7_H4pluwZh8uK3sjQSTgjAQJvfNoAtG0AOB5oGvik0pZ8eNdBmjgNASULbrZq8PZp1phCO9NsySxa8lE8ykMP8elgtpsY0EBzaQEEytXA'

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
