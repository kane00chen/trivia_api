# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, '''bash http://127.0.0.1:5000/''', which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

'''
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
'''

The API will return two error types when requests fail:

- 400: bad request
- 404: resource Not Found
- 405: method not allowed
- 422: unprocessable
- 500: internal server error

### Endpoints

#### GET '/categories'

- Fetches a list of dictionaries of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None
- Returns: A list of dictionaries of categories. Each dictionary has two keys. One key is 'id', the value is the id number. The other key is 'type', value is category_string.
'''
C:\>curl http://127.0.0.1:5000/categories
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true
}
'''

#### GET & POST '/questions'

- If the method is 'GET', the API fetches all questions in the database. 
- Request Arguments: None
- Returns: A pagenationary of questions list , dictionary of categories , number of total questions and 'success'= True.
'''
C:\>curl http://127.0.0.1:5000/questions
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "answer1",
      "category": 1,
      "difficulty": 5,
      "id": 1,
      "question": "question1"
    },
    {
      "answer": "Tom Cruise",
      "category": 4,
      "difficulty": 5,
      "id": 3,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 2,
      "difficulty": 4,
      "id": 4,
      "question": "Whose autobiography is entitled <I Know Why the Caged Bird Sings>?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 3,
      "difficulty": 5,
      "id": 5,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 1,
      "difficulty": 4,
      "id": 7,
      "question": "What boxer`s original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 3,
      "difficulty": 6,
      "id": 8,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 4,
      "difficulty": 6,
      "id": 9,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 2,
      "difficulty": 4,
      "id": 10,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 2,
      "difficulty": 3,
      "id": 11,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 12,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "totalQuestions": 28
}
'''

- If the method is 'POST', the API starts a search by the input. 
- Request Arguments: searchTerm
- Returns: A pagenationary of questions list insensibly include the given searchTerm, dictionary of categories , number of total questions in the search results and 'success'= True.
'''
C:\>curl -X POST -H "Content-Type:application/json" -d "{\"searchTerm\": \"title\"}" http://127.0.0.1:5000/questions
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 2,
      "difficulty": 4,
      "id": 4,
      "question": "Whose autobiography is entitled <I Know Why the Caged Bird Sings>?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 3,
      "difficulty": 5,
      "id": 5,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "totalQuestions": 2
}
'''

#### GET '/categories/<int:id>'

- Fetches all questions in a category.
- Request Arguments: Category_id(from 1 to 6).
- Returns: A list of dictionaries of questions. Also returns currentCategory, current page, total questions based by current category and success info.
'''
C:\>curl http://127.0.0.1:5000/categories/1
{
  "currentCategory": 1,
  "page": 1,
  "questions": [
    {
      "answer": "answer1",
      "category": 1,
      "difficulty": 5,
      "id": 1,
      "question": "question1"
    },
    {
      "answer": "Muhammad Ali",
      "category": 1,
      "difficulty": 4,
      "id": 7,
      "question": "What boxer`s original name is Cassius Clay?"
    },
    {
      "answer": "Escher",
      "category": 1,
      "difficulty": 2,
      "id": 14,
      "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "totalQuestions": 3
}
'''

#### GET '/categories/<int:category_id>'

- Fetches all questions in a category.
- Request Arguments: category_id(from 1 to 6).
- Returns: A list of dictionaries of questions. Also returns currentCategory, current page, total questions based by current category and success info.
'''
C:\>curl http://127.0.0.1:5000/categories/1
{
  "currentCategory": 1,
  "page": 1,
  "questions": [
    {
      "answer": "answer1",
      "category": 1,
      "difficulty": 5,
      "id": 1,
      "question": "question1"
    },
    {
      "answer": "Muhammad Ali",
      "category": 1,
      "difficulty": 4,
      "id": 7,
      "question": "What boxer`s original name is Cassius Clay?"
    },
    {
      "answer": "Escher",
      "category": 1,
      "difficulty": 2,
      "id": 14,
      "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "totalQuestions": 3
}
'''

#### DELETE '/questions/<int:question_id>'

- Delete a question by the question_id.
- Request Arguments: question_id
- Returns: Deleted question id, remained total questions number and success info.
'''
C:\>curl -X DELETE http://127.0.0.1:5000/questions/37
{
  "deleted": 37,
  "success": true,
  "totalQuestions": 27
}
'''

#### POST '/add'

- Create a new question by inputtings of question and answer text, category, and difficulty score.
- Request Arguments: question, answer, category, difficulty score
- Returns: Created question id, total questions number after creation, pagenational questions list and success info.
'''
C:\>curl -X POST -H "Content-Type:application/json" -d "{\"question\": \"new question example23\", \"answer\": \"answer of example23\", \"category\": \"5\", \"difficulty\": 4}" http://127.0.0.1:5000/add
{
  "created": 38,
  "questions": [
    {
      "answer": "answer1",
      "category": 1,
      "difficulty": 5,
      "id": 1,
      "question": "question1"
    },
    {
      "answer": "Tom Cruise",
      "category": 4,
      "difficulty": 5,
      "id": 3,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 2,
      "difficulty": 4,
      "id": 4,
      "question": "Whose autobiography is entitled <I Know Why the Caged Bird Sings>?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 3,
      "difficulty": 5,
      "id": 5,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 1,
      "difficulty": 4,
      "id": 7,
      "question": "What boxer`s original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 3,
      "difficulty": 6,
      "id": 8,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 4,
      "difficulty": 6,
      "id": 9,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 2,
      "difficulty": 4,
      "id": 10,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 2,
      "difficulty": 3,
      "id": 11,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 12,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 28
}
'''

#### GET '/play'

- Fetches a dictionary of categories.
- Request Arguments: None
- Returns: A dictionary of categories and success info.
'''
C:\>curl http://127.0.0.1:5000/play
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
'''

#### POST '/play/getnextquestion'

- POST a category id from 0~6, 0 stands for all categories. Returns a random question selected from selected category or all categories till none questions remain.
- Request Arguments: previous_questions, quiz_category.ID
- Returns: A random question selected from selected category/categories till none questions remain. And success info.
'''
C:\>curl -X POST -H "Content-Type:application/json" -d "{\"previous_questions\": [], \"quiz_category\": {\"type\": \"Science\", \"id\": \"1\"}}" http://127.0.0.1:5000/play/getnextquestion
{
  "question": {
    "answer": "Muhammad Ali",
    "category": 1,
    "difficulty": 4,
    "id": 7,
    "question": "What boxer`s original name is Cassius Clay?"
  },
  "success": true
}
'''

## Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```