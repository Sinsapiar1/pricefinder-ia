# pricefinder-ia# 🚀 PriceFinder IA

Aplicación web profesional para búsqueda inteligente de productos en las principales tiendas online de EE.UU. usando IA de Google Gemini.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Descripción

PriceFinder IA transforma la búsqueda manual de productos en una decisión de compra inteligente. La aplicación:

- 🔍 Busca productos en Amazon, Walmart, Best Buy, eBay y Target
- 🤖 Analiza precios usando Google Gemini AI
- 📊 Compara precios y genera recomendaciones inteligentes
- 💰 Identifica el mejor valor considerando precio, reputación y reviews

## ✨ Características

- **Búsqueda Multi-Sitio**: Scraping simultáneo en las 5 tiendas más grandes de EE.UU.
- **Análisis Inteligente**: Google Gemini normaliza nombres y detecta productos idénticos
- **Comparación Visual**: Gráficos interactivos y tabla comparativa
- **Recomendaciones IA**: Sistema de clasificación (Mejor Precio, Alternativa, No Recomendado)
- **Interfaz Moderna**: UI responsive con Tailwind CSS
- **Containerizado**: Listo para despliegue con Docker

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| Backend | Python 3.11 + Flask |
| Frontend | HTML5, CSS3 (Tailwind), JavaScript |
| IA | Google Gemini API |
| Scraping | ScraperAPI / Bright Data |
| Gráficos | Chart.js |
| Deploy | Docker + Gunicorn |

## 📦 Instalación

### Prerrequisitos

- Python 3.11+
- pip
- Git
- (Opcional) Docker

### Opción 1: Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/pricefinder-ia.git
cd pricefinder-ia

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 5. Ejecutar la aplicación
python run.py
```

La aplicación estará disponible en: `http://localhost:5000`

### Opción 2: Docker

```bash
# 1. Construir la imagen
docker build -t pricefinder-ia .

# 2. Ejecutar el contenedor
docker run -p 5000:5000 pricefinder-ia
```

## 🔑 Configuración de API Keys

### Google Gemini API

1. Ve a [Google AI Studio](https://ai.google.dev/)
2. Inicia sesión con tu cuenta de Google
3. Crea un nuevo proyecto
4. Genera una API Key
5. Copia la key (la necesitarás en la interfaz web)

### ScraperAPI

1. Regístrate en [ScraperAPI](https://www.scraperapi.com/)
2. El plan gratuito incluye 5,000 requests/mes
3. Copia tu API Key desde el dashboard
4. Úsala en la interfaz web

## 🎯 Uso

1. **Abrir la aplicación**: Navega a `http://localhost:5000`

2. **Ingresar API Keys**:
   - Gemini API Key
   - Scraper API Key

3. **Buscar producto**: 
   - Ejemplo: "Sony WH-1000XM5"
   - Ejemplo: "iPhone 15 Pro Max"
   - Ejemplo: "Nintendo Switch OLED"

4. **Ver resultados**:
   - Resumen inteligente generado por IA
   - Estadísticas de precios
   - Gráfico comparativo
   - Tabla detallada con enlaces directos

## 📁 Estructura del Proyecto

```
pricefinder-ia/
├── app/
│   ├── __init__.py           # Inicialización Flask
│   ├── routes.py             # Rutas y endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── scraper.py        # Lógica de scraping
│   │   └── gemini_analyzer.py # Análisis con IA
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js       # Lógica frontend
│   └── templates/
│       └── index.html        # Interfaz principal
├── config.py                 # Configuración
├── run.py                    # Punto de entrada
├── requirements.txt          # Dependencias
├── Dockerfile               # Containerización
├── .dockerignore
├── .gitignore
├── .env.example
└── README.md
```

## 🚀 Despliegue

### Render

1. Conecta tu repositorio de GitHub
2. Selecciona "Web Service"
3. Configura:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT run:app`

### Railway

1. Conecta tu repositorio
2. Railway detectará automáticamente el Dockerfile
3. Deploy automático en cada push

### Vercel (Solo Frontend)

Para el frontend estático con Next.js o similar.

## 🔄 CI/CD con GitHub Actions

Crea `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

## 🧪 Testing

```bash
# Instalar dependencias de testing
pip install pytest pytest-cov

# Ejecutar tests
pytest tests/

# Con coverage
pytest --cov=app tests/
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Roadmap

- [ ] Soporte para más tiendas (Costco, Home Depot)
- [ ] Sistema de alertas de precio
- [ ] Historial de búsquedas
- [ ] Autenticación de usuarios
- [ ] API REST pública
- [ ] Aplicación móvil (React Native)
- [ ] Análisis de tendencias de precio

## ⚠️ Advertencias

- Las API keys deben mantenerse privadas
- Respeta los términos de servicio de las tiendas
- El scraping puede estar limitado por rate limits
- Algunos sitios pueden requerir técnicas anti-bot más avanzadas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

## 🙏 Agradecimientos

- Google Gemini por la API de IA
- ScraperAPI por facilitar el web scraping
- La comunidad de Flask y Python

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!

**Made with ❤️ using Flask & Google Gemini**