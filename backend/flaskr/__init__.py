import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def pagination(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = page * QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions



def create_app(test_config=None):
  # create and configure the app

  # try:
  #   os.makedirs(app.instance_path)
  # except OSError:
  #   pass

  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass



  setup_db(app)
  CORS(app, resources={r"/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
    return response


  @app.route('/categories', methods=['GET'])
  def get_categories():

    categories = Category.query.order_by(Category.id).all()
    formatted_categories = {}

    for category in categories:
      formatted_categories[category.id] = category.type

    return jsonify({
      'Success': True,
      'categories': formatted_categories,
      'total_categories': len(categories)
    })


  @app.route('/questions', methods=['GET'])
  def get_questions():

    selection = Question.query.order_by(Question.id).all()
    current_questions = pagination(request, selection)

    categories = Category.query.all()
    formatted_categories={}

    for category in categories:
      formatted_categories[category.id] = category.type

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'categories': formatted_categories,
      'total_questions': len(selection),
      'current_category': None
    })


  @app.route('/questions', methods=['POST'])
  def add_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    try:
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = pagination(request, selection)

      return jsonify({
        'success': True,
        'created': question.id,
        'questions category': question.category
      })

    except:
      abort(402)



  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):

    delete_question = Question.query.filter_by(id=question_id).first()

    if not delete_question:
      abort(404)

    try:
      Question.delete(delete_question)
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()

    return jsonify({
      'id': question_id,
      'success': True
    }), 200


  @app.route('/questions/search', methods=['POST'])
  def search_question():

    data = request.get_json()
    search_term = data.get('searchTerm', '')

    if search_term:
      results = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
      formatted_result_questions = [ search.format() for search in results ]

      return jsonify({
        'success': True,
        'questions': formatted_result_questions,
        'total_questions': len(results),
        'current_category': None
      })

    else:
      abort(404)
      # results = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
      # formatted_result_questions = [search.format() for search in results]
      #
      # return jsonify({
      #   'success': True,
      #   'questions': formatted_result_questions,
      #   'total_questions': len(results),
      #   'current_category': None
      # })

      # abort(404)

    # return jsonify ({
    #   'success': True,
    #   'questions': formatted_result_questions,
    #   'total_questions': len(results),
    #   'current_category': None
    # })




  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def list_questions_by_category(id):
    try:
      questions_by_category = Question.query.filter(Question.category==str(id)).all()
      formatted_questions_by_category = [ question.format() for question in questions_by_category]
      current_category = Category.query.filter(Category.id==str(id)).first()

      return jsonify({
        'success': True,
        'questions': formatted_questions_by_category,
        'total_questions': len(questions_by_category),
        'current_category': current_category.type
      })

    except:
      abort(404)



  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    data = request.get_json()
    next_question = None
    previous_questions = data.get('previous_questions')
    category = data.get('quiz_category')

    try:
      if category.get('id', None) != 0:
        selection = Question.query.filter(Question.category==category.get('id')).all()
      else:
        selection = Question.query.all()

      all_questions = [ question.format() for question in selection if question.id not in previous_questions]

      if len(all_questions) != 0:
        question_to_ask = random.choice(all_questions)

    except:
      abort(422)

    return jsonify({
      'success': True,
      'id': category,
      'question': question_to_ask
    })



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable_entity"
    }), 422


  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "Success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405


  return app

    