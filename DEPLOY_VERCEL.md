# 🚀 Guía de Despliegue en Vercel

Esta guía te ayudará a desplegar **PriceFinder IA** en Vercel en menos de 5 minutos.

## ✅ Prerrequisitos

- Una cuenta de GitHub (gratuita)
- Una cuenta de Vercel (gratuita) - [Crear cuenta](https://vercel.com/signup)
- Tu código debe estar en un repositorio de GitHub

## 📋 Pasos para Desplegar

### 1. Preparar el Repositorio en GitHub

Si aún no tienes tu código en GitHub:

```bash
# Inicializar repositorio (si no lo has hecho)
git init
git add .
git commit -m "Preparar para despliegue en Vercel"

# Crear repositorio en GitHub y conectarlo
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
```

### 2. Conectar con Vercel

1. **Ir a Vercel**: Visita [vercel.com](https://vercel.com)

2. **Iniciar sesión**: Usa tu cuenta de GitHub para iniciar sesión

3. **Nuevo Proyecto**:
   - Click en **"Add New..."** → **"Project"**
   - Autoriza a Vercel para acceder a tus repositorios de GitHub
   - Selecciona el repositorio de **PriceFinder IA**

### 3. Configurar el Proyecto

Vercel detectará automáticamente la configuración gracias al archivo `vercel.json`.

**No necesitas cambiar nada**, pero estos son los valores que detectará:

```
Framework Preset: Other
Build Command: [Automático]
Output Directory: [Automático]
Install Command: pip install -r requirements.txt
```

### 4. Deploy

1. Click en **"Deploy"**
2. Espera 2-3 minutos mientras Vercel:
   - Instala las dependencias de Python
   - Construye la aplicación
   - Despliega las funciones serverless

### 5. ¡Listo! 🎉

Una vez completado el despliegue:

1. Vercel te mostrará una URL: `https://tu-proyecto.vercel.app`
2. Click en **"Visit"** para abrir tu aplicación
3. Ingresa tus API keys en la interfaz:
   - **Gemini API Key**: Obtén una en [Google AI Studio](https://ai.google.dev/)
   - **Scraper API Key**: Obtén una en [ScraperAPI](https://www.scraperapi.com/)
4. ¡Comienza a buscar productos!

## 🔄 Actualizaciones Automáticas

Cada vez que hagas `git push` a la rama `main`, Vercel automáticamente:
- Detectará los cambios
- Reconstruirá la aplicación
- Desplegará la nueva versión

## ⚙️ Variables de Entorno (Opcional)

Si quieres configurar variables de entorno en Vercel:

1. En tu proyecto de Vercel, ve a **Settings** → **Environment Variables**
2. Añade las variables que necesites:
   ```
   SECRET_KEY=tu-clave-secreta
   FLASK_ENV=production
   ```
3. Redeploya el proyecto

## 📊 Características de Vercel

### Plan Gratuito (Hobby)
- ✅ Despliegues ilimitados
- ✅ HTTPS automático
- ✅ Dominio personalizado
- ✅ 100 GB de ancho de banda/mes
- ⏱️ Timeout de función: **10 segundos**

### Plan Pro ($20/mes)
- ✅ Todo lo del plan gratuito
- ✅ 1 TB de ancho de banda/mes
- ⏱️ Timeout de función: **60 segundos**
- ✅ Análisis avanzado

## ⚠️ Limitaciones Importantes

### Timeout de Funciones
- **Plan gratuito**: 10 segundos máximo por request
- **Plan Pro**: 60 segundos máximo por request

Si tu búsqueda toma más tiempo (scraping de múltiples sitios), considera:
1. Reducir el número de sitios a buscar
2. Optimizar el scraper
3. Usar **Render** o **Railway** (sin límite de timeout)

### Funciones Serverless
- No hay estado persistente entre requests
- Cada request es independiente
- No puedes usar procesos en background

## 🐛 Solución de Problemas

### Error: "Build Failed"
```bash
# Asegúrate de que requirements.txt esté actualizado
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Actualizar dependencias"
git push
```

### Error: "Function Timeout"
- Reduce el número de sitios a buscar en `config.py`
- Considera actualizar al plan Pro de Vercel
- O usa Render/Railway para timeouts más largos

### Error: "Module Not Found"
- Verifica que todos los módulos estén en `requirements.txt`
- Revisa que la estructura de carpetas sea correcta

## 🔗 Dominio Personalizado

Para usar tu propio dominio:

1. En Vercel, ve a **Settings** → **Domains**
2. Añade tu dominio (ej: `pricefinder.com`)
3. Configura los DNS según las instrucciones de Vercel
4. ¡Listo! Tu app estará en tu dominio personalizado

## 📈 Monitoreo

Vercel proporciona métricas en tiempo real:
- **Analytics**: Visitas, países, dispositivos
- **Logs**: Ver logs de función en tiempo real
- **Performance**: Tiempo de respuesta, uso de recursos

Accede a estas métricas desde tu dashboard de Vercel.

## 🆚 Comparación con Otras Plataformas

| Plataforma | Timeout | Precio | Facilidad | Recomendado Para |
|-----------|---------|--------|-----------|------------------|
| **Vercel** | 10-60s | Gratis-$20 | ⭐⭐⭐⭐⭐ | Apps rápidas, prototipos |
| **Render** | Ilimitado | Gratis-$7 | ⭐⭐⭐⭐ | Apps con procesos largos |
| **Railway** | Ilimitado | $5/mes | ⭐⭐⭐⭐ | Apps con Docker |
| **Heroku** | 30s | $7/mes | ⭐⭐⭐ | Apps tradicionales |

## 💡 Consejos Pro

1. **Preview Deployments**: Cada PR crea un preview deployment automático
2. **Rollback Instantáneo**: Puedes volver a cualquier versión anterior en 1 click
3. **Edge Network**: Tu app se sirve desde el edge más cercano al usuario
4. **Monitoreo**: Configura notificaciones para errores en Settings

## 📚 Recursos Adicionales

- [Documentación de Vercel](https://vercel.com/docs)
- [Vercel + Python](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Comunidad de Vercel](https://vercel.com/community)

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs en el dashboard de Vercel
2. Consulta la [documentación oficial](https://vercel.com/docs)
3. Abre un issue en GitHub
4. Contacta al soporte de Vercel (muy responsivo)

---

**¡Happy Deploying! 🚀**

Si esta guía te fue útil, dale ⭐ al repositorio.
