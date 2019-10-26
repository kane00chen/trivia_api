import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  '''
  Create paginations.
  '''
  page = request.args.get('page', 1, type=int)
  start = (page -1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  '''
  Create and configure the app.
  '''
  app = Flask(__name__, instance_relative_config=True)
  setup_db(app)
  
  '''
  Format the categories to fit JS needs.
  '''
  categories_query = Category.query.all()
  categories = {}
  for category in categories_query:
    cat ={}
    cat[category.id] = category.type
    categories.update(cat)
    


  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  Sorry, I don't know how to let 'cors' work.
  '''
  #cors = CORS(app, resources={r"*/api/*": {"origins": "*"}})
  
  @app.after_request
  def after_request(response):
    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, True')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  @app.route('/categories', methods=['GET'])
  def get_categories():
    '''
    Handle GET requests for all available categories.
    '''
    categories = Category.query.all()

    if len(categories) == 0:
      abort(404)

    formatted_categories = [category.format() for category in categories]

    return jsonify({
      'success': True,
      'categories': formatted_categories
    })

  
  @app.route('/questions', methods=['GET', 'POST'])
  def get_search_qustions():
    '''
    If the request.method is POST, then get questions based on a search term. 
    Return any questions for whom the search term is a substring of the question. 
    
    And if the request.method is GET, then get all questions in database, 
    including pagination (every 10 questions). 
 
    PROBLEM!
    The pagination is not visable although the curl test is right. 
    Please help. Thanks a lot!
    '''
    if request.method == 'POST':
      body = request.get_json()

      if 'searchTerm' in body:  
        search_item = '%' + body['searchTerm'] + '%'
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike(search_item)).all()
        current_questions = paginate_questions(request, selection)

      else:
        abort(404)

    else:
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'totalQuestions': len(selection),
      'categories': categories
    })

    
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    '''
    DELETE question using a question ID. 

    TESTED: When click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    question = Question.query.filter(Question.id == question_id).one_or_none()

    if question == None:
      abort(404)

    else:
      question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id,
        'totalQuestions': len(Question.query.all()),
      })

  @app.route('/add', methods=['POST'])
  def create_new_question():
    '''
    POST a new question which requires the question and answer text, 
    category, and difficulty score.

    TESTED: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    body = request.get_json()

    if body.get('question') == '' or body.get('answer') == '':
      abort(422)

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = int(body.get('category', None)) + 1
    new_diffidulty = body.get('difficulty', None)    
    
    try:
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_diffidulty)
      question.insert()
      
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)

  @app.route('/categories/<int:category_id>', methods=['GET'])
  def get_category_qustions(category_id):
    '''
    Get questions based on category. 

    TESTED: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    page = request.args.get('page', 1, type=int)
    selection = Question.query.filter(Question.category==category_id).order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'page': page,
      'totalQuestions': len(selection),
      'currentCategory': category_id,
    })

  @app.route('/play', methods=['GET'])
  def choose_category():
    '''
    GET requests for all available categories.     

    TEST: In the "Play" tab, display categories, after a user selects "All" or a category,
    turn to question_quiz form.
    '''    
    return jsonify({
      'success': True,
      'categories': categories
    })

  @app.route('/play/getnextquestion', methods=['POST'])
  def get_next_question():
    '''
    Display a random question within the given category, 
    if provided, and that is not one of the previous questions. 

    TESTED:One question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    body = request.get_json()
    previous_questions = body.get('previous_questions', None)
    get_category_id = body.get('quiz_category', None).get('id', None)

    category_id = int(get_category_id)

    if category_id == 0:
      questions = Question.query.filter(~Question.id.in_(previous_questions)).all()

    else:
      questions = Question.query.filter(Question.category==category_id, ~Question.id.in_(previous_questions)).all()
    
    formatted_questions = [question.format() for question in questions]
    total_remained_questions = len(formatted_questions)

    if total_remained_questions != 0:
      random_num = random.randint(0,total_remained_questions-1)
      question = formatted_questions[random_num]

    else:
      question = None

    return jsonify({
        'success': True,
        'question': question,
      })


  @app.errorhandler(400)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(405)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(500)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
    }), 500
   
   
  return app

    