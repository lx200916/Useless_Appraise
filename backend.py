from flask import Flask, request, jsonify, Response, render_template, send_from_directory,send_file
from flask_socketio import SocketIO
from flask_socketio import Namespace, emit,send
from multiprocessing import Value
counts=Value('i',0)
isover=Value('i',0)
from flask_cors import *
from flask import jsonify
import requests
import copy
a=0
grades=['D','C','B','A']
file=open("stu.ini","r")
stu=file.readlines()
app = Flask(__name__)
out = open("val.csv", "w+")
print(",".join([v.strip() for v in stu]),file=out)
from  enum import Enum
class GRD(Enum):
    D = 1
    C  = 2
    B = 3
    A = 4
out.close()
CORS(app, supports_credentials=True)
socketio = SocketIO(app,cors_allowed_origins="*")
@app.route('/test',methods=['GET'])
def test():
    return send_from_directory('Templates','index.html')

@app.route('/get',methods=['GET'])
def get():
    info={}
    infos=[]
    for st in stu:
        info['name']=st.split('	')[1].strip()
        info['number'] = st.split('	')[0]
        info['value']=0
        info['dot']=False
        infos.append(copy.deepcopy(info))


    print(a)
    return jsonify(infos)
@app.route('/',methods=['GET'])
def index():

    return send_from_directory('Templates', 'back.html')

@app.route('/done',methods=['GET'])
def result():
    isover.value+=1
    print(isover.value)
    return send_from_directory('./','val.csv',as_attachment=True)
@socketio.on('connect')
def test_connect():
    emit('init', {'all': len(stu),'num':counts.value,'isover':0})
@app.route('/post',methods=['POST'])
def post():
    print(isover.value)
    if(isover.value!=0):
        print(isover.value)
        return jsonify({
            'code':1,
            'mes':'已截止'
        })
    if(type(request.json)!=list):
        if(str(request.json.get('code','0'))=='3'):
            isover.value=+1
            socketio.emit('off',{'isover':1})
            return 'ok'

    rec=open("rec.txt","a+")
    out = open("val.csv", "a+")

    values=list(map(lambda x:x['value'],request.json))




    if (0 in values):
        return jsonify({"code":1,"mes":"请检查是否漏填"})
    if ((2 not in values)|(values.count(2)<2)):
        return jsonify({"code":1,"mes":"必须有两个C级"})
    if(len(values)!=len(stu)):
        return jsonify({"code": 1, "mes": "数据非法"})

    values=list(map(lambda x:str(GRD(x).name),values))
    print(request.json,file=rec)
    print(values)
    counts.value+=1
    print(",".join(values),file=out)
# print(request.headers)
    socketio.emit('new',{'num':counts.value,'ua':request.headers.get('User-Agent',"Unknown"),'ip':request.remote_addr})
    out.close()
    return jsonify({"code":0})


if __name__ == '__main__':
    socketio.run(app,port=2333,host="0.0.0.0")
