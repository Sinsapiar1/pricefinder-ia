# 🚀 Deployment en Vercel

## Configuración Completa para Vercel

Tu aplicación Flask ya está configurada para funcionar en Vercel como funciones serverless.

## Pasos para Deployar

### 1. **Instalar Vercel CLI**
```bash
npm install -g vercel
```

### 2. **Login en Vercel**
```bash
vercel login
```

### 3. **Deploy desde tu directorio**
```bash
vercel
```

### 4. **Configurar Variables de Entorno**
En el dashboard de Vercel:
1. Ve a tu proyecto
2. Settings → Environment Variables
3. Agrega:
   ```
   SECRET_KEY=tu-secret-key-super-seguro
   FLASK_ENV=production
   FLASK_DEBUG=false
   ```

### 5. **Deploy de Producción**
```bash
vercel --prod
```

## Estructura para Vercel

```
/
├── api/
│   ├── index.py          # Handler principal
│   └── requirements.txt  # Dependencias para Vercel
├── app/                  # Tu aplicación Flask
├── vercel.json          # Configuración de Vercel
└── ...
```

## URLs de tu App

- **Desarrollo**: `https://tu-app-git-main-tu-usuario.vercel.app`
- **Producción**: `https://tu-app.vercel.app`

## Endpoints Disponibles

- `GET /` - Página principal
- `GET /api/health` - Health check
- `POST /api/search` - Búsqueda de productos

## Limitaciones de Vercel

⚠️ **Importante**: Vercel tiene limitaciones para aplicaciones Flask:

1. **Timeout**: 10 segundos para funciones gratuitas, 60s para Pro
2. **Memoria**: 1GB máximo
3. **Cold Start**: Primera petición puede ser lenta
4. **Dependencias**: Algunas librerías pueden no funcionar

## Alternativas Recomendadas

Si tienes problemas con Vercel, considera:

1. **Railway** - Mejor para Flask
2. **Render** - Excelente soporte Python
3. **DigitalOcean App Platform** - Más control
4. **Heroku** - Clásico y confiable

## Testing Local

```bash
# Instalar Vercel CLI
npm install -g vercel

# Ejecutar localmente
vercel dev

# Tu app estará en http://localhost:3000
```

## Troubleshooting

### Error: "Module not found"
- Verifica que `api/requirements.txt` tenga todas las dependencias
- Asegúrate de que el path en `api/index.py` sea correcto

### Error: "Timeout"
- Optimiza tu código para respuestas más rápidas
- Considera usar Vercel Pro para timeouts más largos

### Error: "CORS"
- Ya está configurado para permitir todos los orígenes
- Si persiste, verifica la configuración en `app/__init__.py`