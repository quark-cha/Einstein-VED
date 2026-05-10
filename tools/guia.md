# FUNCIONAMIENTO — Herramientas y Flujo de Trabajo

## 1. Estructura de Directorios

| Carpeta | Contenido |
|---------|-----------|
| `SRC`   | Scripts originales `.py`. Cada script genera figuras base. |
| `TMP`   | Adaptaciones por idioma: `<idioma>_<script>.py` para generar imágenes específicas. |
| `IMG`   | Imágenes generadas: `img/<idioma>_<nombre_imagen>.<svg|png>` |
| `MD`    | Documentos Markdown por idioma: `ES_*.md`, `EN_*.md`, etc. |

---

## 2. Generación de Imágenes

1. Los scripts `.py` en `SRC` generan las figuras originales.  
2. Para cada idioma, se crea una versión en `TMP` con prefijo `<idioma>_`.  
3. Las figuras generadas se colocan en `IMG` con el prefijo correspondiente:  
