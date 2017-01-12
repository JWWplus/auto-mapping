# coding=utf-8
# uwsgi --http :6234 --wsgi-file app.py  --callable app --processes 4
# --threads 1
"""
按照json格式返回的数据一定要是字符串   否则 AngularJs 解析出错
a=datawebunit.datainfo.aggregate([{'$match':{'appversion':"4.13"}},{"$group":{"_id":"$page",'sum':{'$sum':1}}}])
"""
from flask import Flask, request, send_file
from pymongo import MongoClient
import logging
from bson import json_util
from bson import ObjectId
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

# datawebunit = MongoClient('localhost:27017').datawebunit
datawebunit = MongoClient('dataTask01:29017', connect=False).test
app = Flask(__name__)


# 解决跨域问题在返回标头加上
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


"""
该api返回以下信息
GET方式: 获取单条id的信息  用在修改单条数据时获取信息
PUT方式: 修改此id在数据库中的信息
DELETE方式: 删除此id在数据库中的信息
"""


@app.route('/')
def root():
    return send_file("templates/index.html")


@app.route('/api/v1/getinfo/<id_number>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def getinfo_by_id(id_number):
    if request.method == 'GET':
        resp = datawebunit.datainfo.find({"_id": ObjectId(id_number)})[0]
        return json_util.dumps(resp)
    elif request.method == 'PUT':
        data = json.loads(request.data)
        old_content = datawebunit.datainfo.find_one(
            {"_id": ObjectId(id_number)})
        datawebunit.datainfo.update({
            '_id': ObjectId(id_number)
        }, {
            '$set': {
                'appversion': data['appversion'],
                'page': data['page'],
                'platform': data['platform'],
                'pm': data.get('pm', ''),
                'event': data['event'],
                'object': data['object'],
                'page_key': data['page_key'],
                'type': data['type'],
                'sub_type': data['sub_type'],
                'note': data.get('note', ''),
                'se_category': data['se_category'],
                'se_action': data['se_action'],
            }
        })
        datawebunit.log.insert({
            'time': data['time'],
            'username': data['username'],
            'type': data['logtype'],
            'old_content': old_content,
            'new_content': datawebunit.datainfo.find_one({"_id": ObjectId(id_number)}),
            'oid': id_number,
        })
    elif request.method == 'DELETE':
        datawebunit.datainfo.delete_one({
            '_id': ObjectId(id_number)
        })
    return '1'


"""
该api返回以下信息
GET方法: 返回整个数据集的一些信息,目前只返回了总记录数
POST方法: 用于往数据库中增加新的信息
"""


@app.route('/api/v1/getinfo', methods=['GET', 'POST'])
def getinfo():
    if request.method == 'GET':
        app_version = datawebunit.appversion.find()
        resp = {
            'appversion': app_version,
        }
        return json_util.dumps(resp)

    elif request.method == 'POST':
        data = json.loads(request.data)
        if data:
            add_id = datawebunit.datainfo.insert({
                'appversion': data['appversion'],
                'page': data['page'],
                'platform': data['platform'],
                'pm': data.get('pm', ''),
                'event': data['event'],
                'object': data['object'],
                'page_key': data['page_key'],
                'type': data['type'],
                'sub_type': data['sub_type'],
                'note': data.get('note', ''),
                'se_category': data['se_category'],
                'se_action': data['se_action'],
            })

            datawebunit.log.insert({
                'time': data['time'],
                'username': data['username'],
                'type': data['logtype'],
                'old_content': '',
                'new_content': datawebunit.datainfo.find_one({"_id": add_id})
            })
        return '1'


"""
该api返回以下信息
Post方法: 返回对应分页时的记录  有版本选择等等筛选条件
"""


@app.route('/api/v1/getdata', methods=['POST', 'GET'])
def getdata():
    if request.method == 'POST':
        data = json.loads(request.data)
        currentPage = int(data['curPage'])
        numPerPage = int(data['numPerPage'])
        AppVersion = data['AppVersion']
        event = data['event']
        platform = data['platform']
        page = data['page']
        Datainfo = {}

        if not page:
            if AppVersion:
                page_type = datawebunit.datainfo.aggregate([{'$match': {'appversion': AppVersion}}, {
                                                           "$group": {"_id": "$page", 'sum': {'$sum': 1}}}, {'$sort': {'sum': -1}}])
                if platform:
                    if event:
                        count = datawebunit.datainfo.find({
                            'appversion': AppVersion,
                            'event': event,
                            'platform': platform,
                        }).count()
                        resp = datawebunit.datainfo.find({
                            'appversion': AppVersion,
                            'event': event,
                            'platform': platform,
                        }).sort('object', 1).limit(
                            numPerPage).skip((currentPage - 1) * numPerPage)
                    else:
                        count = datawebunit.datainfo.find({
                            'appversion': AppVersion,
                            'platform': platform,
                        }).count()
                        resp = datawebunit.datainfo.find({
                            'appversion': AppVersion,
                            'platform': platform,
                        }).sort('object', 1).limit(
                            numPerPage).skip((currentPage - 1) * numPerPage)
                else:
                    count = datawebunit.datainfo.find({
                        'appversion': AppVersion,
                    }).count()
                    resp = datawebunit.datainfo.find({
                        'appversion': AppVersion,
                    }).sort('object', 1).limit(numPerPage).skip((currentPage - 1) * numPerPage)

            elif not AppVersion and platform:
                page_type = datawebunit.datainfo.aggregate([{'$match': {'platform': platform}}, {
                    "$group": {"_id": "$page", 'sum': {'$sum': 1}}}, {'$sort': {'sum': -1}}])

                count = datawebunit.datainfo.find({
                    'platform': platform,
                }).count()
                resp = datawebunit.datainfo.find({
                    'platform': platform,
                }).sort('object', 1).limit(numPerPage).skip((currentPage - 1) * numPerPage)

            else:
                count = datawebunit.datainfo.count()
                resp = datawebunit.datainfo.find().sort('object', 1).limit(
                    numPerPage).skip((currentPage - 1) * numPerPage)
                page_type = {}

        else:
            if AppVersion:
                page_type = datawebunit.datainfo.aggregate([{'$match': {'appversion': AppVersion}}, {
                                                           "$group": {"_id": "$page", 'sum': {'$sum': 1}}}, {'$sort': {'sum': -1}}])
                if platform:
                    if event:
                        count = datawebunit.datainfo.find({
                            'appversion': AppVersion,
                            'event': event,
                            'platform': platform,
                            'page': page,
                        }).count()
                        resp = datawebunit.datainfo.find({
                            'appversion': AppVersion,
                            'event': event,
                            'platform': platform,
                            'page': page,
                        }).sort('object', 1).limit(
                            numPerPage).skip((currentPage - 1) * numPerPage)
                    else:
                        count = datawebunit.datainfo.find({
                            'appversion': AppVersion,
                            'platform': platform,
                            'page': page,
                        }).count()
                        resp = datawebunit.datainfo.find({
                            'appversion': AppVersion,
                            'platform': platform,
                            'page': page,
                        }).sort('object', 1).limit(
                            numPerPage).skip((currentPage - 1) * numPerPage)
                else:
                    count = datawebunit.datainfo.find({
                        'appversion': AppVersion,
                        'page': page,
                    }).count()
                    resp = datawebunit.datainfo.find({
                        'appversion': AppVersion,
                        'page': page,
                    }).sort('object', 1).limit(
                        numPerPage).skip((currentPage - 1) * numPerPage)

            elif not AppVersion and platform:
                page_type = datawebunit.datainfo.aggregate([{'$match': {'platform': platform}}, {
                    "$group": {"_id": "$page", 'sum': {'$sum': 1}}}, {'$sort': {'sum': -1}}])

                count = datawebunit.datainfo.find({
                    'platform': platform,
                    'page': page,
                }).count()
                resp = datawebunit.datainfo.find({
                    'platform': platform,
                    'page': page,
                }).sort('object', 1).limit(numPerPage).skip((currentPage - 1) * numPerPage)

            else:
                count = datawebunit.datainfo.count()
                resp = datawebunit.datainfo.find().sort('object', 1).limit(
                    numPerPage).skip((currentPage - 1) * numPerPage)
                page_type = {}

        Datainfo = {
            'resp': resp,
            'count': count,
            'page_type': page_type,
        }

        return json_util.dumps(Datainfo)


@app.route('/api/v1/add_version', methods=['POST', 'GET'])
def add_version():
    if request.method == 'POST':
        Data = json.loads(request.data)
        last_version = datawebunit.appversion.find().sort(
            '_id', -1).limit(1)[0]
        datawebunit.appversion.insert({
            'appversion': Data['appversion']
        })
        datawebunit.log.insert({
            'time': Data['time'],
            'username': Data['username'],
            'type': Data['logtype'],
            'old_content': '',
            'new_content': Data['appversion']
        })
        for data in datawebunit.datainfo.find({
            'appversion': last_version['appversion']
        }):
            datawebunit.datainfo.insert({
                'appversion': Data['appversion'],
                'page': data['page'],
                'platform': data['platform'],
                'pm': data.get('pm', ''),
                'event': data['event'],
                'object': data['object'],
                'page_key': data['page_key'],
                'type': data['type'],
                'sub_type': data['sub_type'],
                'note': data.get('note', ''),
                'se_category': data['se_category'],
                'se_action': data['se_action'],
            })
        return '1'


@app.route('/api/v1/login', methods=['POST', 'GET'])
def check_passwd():
    if request.method == 'POST':
        data = json.loads(request.data)
        username = data['username']
        passwd = data['password']
        check_from_db = datawebunit.user.find_one({
            'username': username,
            'password': passwd,
        })
        if check_from_db:
            result = {
                'status': 1,
                'role': check_from_db['role']
            }
        else:
            result = {
                'status': -1,
            }
        return json_util.dumps(result)


# 像数据库插入log记录
@app.route('/api/v1/log_server/<logtype>', methods=['POST', 'GET'])
def LogService(logtype):
    Data = json.loads(request.data)
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        if logtype == 'AddVersion':
            pass
        elif logtype == 'Edit':
            pass
        elif logtype == 'AddData':
            pass
        elif logtype == 'Delete':
            datawebunit.log.insert({
                'time': Data['time'],
                'username': Data['username'],
                'type': Data['logtype'],
                'old_content': datawebunit.datainfo.find_one({"_id": ObjectId(Data['id'])}),
                'new_content': '',
            })
        return '1'


# 查询当前页下的改动记录
@app.route('/api/v1/log_server/check_for_current_page', methods=['POST', 'GET'])
def check_for_current_page():
    if request.method == 'POST':
        loginfo = []
        Data = json.loads(request.data)
        for oid in Data['oid']:
            result = datawebunit.log.find_one({"oid": oid})
            if result:
                loginfo.append(result)

        resp = {
            'loginfo': loginfo,
        }
        return json_util.dumps(resp)


# 读取log每页的数据
@app.route('/api/v1/log_server/<pagenumber>/<numPerPage>', methods=['POST', 'GET'])
def get_loginfo_by_page(pagenumber, numPerPage):
    if request.method == 'GET':
        count = datawebunit.log.count()
        resp = datawebunit.log.find().sort('time', -1).limit(
            int(numPerPage)).skip((int(pagenumber) - 1) * int(numPerPage))

        result = {
            'resp': resp,
            'count': count,
        }
        return json_util.dumps(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6234, debug=True)
