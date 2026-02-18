Write-Host "Build images with Docker Compose..."
docker-compose build
if ($LASTEXITCODE -ne 0) {
    Write-Host "The Docker Compose failed to build the app"
    exit 1
}
    
Write-Host "Starting app with Docker Compose..."
docker-compose up --detach
if ($LASTEXITCODE -ne 0) {
    Write-Host "The Docker Compose failed to start the app"
    exit 1
}


$counter = 60
$success = $false

while ($counter -ge 1) {
    $healthCheckMessage = "The script couldn't connect to the API"

    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:5173/api/health'

        if ($response.StatusCode -eq 200) {
            $counter = 0
            $success = $true
            $healthCheckMessage = "Connection to the API is successful"
        } else {
            $counter = $counter - 1
        }
    } 
    catch {
        $counter = $counter - 1
    } 
    finally {
        if (-Not $success) {
            Start-Sleep -Seconds 2
        }
    }
}

$healthCheckMessage

Write-Host "Docker-compose is stopping..."
docker-compose down

if ($success) {
    exit 0
} else {
    exit 1
}
