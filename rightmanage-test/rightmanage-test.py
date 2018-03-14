from flask import Flask
import json,os,sys

app = Flask(__name__)


@app.route('/rightmanage/v1.0/cur-permissions')
def cur_permissions(systemname=None):
    basedir=os.path.split(os.path.realpath(__file__))
    filename=basedir[0]+'/right-data.json'
    with open(filename, 'r') as f:
        read_data = f.read()
    f.closed
    d = json.loads(read_data)
    return json.dumps(d)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
