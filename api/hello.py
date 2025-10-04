from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': '¡Hola desde Vercel!',
        'status': 'success',
        'app': 'PriceFinder IA'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Servidor funcionando'
    })