# ⚡ Quick Start - Vercel Deploy

## 🎯 Pasos Rápidos (2 minutos)

### 1️⃣ Preparar Repositorio
```bash
git add .
git commit -m "Configurar para Vercel"
git push
```

### 2️⃣ Desplegar en Vercel
1. Ve a [vercel.com](https://vercel.com)
2. Inicia sesión con GitHub
3. Click en "New Project"
4. Selecciona tu repositorio
5. Click en "Deploy"
6. ¡Listo! ⏱️ (2-3 minutos)

### 3️⃣ Usar la Aplicación
1. Abre la URL que te da Vercel
2. Ingresa tus API Keys:
   - **Gemini API**: https://ai.google.dev/
   - **Scraper API**: https://www.scraperapi.com/
3. ¡Busca productos!

## 📁 Archivos Creados para Vercel

```
✅ vercel.json        # Configuración de Vercel
✅ api/index.py       # Punto de entrada serverless
✅ .vercelignore      # Archivos a ignorar
✅ .env.example       # Variables de entorno ejemplo
```

## ⚙️ Configuración Aplicada

```json
{
  "Python Runtime": "3.x",
  "Serverless Functions": "Habilitado",
  "Static Files": "app/static/",
  "Auto Deploy": "main branch"
}
```

## ⚠️ Importante

- **Timeout**: 10 segundos (plan gratuito)
- **Ideal para**: Búsquedas rápidas de 2-3 sitios
- **Si necesitas más tiempo**: Usa Render o Railway

## 🔗 URLs Útiles

- 📚 [Guía completa de despliegue](./DEPLOY_VERCEL.md)
- 🌐 [Vercel Dashboard](https://vercel.com/dashboard)
- 💬 [Soporte Vercel](https://vercel.com/support)

## 🐛 Problemas Comunes

### Error en Build
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Fix dependencies"
git push
```

### Función se queda esperando
- Reduce sitios a buscar en config.py
- O actualiza al plan Pro de Vercel ($20/mes)

## 💡 Tips

- ✅ Los cambios se despliegan automáticamente con cada `git push`
- ✅ Puedes hacer rollback a versiones anteriores
- ✅ Cada PR crea un preview deployment
- ✅ HTTPS gratis incluido

---

**¿Problemas?** Lee la [guía completa](./DEPLOY_VERCEL.md)
