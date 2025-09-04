@echo off
echo 🚀 Deploying Astrooverz...

REM Check if config.env file exists
if not exist config.env (
    echo ⚠️  config.env file not found. Creating from config.env.example...
    if exist config.env.example (
        copy config.env.example config.env
        echo ✅ config.env file created. Please edit it with your actual values.
        echo    Then run this script again.
        pause
        exit /b 1
    ) else (
        echo ❌ config.env.example not found. Please create a config.env file manually.
        pause
        exit /b 1
    )
)

REM Stop existing containers
echo 🛑 Stopping existing containers...
docker-compose down

REM Remove old images to ensure fresh build
echo 🧹 Cleaning old images...
docker-compose rm -f
docker system prune -f

REM Build and start containers
echo 🔨 Building and starting containers...
docker-compose up -d --build

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check container status
echo 📊 Checking container status...
docker-compose ps

REM Check logs for any errors
echo 📋 Checking logs for errors...
docker-compose logs --tail=20

echo ✅ Deployment complete!
echo 🌐 Your website should be available at: https://astrooverz.com
echo 🔍 Check logs with: docker-compose logs -f
echo 🛑 Stop services with: docker-compose down
pause
