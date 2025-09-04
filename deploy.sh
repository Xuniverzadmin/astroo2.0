#!/bin/bash

echo "🚀 Deploying Astrooverz..."

# Check if config.env file exists
if [ ! -f config.env ]; then
    echo "⚠️  config.env file not found. Creating from config.env.example..."
    if [ -f config.env.example ]; then
        cp config.env.example config.env
        echo "✅ config.env file created. Please edit it with your actual values."
        echo "   Then run this script again."
        exit 1
    else
        echo "❌ config.env.example not found. Please create a config.env file manually."
        exit 1
    fi
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Remove old images to ensure fresh build
echo "🧹 Cleaning old images..."
docker-compose rm -f
docker system prune -f

# Build and start containers
echo "🔨 Building and starting containers..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check container status
echo "📊 Checking container status..."
docker-compose ps

# Check logs for any errors
echo "📋 Checking logs for errors..."
docker-compose logs --tail=20

echo "✅ Deployment complete!"
echo "🌐 Your website should be available at: https://astrooverz.com"
echo "🔍 Check logs with: docker-compose logs -f"
echo "🛑 Stop services with: docker-compose down"
