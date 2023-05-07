"""The Endpoints to manage the BOOK_REQUESTS"""
import json
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint, g, current_app
from flask_mysqldb import MySQL
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)



# from validate_email import validate_email
REQUEST_API = Blueprint('request_api', __name__)
auth = HTTPBasicAuth()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/storage', methods=['GET'])
@auth.login_required
def get_storage():
    """Get all storages information
    @param none
    @return: 200: a list of storages in json format
    @raise 404: no raise
    """
    
    c = g.mysql_db.cursor()
    # c.execute("select * from storage")
    data = query_result_to_json(c, "select * from STORAGE")
    c.close()
    print(data)
    return jsonify(data)

@REQUEST_API.route('/storage/<string:_id>', methods=['GET'])
@auth.login_required
def get_storage_byID(_id):
    
    c = g.mysql_db.cursor()
    data = query_result_to_json(c, "select * from STORAGE where strg_id = {}".format(_id), one=True)
    c.close()
    print(data)
    return jsonify(data)

@REQUEST_API.route('/storage', methods=['POST'])
@auth.login_required
def create_storage():
    """Create a Storage record
    @param email: post : the requesters email address
    @param title: post : the title of the book requested
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    table = 'STORAGE'
    if data.get('strg_id') is not None:
        data.pop('strg_id')    
    c = g.mysql_db.cursor()
    try:
       id = insert_db(c, data, table)
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify({'strg_id': id})


@REQUEST_API.route('/storage/<string:_id>', methods=['PUT'])
@auth.login_required
def edit_storage(_id):


    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if data.get('strg_id') is not None:
        print('deleting strg_id')
        data.pop('strg_id')

    table = 'STORAGE'
 
    c = g.mysql_db.cursor()
    try:
       update_db(c, data, table, "strg_id={}".format(_id))
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify(data)

@REQUEST_API.route('/storage/<string:_id>', methods=['DELETE'])
@auth.login_required
def delete_storage(_id):

    table = 'STORAGE'
 
    c = g.mysql_db.cursor()
    try:
       delete_db(c, table, "strg_id={}".format(_id))
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify({"status": "OK"}), 200

@REQUEST_API.route('/storage/<string:_id>/vehicles', methods=['GET'])
@auth.login_required
def storage_vehicles(_id):
    c = g.mysql_db.cursor()
    q= """select c.car_id, c.VIN, c.color, c.arrival_date, c.model
                    from CAR c, `STORED` s
                    where c.car_id = s.car_id 
                    and s.strg_id = {} """.format(_id)

    data = query_result_to_json(c, q)
    c.close()

    return jsonify(data)


@REQUEST_API.route('/task', methods=['POST'])
@auth.login_required
def create_tasks():
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    data
    table = 'TASK'
    if data.get('task_id') is not None:
        data.pop('task_id')
    c = g.mysql_db.cursor()
    try:
       id = insert_db(c, data, table)
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify({'task_id': id})

@REQUEST_API.route('/task', methods=['GET'])
@auth.login_required
def get_task():

    c = g.mysql_db.cursor()
    q= "select * from TASK" 

    data = query_result_to_json(c, q)
    c.close()

    return jsonify(data)

@REQUEST_API.route('/task/<string:_id>', methods=['PUT'])
@auth.login_required
def edit_task(_id):


    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if data.get('task_id') is not None:
        print('deleting strg_id')
        data.pop('task_id')
    table = 'TASK'
 
    c = g.mysql_db.cursor()
    try:
       update_db(c, data, table, "task_id={}".format(_id))
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify(data)

@REQUEST_API.route('/task/<string:_id>', methods=['DELETE'])
@auth.login_required
def delete_task(_id):

    table = 'TASK'
 
    c = g.mysql_db.cursor()
    try:
       delete_db(c, table, "task_id={}".format(_id))
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify({"status": "OK"}), 200


### --- ROUTINE:


@REQUEST_API.route('/routine', methods=['POST'])
@auth.login_required
def create_routine():
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    tasks = data.get('tasks')
    table = 'ROUTINE'
    del data['tasks']


    c = g.mysql_db.cursor()
    try:
       id = insert_db(c, data, table)
       for task in tasks: 
           insert_db(c, {'rtn_id': id, 'task_id': task}, 'rtn_tsk')
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify({'rtn_id': id})

@REQUEST_API.route('/routine', methods=['GET'])
@auth.login_required
def get_routine():

    c = g.mysql_db.cursor()
    q= "select * from ROUTINE" 

    data = query_result_to_json(c, q)
    c.close()

    return jsonify(data)

@REQUEST_API.route('/routine/<string:_id>', methods=['GET'])
@auth.login_required
def get_routine_id(_id):

    c = g.mysql_db.cursor()
    q= "select * from ROUTINE where rtn_id={}".format(_id)

    data = query_result_to_json(c, q)
    data = data[0]
    print(data)
    q= """select * from TASK t, rtn_tsk rt 
            where rt.rtn_id = {}
            and t.task_id = rt.task_id ;""".format(_id)
    tasks = query_result_to_json(c, q)
    data['tasks'] = tasks


    c.close()

    return jsonify(data)


@REQUEST_API.route('/routine/<string:_id>', methods=['PUT'])
@auth.login_required
def edit_routine(_id):


    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if data.get('rtn_id') is not None:
        data.pop('rtn_id')
    table = 'ROUTINE'
 
    c = g.mysql_db.cursor()
    try:
       update_db(c, data, table, "rtn_id={}".format(_id))
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify(data)

@REQUEST_API.route('/routine/<string:_id>', methods=['DELETE'])
def delete_routine(_id):

    table = 'ROUTINE'
 
    c = g.mysql_db.cursor()
    try:
       delete_db(c, table, "rtn_id={}".format(_id))
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify({"status": "OK"}), 200


### _____ Job services: 

## the service should look for all cars in a storage 
## and find the latest tasks was done on each car 
## and based on the task frequency.. the new job should be activated 
# for example; if a car has no job log then all tasks are due today. 
# if the job log was found and done today; then the new job 
# should be due today+frequency 

@REQUEST_API.route('/jobs', methods=['GET'])
@auth.login_required
def get_jobs():
    c = g.mysql_db.cursor()
    rtn_q = "select rtn_id from `ROUTINE` r where r.model = 'GM_ALL' "
    rtn_id = query_result_to_json(c, rtn_q, one=True)['rtn_id']
   
    _id = g.user[0]['strg_id'] ## user = (user, token)
    q= """select c.car_id, c.VIN, c.color, c.arrival_date, c.model
                    from CAR c, `STORED` s
                    where c.car_id = s.car_id 
                    and s.strg_id = {} """.format(_id)


    cars = query_result_to_json(c, q)
    print('getting user cars')

    for idx, car in enumerate(cars):
        due = None
        lst_car_log = None
        q= """select * from TASK t, rtn_tsk rt 
            where rt.rtn_id = {}
            and t.task_id = rt.task_id ;""".format(rtn_id)
        tasks = query_result_to_json(c, q)
        for task in tasks:
            q = """select * from CAR_LOG cl 
                    where task_id = {}
                    and car_id = {} 
                    ORDER BY cl.task_date  DESC;""".format(task['task_id'], car['car_id'])
            lst_car_log = query_result_to_json(c, q)

            if len(lst_car_log) > 0:
                lst_car_log = lst_car_log[0]
                if  datetime.now() - lst_car_log['task_date'] > timedelta(days=10):
                    due_date = lst_car_log['task_date']+timedelta(days=14)
                    if due is None:
                        due = due_date
                    elif due_date < due:
                        due = due_date
                    task['due_date'] = due_date
                    if car.get('tasks') is not None:
                        car['tasks'].append(task)
                    else:
                        car['tasks'] = [task]
            else:
                task['due_date'] = datetime.now()
                if car.get('tasks') is not None:
                    car['tasks'].append(task)
                else:
                    car['tasks'] = [task]
        car['due_date'] = due
        if car.get('tasks') is None:
            cars.pop(idx)
    c.close()
    return jsonify(cars)

## job log service: 
"""
here the uesr can check in a car or log it in 
"""
@REQUEST_API.route('/check-in', methods=['POST'])
@auth.login_required
def car_check_in():
    c = g.mysql_db.cursor()

    strg_id = g.user[0]['strg_id'] ## user = (user, token)
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    if data.get('car_id') is not None:
        data.pop('car_id')
    table = 'CAR'
    c = g.mysql_db.cursor()
    try:
        id = insert_db(c, data, table)
        insert_db(c, {'car_id': id, 'strg_id': strg_id}, '`STORED`')
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify({'car_id': id})


@REQUEST_API.route('/job_log', methods=['POST'])
@auth.login_required
def log_job():
    
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    user_id = g.user[0]['user_id'] ## user = (user, token)
    car_id = data.get('car_id')
    rtn_id = data.get('rtn_id')
    tasks = data.get('tasks')
    table = 'CAR_LOG'
    c = g.mysql_db.cursor()
    try:
        car_status = True
        for task in tasks: 
            car_log = {
                "car_id": car_id,
                "rtn_id": rtn_id,
                "task_id": task['task_id'],
                "task_value": task['task_value'],
                "notes": task['notes'],
                "user_id": user_id,
                "task_status": task['task_status'],
                "task_date": datetime.now()
            }
            if task['task_status'] is False:
                car_status= False
            id = insert_db(c, car_log, table)
            if task['pictures'] is not None:
                for pic in task['pictures']:
                    insert_db(c, {'log_id': id, 'image': pic}, '`CAR_LOG_PICS`')
        update_db(c, {"status": car_status}, "CAR", "car_id={}".format(car_id))
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify({'car_id': id})

  


## user service: 
@REQUEST_API.route('/user', methods=['GET'])
@auth.login_required
def get_users():

    c = g.mysql_db.cursor()
    q= "select * from USER" 

    data = query_result_to_json(c, q)
    c.close()

    return jsonify(data)

@REQUEST_API.route('/user', methods = ['POST'])
@auth.login_required
def new_user():
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    strg_id = data.get('strg_id')
    if username is None or password is None or email is None:
        abort(400) # missing arguments
    c = g.mysql_db.cursor()
    
    user = get_user(c, username)
    if user is not None:
        abort(400) # existing user
        
    user = {"username": username, 
            "email": email,
            "password": hash_password(password),
            "strg_id": strg_id}
    user = insert_db(c, user, "USER")
    g.mysql_db.commit()
    c.close()
    return jsonify(user)


@REQUEST_API.route('/user/<string:_id>', methods=['PUT'])
@auth.login_required
def edit_user(_id):

    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    strg_id = data.get('strg_id')

    if username is None or password is None or email is None:
        abort(400) # missing arguments

    if data.get('user_id') is not None:
        data.pop('user_id')
    user = {"username": username, 
            "email": email,
            "password": hash_password(password),
            "strg_id": strg_id}
    table = 'USER'
 
    c = g.mysql_db.cursor()
    try:
       update_db(c, user, table, "user_id={}".format(_id))
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify({'message': 'ok'})


@REQUEST_API.route('/user/<string:_id>', methods=['DELETE'])
def delete_user(_id):

    table = 'USER'
 
    c = g.mysql_db.cursor()
    try:
       delete_db(c, table, "user_id={}".format(_id))
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify({"status": "OK"}), 200


@REQUEST_API.route('/login', methods = ['GET'])
@auth.login_required
def get_auth_token():
    return jsonify({ 'token': g.user[1].decode('ascii') })


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    c = g.mysql_db.cursor()
    user = verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = get_user(c, username_or_token)
        if not user or not pwd_context.verify(password, user['password']):
            print('user not found')
            return False
    token = generate_auth_token(username_or_token)
    g.user = (user, token)
    print(user['username'])

    return True

def generate_auth_token(username, expiration = 600):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
    return s.dumps({ 'id': username })

@staticmethod
def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    user = None #"user" #User.query.get(data['id'])
    return user



def check_password():
    pass

def get_user(c, username):

    q_user_exist = """select * from USER
                        where username = '{}';""".format(username) 

    user = query_result_to_json(c, q_user_exist, one=True)
    return user
    
### _____-------------------_____

def query_result_to_json(cur, query, args=(), one=False):
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    return (r[0] if r else None) if one else r

def insert_db(c, data, table):
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)
    print(sql)
    # valid in Python 3
    c.execute(sql, list(data.values()))
    id = c.lastrowid
    return id

def update_db(c, data, table, cond):
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = 'UPDATE {} SET {} WHERE {}'.format(table,
    ', '.join('{}="{}"'.format(k,v) for k, v in data.items()),
    cond)
    print(sql)

    # valid in Python 3
    c.execute(sql)

def delete_db(c, table, cond):
    sql = 'DELETE FROM {}  WHERE {}'.format(table, cond)
    print(sql)
    # valid in Python 3
    c.execute(sql)


def hash_password(password):
    return pwd_context.encrypt(password)

def verify_password(password, password_hash):
    return pwd_context.verify(password, password_hash)

