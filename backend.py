#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS
import subprocess, json, datetime, os

app = Flask(__name__)
CORS(app)
SPEEDTEST_CMD = os.environ.get('SPEEDTEST_CMD', 'speedtest-cli')

@app.route('/api/test', methods=['GET'])
def speed_test():
    try:
        raw = subprocess.check_output([SPEEDTEST_CMD, '--json'],
                                      stderr=subprocess.STDOUT, timeout=90).decode('utf-8')
        result = json.loads(raw)
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
        return jsonify({
            'timestamp': timestamp,
            'ping': result.get('ping'),
            'download': result.get('download'),
            'upload': result.get('upload'),
            'server': result.get('server', {})
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Speedtest timeout'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return 'TLAXICOM API OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
