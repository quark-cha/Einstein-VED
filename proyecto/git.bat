cd C:\Users\vedq\Desktop\desarrollo\SRC-VED\Einstein-VED

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PREPARANDO EINSTEIN-VED PARA GITHUB" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. Eliminar .git sucio
Write-Host "[1/6] Eliminando .git local..." -ForegroundColor Yellow
Remove-Item -Path .git -Force -Recurse -ErrorAction SilentlyContinue

# 2. Eliminar SOLO basura (ZIPs, backups, temporales)
Write-Host "[2/6] Eliminando basura (ZIPs, backups, logs)..." -ForegroundColor Yellow
Remove-Item -Path *.zip -Force -ErrorAction SilentlyContinue
Remove-Item -Path backup_* -Force -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path tmp -Force -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path __pycache__ -Force -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path *.log -Force -ErrorAction SilentlyContinue

# NO eliminar: .pdf, .png, .bat, .py, papers/, tools/, img/, etc.

# 3. Crear .gitignore (solo lo estrictamente basura)
Write-Host "[3/6] Creando .gitignore..." -ForegroundColor Yellow
@"
# Excluir solo comprimidos y backups
*.zip
*.7z
*.rar
backup_*/
tmp/
__pycache__/
.ipynb_checkpoints/
.vscode/
*.log
.env
.local
"@ | Out-File -FilePath .gitignore -Encoding utf8

# 4. Inicializar repositorio
Write-Host "[4/6] Inicializando repositorio Git..." -ForegroundColor Yellow
git init

# 5. Añadir TODO (excepto lo excluido por .gitignore)
Write-Host "[5/6] Añadiendo archivos..." -ForegroundColor Yellow
git add .

# 6. Commit y push
Write-Host "[6/6] Commit y push..." -ForegroundColor Yellow
git commit -m "Version completa EINSTEIN-VED - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git remote add origin https://github.com/quark-cha/Einstein-VED.git
git push -u origin main --force

Write-Host "========================================" -ForegroundColor Green
Write-Host "[OK] Repositorio actualizado" -ForegroundColor Green
Write-Host "https://github.com/quark-cha/Einstein-VED" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green