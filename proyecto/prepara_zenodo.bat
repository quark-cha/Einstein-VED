# Abrir PowerShell como administrador o terminal de VS Code

# 1. Ir a su directorio de Einstein-VED
cd C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED  # Ajuste su ruta

# 2. Crear directorio para la actualización Zenodo
mkdir zenodo-update -Force
cd zenodo-update

# 3. Crear subdirectorios
mkdir uniholog-integration,figures -Force

# 4. Copiar archivos originales de Einstein-VED
# (Ajuste las rutas según su sistema)
$einsteinPath = "C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED"
$unihologPath = "C:\Users\vedq\Desktop\desarrollo\SRC-VED\UNIHOLOG"

# Copiar PDFs de Einstein-VED
Copy-Item "$einsteinPath\*.pdf" . -ErrorAction SilentlyContinue

# Copiar README si existe
if (Test-Path "$einsteinPath\README.md") {
    Copy-Item "$einsteinPath\README.md" .
}