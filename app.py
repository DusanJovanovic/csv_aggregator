from flask import Flask, request, jsonify, send_file
from utils.transformator import transform_csv

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Friend!'


@app.route('/api/uploader', methods=['POST'])
def uploader():
    agg = request.form['aggregation']
    data = request.files['data']
    transformer_data, transformer_status = transform_csv(data, agg)
    if transformer_status == 200:
        transformer_data.to_csv('temp.csv', sep=',')
        return send_file('temp.csv')
    return jsonify(transformer_data), transformer_status


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)