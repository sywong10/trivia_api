# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

  

GET '/categories'
- Fetch a dictionary of categories, in which key = category id, value = category
- Request Arguments: None
- Returns:  a categories dictionary in which key is category id, value is category name




GET '/questions'
- Fetch a dictionary about questions, including total number of questions, a list of paginated dictionary (default is 10) about each question 
  and a dictionary about questions categories.
- Returns a dictionary which contains:
  - a dictionary of categories, with category id as dictionary key and category name as dictionary value
  - a list of questions in dictionary.  containing 10 dictionary of questions in each paginated page
  - a number of total questions



POST '/questions'
- $ curl -X POST -H "Content-Type: application/json" http://localhost:5000/questions -d '{"question":"new question", "answer":"new answer", "category": "2", "difficulty":"2"}'
- Post, add a new question
- Argument: the endpoint takes question, answer, category id and difficulty
- Return an object of newly added question id and question category id 
  {
    "created": 32,
    "questions category": 2,
    "success": true
   }




DELETE '/questions/<question_id>'
- $ curl -X DELETE -H "Content-Type: application/json" http://localhost:5000/questions/32
- remove a question
- Return object contains question id of removed question
  {
    "id": "32",
    "success": true
  }




POST '/questions/search'
- $ curl -X POST -H "Content-Type: application/json" http://localhost:5000/questions/search -d '{"searchTerm":"who"}'
- Argument, the endpoint takes argument of a case insensitive search string
- Return an object including a list of question dictionary and total number of questions that contain search term.
  {
    "current_category": null,
    "questions": [
      {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
      },
      {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
      }
    ],
    "success": true,
    "total_questions": 2
  }




GET '/categories/<id>/questions'
- $ curl http://localhost:5000/categories/4/questions
- the endpoint takes category ID of interested category, it retrieves questions by category ID
- return an object that includes selected category name, total number of questions in this category and an array of question dictionaries in this category.
  {
    "current_category": "History",
    "questions": [
      {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
      },
      {
        "answer": "Scarab",
        "category": 4,
        "difficulty": 4,
        "id": 23,
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
      }
    ],
    "success": true,
    "total_questions": 2
  }




- POST '/quizzes'
- Request Body:
  {
    'previous_questions': [22, 20],
    'quiz_category': a string of the current category
  }

- return the new question object
  {
    'question': {
      'id': 22, 
      'question': 'Hematology is a branch of medicine involving the study of what?', 
      'answer': 'Blood', 
      'category': 1, 
      'difficulty': 4
    }
  }



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
