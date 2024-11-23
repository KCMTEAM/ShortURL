from flask import Flask, redirect, request, jsonify
import random
import string

app = Flask(__name__)

# Penyimpanan URL (gunakan database untuk produksi)
url_database = {}

# Fungsi untuk menghasilkan kode pendek acak
def generate_shortcode():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Route untuk mempersingkat URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')
    if not original_url:
        return jsonify({'error': 'URL tidak ditemukan'}), 400
    
    shortcode = generate_shortcode()

    # Pastikan shortcode unik
    while shortcode in url_database:
        shortcode = generate_shortcode()

    # Menyimpan URL dan shortcode
    url_database[shortcode] = original_url

    return jsonify({'shortened_url': f'http://127.0.0.1:5000/{shortcode}'}), 200

# Route untuk memperluas URL menggunakan shortcode
@app.route('/<shortcode>', methods=['GET'])
def expand_url(shortcode):
    original_url = url_database.get(shortcode)
    if original_url:
        return redirect(original_url)
    else:
        return jsonify({'error': 'URL tidak ditemukan'}), 404

if __name__ == '__main__':
    app.run(debug=True)