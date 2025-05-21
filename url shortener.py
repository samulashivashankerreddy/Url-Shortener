from flask import Flask, request, redirect, jsonify
import random
import string

app = Flask(__name__)

url_mapping = {}

def generate_short_id(num_chars=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')
    if not original_url:
        return jsonify({'error': 'Missing URL'}), 400

    short_id = generate_short_id()
    while short_id in url_mapping:
        short_id = generate_short_id()

    url_mapping[short_id] = original_url

    short_url = request.host_url + short_id
    return jsonify({'short_url': short_url})

@app.route('/<short_id>')
def redirect_short_url(short_id):
    original_url = url_mapping.get(short_id)
    if original_url:
        return redirect(original_url)
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
