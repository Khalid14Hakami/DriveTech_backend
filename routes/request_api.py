"""The Endpoints to manage the BOOK_REQUESTS"""
import json
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint, g
from flask_mysqldb import MySQL



from validate_email import validate_email
REQUEST_API = Blueprint('request_api', __name__)



def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


BOOK_REQUESTS = {
    "8c36e86c-13b9-4102-a44f-646015dfd981": {
        'title': u'Good Book',
        'email': u'testuser1@test.com',
        'timestamp': (datetime.today() - timedelta(1)).timestamp()
    },
    "04cfc704-acb2-40af-a8d3-4611fab54ada": {
        'title': u'Bad Book',
        'email': u'testuser2@test.com',
        'timestamp': (datetime.today() - timedelta(2)).timestamp()
    }
}


@REQUEST_API.route('/request', methods=['GET'])
def get_records():
    """Return all book requests
    @return: 200: an array of all known BOOK_REQUESTS as a \
    flask/response object with application/json mimetype.
    """
    c = g.mysql_db
    c.execute("select * from car")
    data = c.fetchall()
    print("لا يشيخ")
    c.close()
    print(data)
    return jsonify(data)


@REQUEST_API.route('/request/<string:_id>', methods=['GET'])
def get_record_by_id(_id):
    """Get book request details by it's id
    @param _id: the id
    @return: 200: a BOOK_REQUESTS as a flask/response object \
    with application/json mimetype.
    @raise 404: if book request not found
    """
    if _id not in BOOK_REQUESTS:
        abort(404)
    return jsonify(BOOK_REQUESTS[_id])


@REQUEST_API.route('/request', methods=['POST'])
def create_record():
    """Create a book request record
    @param email: post : the requesters email address
    @param title: post : the title of the book requested
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('email'):
        abort(400)
    if not validate_email(data['email']):
        abort(400)
    if not data.get('title'):
        abort(400)

    new_uuid = str(uuid.uuid4())
    book_request = {
        'title': data['title'],
        'email': data['email'],
        'timestamp': datetime.now().timestamp()
    }
    BOOK_REQUESTS[new_uuid] = book_request
    # HTTP 201 Created
    return jsonify({"id": new_uuid}), 201


@REQUEST_API.route('/request/<string:_id>', methods=['PUT'])
def edit_record(_id):
    """Edit a book request record
    @param email: post : the requesters email address
    @param title: post : the title of the book requested
    @return: 200: a booke_request as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if _id not in BOOK_REQUESTS:
        abort(404)

    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('email'):
        abort(400)
    if not validate_email(data['email']):
        abort(400)
    if not data.get('title'):
        abort(400)

    book_request = {
        'title': data['title'],
        'email': data['email'],
        'timestamp': datetime.now().timestamp()
    }

    BOOK_REQUESTS[_id] = book_request
    return jsonify(BOOK_REQUESTS[_id]), 200


@REQUEST_API.route('/request/<string:_id>', methods=['DELETE'])
def delete_record(_id):
    """Delete a book request record
    @param id: the id
    @return: 204: an empty payload.
    @raise 404: if book request not found
    """
    if _id not in BOOK_REQUESTS:
        abort(404)

    del BOOK_REQUESTS[_id]

    return '', 204


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
    q= """select c.car_id, c.VIN, c.color, c.arraival_date 
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