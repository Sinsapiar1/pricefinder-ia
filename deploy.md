# Guía de Deployment

## Plataformas Recomendadas

### 1. Railway
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login y deploy
railway login
railway init
railway up
```

### 2. Render
1. Conecta tu repositorio GitHub
2. Selecciona "Web Service"
3. Configura:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT run:app`
   - Environment: `Python 3.11`

### 3. Heroku
```bash
# Instalar Heroku CLI
# Crear Procfile
echo "web: gunicorn --bind 0.0.0.0:\$PORT run:app" > Procfile

# Deploy
heroku create tu-app-name
git push heroku main
```

### 4. DigitalOcean App Platform
1. Conecta GitHub
2. Selecciona el repositorio
3. Configura:
   - Source: `/`
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn --bind 0.0.0.0:$PORT run:app`

## Variables de Entorno Requeridas

```bash
SECRET_KEY=tu-secret-key-super-seguro
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
```

## Comandos de Testing Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest

# Ejecutar con Docker
docker build -t pricefinder-ia .
docker run -p 5000:5000 pricefinder-ia

# Ejecutar con Docker Compose
docker-compose up
```