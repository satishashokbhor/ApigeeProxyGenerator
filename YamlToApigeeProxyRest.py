from flask import Flask, jsonify
from flask_restful import Api,reqparse, Resource
from flask import request
import YamlToProxyConverter
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


app = Flask(__name__)
api = Api(app)

@app.route('/proxy', methods=['POST'])
def postProxy():
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=FileStorage, location='files')
    parser.add_argument("authorization",required=True, location='headers', help="authorization can not be blank")

    args = parser.parse_args()
    
    file_ = args['file']
    # file_ = request.files['file']
    if file_:
        print("God Is Great-->"+secure_filename(file_.filename))
        # print(file)
    
    
    print("File Name-->"+secure_filename(file_.filename))
    print("authorization-->"+args["authorization"])
    proxyGenerator =  YamlToProxyConverter.YamlToProxyConverter()
    proxyName = proxyGenerator.convertProxy(file_,args["authorization"])
 
    Proxy = {'proxyName':proxyName}
    return jsonify(Proxy), 201

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(port='5002')

# @app.route('/start', methods=['POST'])
# def startserver():
#     # if __name__ == '__main__':
#     app.run(port='5002',debug=True)
#     return 'Starting server on port : 5002'