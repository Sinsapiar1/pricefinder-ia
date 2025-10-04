from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'PriceFinder IA está funcionando en Vercel!',
        'status': 'success'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Servidor funcionando correctamente'
    })

@app.route('/api/test')
def test():
    return jsonify({
        'message': 'Test endpoint funcionando',
        'timestamp': '2024-01-01'
    })