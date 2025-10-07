# pricefinder-ia# 🚀 PriceFinder IA

Aplicación web profesional para búsqueda inteligente de productos en las principales tiendas online de EE.UU. usando IA de Google Gemini.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/tu-usuario/pricefinder-ia)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 📋 Descripción

PriceFinder IA transforma la búsqueda manual de productos en una decisión de compra inteligente. La aplicación:

- 🔍 Busca productos en Amazon, Walmart, Best Buy, eBay y Target
- 🤖 Analiza precios usando Google Gemini AI
- 📊 Compara precios y genera recomendaciones inteligentes
- 💰 Identifica el mejor valor considerando precio, reputación y reviews

## ✨ Características

- **Búsqueda Multi-Sitio Híbrida**: 
  - ✅ **GRATIS:** Amazon + eBay (plan gratuito ScraperAPI)
  - 💎 **PREMIUM:** Walmart + BestBuy (requiere ScraperAPI pago)
- **Análisis Inteligente con IA**: Google Gemini normaliza nombres, detecta productos idénticos y genera insights
- **Comparación Visual Profesional**: Gráficos interactivos, tabla responsiva, y cards para móvil
- **Recomendaciones IA**: Sistema inteligente (🏆 Mejor Opción, ✅ Buena Alternativa, ⚠️ Considerar, ❌ No Recomendado)
- **100% Responsivo**: Mobile-first design - perfecto en cualquier dispositivo
- **Detección Automática**: Muestra badge "PRO" si detecta plan premium de ScraperAPI
- **Despliegue Fácil**: Listo para Vercel, Render, Railway o Docker

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

### Google Gemini API (100% Gratuito)

1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Click en "Create API Key"
4. Copia la key (empieza con `AIza...`)
5. Pégala en la interfaz web

### ScraperAPI - Modelo Híbrido

#### **Plan Gratuito (Recomendado para empezar)**
1. Regístrate en [ScraperAPI](https://www.scraperapi.com/signup)
2. Plan gratuito: **5,000 requests/mes**
3. Copia tu API Key desde el dashboard
4. **Funciona con:**
   - ✅ Amazon (perfecto)
   - ✅ eBay (muy bien)
5. **No funciona con:**
   - ❌ Walmart (requiere plan pago)
   - ❌ Best Buy (requiere plan pago)

#### **Plan Hobby - $49/mes (Opcional)**
1. Actualiza tu plan en ScraperAPI
2. **250,000 requests/mes**
3. **Funciona con TODAS las tiendas:**
   - ✅ Amazon
   - ✅ eBay
   - ✅ Walmart
   - ✅ Best Buy

**La app detecta automáticamente qué plan tienes y muestra las tiendas disponibles.** 🎯

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

### Vercel

La aplicación está completamente configurada para Vercel con funciones serverless:

1. **Fork o clona el repositorio en GitHub**

2. **Conecta con Vercel**:
   - Ve a [vercel.com](https://vercel.com)
   - Click en "New Project"
   - Importa tu repositorio de GitHub

3. **Configuración automática**:
   - Vercel detectará automáticamente la configuración
   - No necesitas configurar nada adicional

4. **Deploy**:
   - Click en "Deploy"
   - Espera a que termine el despliegue (2-3 minutos)

5. **Usar la aplicación**:
   - Vercel te dará una URL (ej: `tu-app.vercel.app`)
   - Ingresa tus API keys en la interfaz web
   - ¡Listo para usar!

**Limitaciones en Vercel**:
- Timeout de 10 segundos (plan gratuito) o 60 segundos (plan pro)
- Ideal para búsquedas rápidas
- Si necesitas más tiempo, usa Render o Railway

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

**Raul Pivet Alvarez**
- GitHub: [@Sinsapiar1](https://github.com/Sinsapiar1)
- Proyecto: [PriceFinder IA](https://github.com/Sinsapiar1/pricefinder-ia)

## 🙏 Agradecimientos

- Google Gemini por la API de IA
- ScraperAPI por facilitar el web scraping
- La comunidad de Flask y Python

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!

**Made with ❤️ using Flask & Google Gemini**