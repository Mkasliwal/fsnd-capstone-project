import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
import json

from models import setup_db, Question, Category
from auth import AuthError, requires_auth

QUESTIONS_PER_PAGE = 10


def paginate(request, data):
    limit_rows = request.args.get('limit', QUESTIONS_PER_PAGE, type=int)
    selected_page = request.args.get('page', 1, type=int)
    current_index = selected_page - 1
    filteredData = data.limit(limit_rows).offset(
        current_index * limit_rows).all()
    transformedData = [el.format() for el in filteredData]
    return transformedData


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization'
            )
        response.headers.add(
            'Access-Control-Allow-Headers',
            'GET, POST, PATCH, DELETE, OPTIONS'
            )
        return response


    @app.route('/')
    def index():
        return '<h1>Hi there...!!</h1>'

    # GET Request 1
    @app.route('/categories')
    @requires_auth('get:categories')
    def get_categories(jwt):
        err = False
        try:
            categories = Category.query.all()
            if len(categories) == 0:
                err = True
        except Exception as error:
            err = True
            print('Error Occured: {}', format(error))
        finally:
            if not err:
                return jsonify({
                    'success': True,
                    'categories': {
                        category.id: category.type for category in categories
                        }
                })
            else:
                abort(404)

    # GET Request 2
    @app.route('/questions')
    # @requires_auth('get:questions')
    def get_data():
        err = False
        try:
            questions = Question.query.order_by(Question.id)
            formatedQuestion = paginate(request, questions)
            categories = Category.query.all()
            if len(formatedQuestion) == 0:
                err = True
        except Exception as error:
            err = True
            print(sys.exc_info())
            print('Error Occured: {}', format(error))
        finally:
            if not err:
                return jsonify({
                    'success': True,
                    'questions': formatedQuestion,
                    'categories': {
                        category.id: category.type for category in categories
                        },
                    'total_questions': len(questions.all()),
                    'currentCategory': None
                })
            else:
                abort(404)

    # DELETE Request
    @app.route('/questions/<id>', methods=['DELETE'])
    @requires_auth('delete:questions')
    def delete_question_by_id(jwt, id):
        err = False
        try:
            question = Question.query.get(id)
            if question:
                question.delete()
            else:
                err = True
        except Exception as error:
            err = True
            print('Error Occured: {}', format(error))
        finally:
            if not err:
                return jsonify({
                    'success': True,
                    'question': question.id
                })
            else:
                abort(422)

    # POST Request
    @app.route('/questions', methods=['POST'])
    @requires_auth('post:questions')
    def create_question(jwt):
        body = request.get_json()
        print(body)
        formData = Question(
          question=body.get('question'),
          answer=body.get('answer'),
          difficulty=body.get('difficulty'),
          category=body.get('category'),
        )
        err = False
        try:
            if (
                'question' in body and
                'answer' in body and
                'difficulty' in body and
                'category' in body
            ):
                formData.insert()
            else:
                err = True
        except Exception as error:
            err = True
            print('Error Occured: {}', format(error))
        finally:
            if not err:
                return jsonify({
                    'success': True,
                })
            else:
                abort(422)

    # PATCH Request
    @app.route('/questions/<int:id>', methods=['PATCH'])
    @requires_auth('patch:questions')
    def update_drink(jwt, id):
        body = request.get_json()
        print(body)
        try:
            update_question = Question.query.get(id)

            update_question.question = body.get('question')
            update_question.answer = body.get('answer')
            update_question.difficulty = body.get('difficulty')
            update_question.category = body.get('category')

            update_question.update()
            return jsonify({
                'success': True,
            })
        except Exception as error:
            abort(422)
            print(error)

    @app.errorhandler(400)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Permission Not Found in JWT'
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Page Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422
    return app

    @app.errorhandler(500)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Something went wrong at server/application'
        }), 500


app = create_app()
