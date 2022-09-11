# garena-entry-task
This is entry-task repository for garena. It simulates backend for a game where there will be some user that can register, login, input referral code from another user and many more! Created using django and django redis for caching.

## Documentation
It consist of 6 endpoints
1. `POST /api/register`
  - User can register to the system by providing
    - name
    - email
    - username
    - password
2. `POST /api/login`
  - User can login and be responded by the jwt token. Just provide matching name and password.
    - name
    - password
3. `GET /api/heroes`
  - User can get list of all heroes provided by the game. User also can search the heroes by providing `query params` and will get returned heroes. This endpoint is cached using django-redis-cache
4. `GET /api/find_user`
  - User can search others username that registered in the system by providing `query params` with search value 
5. `POST /api/input_ref`
  - User can input referral code from others users. This endpoint is protected so only user who have login can access this endpoint
    - ref_code
6. `PUT /api/edit_profile`
  - User can edit their profile by providing the same field from register except password. 
    - name
    - email
    - username
  - All the field is optional and user only need to provide matching field to change it. `e.g. if user input name field, that means user want to change name attribute`
  
All request and response should be type of `applicaton/json`

## Technologies Used
- python
- virtualenv
- django
- django-redis-cache
- pyjwt

## How to use
1. Install python from `https://www.python.org/downloads/`
1. Clone the repo `git clone https://github.com/IloveNooodles/garena-entry-task.git` 
1. Install virtualenv `pip install virtualenv`
1. Activate the virtualenv. Please refer to [this](https://virtualenv.pypa.io/en/latest/) to activate virtualenv
1. Install all requirement `pip install -r requirements.txt`
1. To run migrations run `python manage.py migrate`
1. To run the server run `python manage.py runserver`
