# zenodo_limpio.ps1
# Script SIN caracteres especiales - SIN errores

Write-Host "=== ZENODO SIMPLE ==="
Write-Host ""

# Rutas
$base = "C:\Users\vedq\Desktop\desarrollo\SRC-VED"
$einstein = "$base\Einstein-VED\papers"
$uniholog = "$base\UNIHOLOG\papers"

# Verificar Einstein-VED
if (-not (Test-Path $einstein)) {
    Write-Host "ERROR: No se encuentra Einstein-VED"
    Write-Host "Busca en: $einstein"
    pause
    exit
}

# Crear carpeta
$fecha = Get-Date -Format "yyyyMMdd_HHmmss"
$salida = "$base\ZENODO_$fecha"

Write-Host "Creando carpeta: $salida"
New-Item -ItemType Directory -Path "$salida\papers" -Force | Out-Null

# Contador
$n = 1

# 1. Copiar PDFs de Einstein-VED
Write-Host ""
Write-Host "1. Einstein-VED (PDFs):"

if (Test-Path $einstein) {
    $pdfs = Get-ChildItem "$einstein\*.pdf" -ErrorAction SilentlyContinue
    foreach ($pdf in $pdfs) {
        $nuevo = "$n" + "_EIN_" + $pdf.Name
        Copy-Item $pdf.FullName "$salida\papers\$nuevo"
        Write-Host "   [$n] $($pdf.Name)"
        $n++
    }
    Write-Host "   Total: $($pdfs.Count) PDFs"
} else {
    Write-Host "   No hay PDFs"
}

# 2. Copiar MDs de Einstein-VED
Write-Host ""
Write-Host "2. Einstein-VED (MDs):"

if (Test-Path $einstein) {
    $mds = Get-ChildItem "$einstein\*.md" -ErrorAction SilentlyContinue
    foreach ($md in $mds) {
        $nuevo = "$n" + "_EIN_" + $md.Name
        Copy-Item $md.FullName "$salida\papers\$nuevo"
        Write-Host "   [$n] $($md.Name)"
        $n++
    }
    Write-Host "   Total: $($mds.Count) MDs"
} else {
    Write-Host "   No hay MDs"
}

# 3. Copiar UNIHOLOG (si existe)
if (Test-Path $uniholog) {
    Write-Host ""
    Write-Host "3. UNIHOLOG (PDFs):"
    
    $pdfs2 = Get-ChildItem "$uniholog\*.pdf" -ErrorAction SilentlyContinue
    foreach ($pdf in $pdfs2) {
        $nuevo = "$n" + "_UNI_" + $pdf.Name
        Copy-Item $pdf.FullName "$salida\papers\$nuevo"
        Write-Host "   [$n] $($pdf.Name)"
        $n++
    }
    Write-Host "   Total: $($pdfs2.Count) PDFs"
    
    Write-Host ""
    Write-Host "4. UNIHOLOG (MDs):"
    
    $mds2 = Get-ChildItem "$uniholog\*.md" -ErrorAction SilentlyContinue
    foreach ($md in $mds2) {
        $nuevo = "$n" + "_UNI_" + $md.Name
        Copy-Item $md.FullName "$salida\papers\$nuevo"
        Write-Host "   [$n] $($md.Name)"
        $n++
    }
    Write-Host "   Total: $($mds2.Count) MDs"
} else {
    Write-Host ""
    Write-Host "3. UNIHOLOG no encontrado"
    Write-Host "   Continuando solo con Einstein-VED"
}

# 4. Crear README
Write-Host ""
Write-Host "5. Creando README..."

$readme = @"
# ZENODO PACKAGE
# Einstein-VED + UNIHOLOG
# Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## STRUCTURE
/papers/ contains numbered files:
- PDFs: 1_EIN_..., 2_EIN_..., etc.
- MDs: corresponding files with same base name

## THEORIES
- EIN_ = Einstein-VED (proton/neutron structure)
- UNI_ = UNIHOLOG (emergent gravity)

## HOW TO USE
Each PDF has corresponding MD with derivations.

## UPLOAD TO ZENODO
1. Compress this folder as ZIP
2. Go to: https://zenodo.org/deposit/new
3. Upload ZIP file
4. Fill metadata

## METADATA SUGGESTIONS
- Title: Einstein-VED & UNIHOLOG: Unified Theory
- Description: Package with scientific papers
- Keywords: Einstein-VED, UNIHOLOG, physics
- License: CC-BY-SA-4.0
- Type: Preprint

## LINKS
- Einstein-VED: https://github.com/quark-cha/Einstein-VED
- UNIHOLOG: https://github.com/quark-cha/UNIHOLOG
"@

$readme | Out-File "$salida\README.txt" -Encoding UTF8

# 5. Crear ZIP
Write-Host ""
Write-Host "6. Creating ZIP..."

$zip = "$base\Einstein_VED_UNIHOLOG_$fecha.zip"
Compress-Archive -Path "$salida\*" -DestinationPath $zip

# 6. Resumen final
Write-Host ""
Write-Host "========================================"
Write-Host "  COMPLETED SUCCESSFULLY!"
Write-Host "========================================"
Write-Host ""

$totalFiles = (Get-ChildItem "$salida\papers" -File -ErrorAction SilentlyContinue).Count
$pdfCount = (Get-ChildItem "$salida\papers\*.pdf" -ErrorAction SilentlyContinue).Count
$mdCount = (Get-ChildItem "$salida\papers\*.md" -ErrorAction SilentlyContinue).Count

Write-Host "SUMMARY:"
Write-Host "  Total files: $totalFiles"
Write-Host "  PDFs: $pdfCount"
Write-Host "  MDs: $mdCount"
Write-Host ""
Write-Host "FOLDER:"
Write-Host "  $salida"
Write-Host ""
Write-Host "ZIP FILE:"
Write-Host "  $zip"
Write-Host "  Size: $([math]::Round((Get-Item $zip).Length/1MB, 2)) MB"
Write-Host ""
Write-Host "NEXT STEP:"
Write-Host "  Upload to: https://zenodo.org/deposit/new"
Write-Host ""
Write-Host "Ready!"