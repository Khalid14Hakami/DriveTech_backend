"""The Endpoints to manage the BOOK_REQUESTS"""
import json
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint, g
from flask_mysqldb import MySQL



# from validate_email import validate_email
REQUEST_API = Blueprint('request_api', __name__)



def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API



@REQUEST_API.route('/storage/', methods=['GET'])
def get_storage():
    """Get all storages information
    @param none
    @return: 200: a list of storages in json format
    @raise 404: no raise
    """
    
    c = g.mysql_db.cursor()
    # c.execute("select * from storage")
    data = query_result_to_json(c, "select * from storage")
    c.close()
    print(data)
    return jsonify(data)

    return '', 204

@REQUEST_API.route('/storage', methods=['POST'])
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
    table = 'storage'
    del data['strg_id']
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
def edit_storage(_id):


    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if data.get('strg_id') is not None:
        print('deleting strg_id')
        data.pop('strg_id')

    table = 'storage'
 
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
def delete_storage(_id):

    table = 'storage'
 
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
def storage_vehicles(_id):
    c = g.mysql_db.cursor()
    q= """select c.car_id, c.VIN, c.color, c.arraival_date, c.model
                    from CAR c, `STORED` s
                    where c.car_id = s.car_id 
                    and s.strg_id = {} """.format(_id)

    data = query_result_to_json(c, q)
    c.close()

    return jsonify(data)


@REQUEST_API.route('/task/', methods=['POST'])
def create_tasks():
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    data
    table = 'TASK'
    del data['task_id']

    c = g.mysql_db.cursor()
    try:
       id = insert_db(c, data, table)
    except (g.mysql_db.Error, g.mysql_db.Warning) as e:
        print(e)
        return jsonify({"status": "Error", "message": str(e)}), 500

    g.mysql_db.commit()
    c.close()
    return jsonify({'task_id': id})

@REQUEST_API.route('/task/', methods=['GET'])
def get_task():

    c = g.mysql_db.cursor()
    q= "select * from TASK" 

    data = query_result_to_json(c, q)
    c.close()

    return jsonify(data)

@REQUEST_API.route('/task/<string:_id>', methods=['PUT'])
def edit_task(_id):


    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if data.get('task_id') is not None:
        print('deleting strg_id')
        data.pop('task_id')
    table = 'task'
 
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
def delete_task(_id):

    table = 'task'
 
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


@REQUEST_API.route('/routine/', methods=['POST'])
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

@REQUEST_API.route('/routine/', methods=['GET'])
def get_routine():

    c = g.mysql_db.cursor()
    q= "select * from routine" 

    data = query_result_to_json(c, q)
    c.close()

    return jsonify(data)

@REQUEST_API.route('/routine/<string:_id>', methods=['GET'])
def get_routine_id(_id):

    c = g.mysql_db.cursor()
    q= "select * from routine where rtn_id={}".format(_id)

    data = query_result_to_json(c, q)
    data = data[0]
    print(data)
    q= """select * from task t, rtn_tsk rt 
            where rt.rtn_id = {}
            and t.task_id = rt.task_id ;""".format(_id)
    tasks = query_result_to_json(c, q)
    data['tasks'] = tasks


    c.close()

    return jsonify(data)


@REQUEST_API.route('/routine/<string:_id>', methods=['PUT'])
def edit_routine(_id):


    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if data.get('rtn_id') is not None:
        data.pop('rtn_id')
    table = 'routine'
 
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

    table = 'routine'
 
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

@REQUEST_API.route('/jobs/', methods=['GET'])
def get_jobs():

    c = g.mysql_db.cursor()
    rtn_id = 4
    _id = 13
    q= """select c.car_id, c.VIN, c.color, c.arraival_date, c.model
                    from CAR c, `STORED` s
                    where c.car_id = s.car_id 
                    and s.strg_id = {} """.format(_id)


    cars = query_result_to_json(c, q)
    for car in cars:
        lst_car_log = None
        q= """select * from task t, rtn_tsk rt 
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
    c.close()
    return jsonify(cars)





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