$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$systemPython = 'C:\Users\athul\AppData\Local\Programs\Python\Python313\python.exe'
$venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'

if (Test-Path $systemPython) {
    $pythonExe = $systemPython
} elseif (Test-Path $venvPython) {
    $pythonExe = $venvPython
} else {
    $pythonExe = 'python'
}

Set-Location $projectRoot
& $pythonExe 'manage.py' backup_db --output-dir backups --keep 90
