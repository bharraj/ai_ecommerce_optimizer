# Navigate to backend/api
cd "$PSScriptRoot/.."
# If .env does not exist, copy template
if (-Not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host ".env created from .env.example"
} else {
    Write-Host ".env already exists"
}