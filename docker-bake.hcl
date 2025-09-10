# Docker Bake configuration for multi-architecture builds
# This file defines how to build Docker images for multiple architectures

# Global variables
variable "REGISTRY" {
  default = "ghcr.io"
}

variable "IMAGE_NAME" {
  default = "astrooverz/astro2.0"
}

variable "TAG" {
  default = "latest"
}

variable "PLATFORMS" {
  default = ["linux/amd64", "linux/arm64"]
}

# Backend image configuration
group "backend" {
  targets = ["backend-latest", "backend-dev"]
}

target "backend-latest" {
  context = "./backend"
  dockerfile = "Dockerfile"
  platforms = PLATFORMS
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/backend:${TAG}",
    "${REGISTRY}/${IMAGE_NAME}/backend:latest"
  ]
  labels = {
    "org.opencontainers.image.title" = "Astrooverz Backend"
    "org.opencontainers.image.description" = "Backend API for Astrooverz Numerology Application"
    "org.opencontainers.image.vendor" = "Astrooverz"
    "org.opencontainers.image.source" = "https://github.com/astrooverz/astro2.0"
    "org.opencontainers.image.version" = "${TAG}"
  }
  cache-from = [
    "type=gha,scope=backend"
  ]
  cache-to = [
    "type=gha,mode=max,scope=backend"
  ]
}

target "backend-dev" {
  context = "./backend"
  dockerfile = "Dockerfile"
  platforms = PLATFORMS
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/backend:dev"
  ]
  target = "development"
  labels = {
    "org.opencontainers.image.title" = "Astrooverz Backend (Development)"
    "org.opencontainers.image.description" = "Development version of Astrooverz Backend"
    "org.opencontainers.image.vendor" = "Astrooverz"
    "org.opencontainers.image.source" = "https://github.com/astrooverz/astro2.0"
    "org.opencontainers.image.version" = "dev"
  }
  cache-from = [
    "type=gha,scope=backend-dev"
  ]
  cache-to = [
    "type=gha,mode=max,scope=backend-dev"
  ]
}

# Frontend image configuration
group "frontend" {
  targets = ["frontend-latest", "frontend-dev"]
}

target "frontend-latest" {
  context = "./frontend"
  dockerfile = "dockerfile"
  platforms = PLATFORMS
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/frontend:${TAG}",
    "${REGISTRY}/${IMAGE_NAME}/frontend:latest"
  ]
  labels = {
    "org.opencontainers.image.title" = "Astrooverz Frontend"
    "org.opencontainers.image.description" = "Frontend application for Astrooverz Numerology"
    "org.opencontainers.image.vendor" = "Astrooverz"
    "org.opencontainers.image.source" = "https://github.com/astrooverz/astro2.0"
    "org.opencontainers.image.version" = "${TAG}"
  }
  cache-from = [
    "type=gha,scope=frontend"
  ]
  cache-to = [
    "type=gha,mode=max,scope=frontend"
  ]
}

target "frontend-dev" {
  context = "./frontend"
  dockerfile = "dockerfile"
  platforms = PLATFORMS
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/frontend:dev"
  ]
  target = "development"
  labels = {
    "org.opencontainers.image.title" = "Astrooverz Frontend (Development)"
    "org.opencontainers.image.description" = "Development version of Astrooverz Frontend"
    "org.opencontainers.image.vendor" = "Astrooverz"
    "org.opencontainers.image.source" = "https://github.com/astrooverz/astro2.0"
    "org.opencontainers.image.version" = "dev"
  }
  cache-from = [
    "type=gha,scope=frontend-dev"
  ]
  cache-to = [
    "type=gha,mode=max,scope=frontend-dev"
  ]
}

# Caddy image configuration
group "caddy" {
  targets = ["caddy-latest"]
}

target "caddy-latest" {
  context = "."
  dockerfile = "Caddyfile"
  platforms = PLATFORMS
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/caddy:${TAG}",
    "${REGISTRY}/${IMAGE_NAME}/caddy:latest"
  ]
  labels = {
    "org.opencontainers.image.title" = "Astrooverz Caddy"
    "org.opencontainers.image.description" = "Caddy web server for Astrooverz"
    "org.opencontainers.image.vendor" = "Astrooverz"
    "org.opencontainers.image.source" = "https://github.com/astrooverz/astro2.0"
    "org.opencontainers.image.version" = "${TAG}"
  }
  cache-from = [
    "type=gha,scope=caddy"
  ]
  cache-to = [
    "type=gha,mode=max,scope=caddy"
  ]
}

# All images group
group "default" {
  targets = ["backend-latest", "frontend-latest", "caddy-latest"]
}

# Development group
group "dev" {
  targets = ["backend-dev", "frontend-dev"]
}

# Production group
group "prod" {
  targets = ["backend-latest", "frontend-latest", "caddy-latest"]
}

# Multi-architecture specific configurations
group "amd64" {
  targets = ["backend-amd64", "frontend-amd64", "caddy-amd64"]
}

target "backend-amd64" {
  inherits = ["backend-latest"]
  platforms = ["linux/amd64"]
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/backend:${TAG}-amd64"
  ]
}

target "frontend-amd64" {
  inherits = ["frontend-latest"]
  platforms = ["linux/amd64"]
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/frontend:${TAG}-amd64"
  ]
}

target "caddy-amd64" {
  inherits = ["caddy-latest"]
  platforms = ["linux/amd64"]
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/caddy:${TAG}-amd64"
  ]
}

group "arm64" {
  targets = ["backend-arm64", "frontend-arm64", "caddy-arm64"]
}

target "backend-arm64" {
  inherits = ["backend-latest"]
  platforms = ["linux/arm64"]
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/backend:${TAG}-arm64"
  ]
}

target "frontend-arm64" {
  inherits = ["frontend-latest"]
  platforms = ["linux/arm64"]
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/frontend:${TAG}-arm64"
  ]
}

target "caddy-arm64" {
  inherits = ["caddy-latest"]
  platforms = ["linux/arm64"]
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/caddy:${TAG}-arm64"
  ]
}

# Release configurations
group "release" {
  targets = ["backend-release", "frontend-release", "caddy-release"]
}

target "backend-release" {
  inherits = ["backend-latest"]
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/backend:${TAG}",
    "${REGISTRY}/${IMAGE_NAME}/backend:latest",
    "${REGISTRY}/${IMAGE_NAME}/backend:stable"
  ]
  labels = {
    "org.opencontainers.image.title" = "Astrooverz Backend"
    "org.opencontainers.image.description" = "Production-ready Backend API for Astrooverz"
    "org.opencontainers.image.vendor" = "Astrooverz"
    "org.opencontainers.image.source" = "https://github.com/astrooverz/astro2.0"
    "org.opencontainers.image.version" = "${TAG}"
    "org.opencontainers.image.created" = "2024-01-01T00:00:00Z"
    "org.opencontainers.image.revision" = "${TAG}"
    "org.opencontainers.image.licenses" = "MIT"
  }
}

target "frontend-release" {
  inherits = ["frontend-latest"]
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/frontend:${TAG}",
    "${REGISTRY}/${IMAGE_NAME}/frontend:latest",
    "${REGISTRY}/${IMAGE_NAME}/frontend:stable"
  ]
  labels = {
    "org.opencontainers.image.title" = "Astrooverz Frontend"
    "org.opencontainers.image.description" = "Production-ready Frontend for Astrooverz"
    "org.opencontainers.image.vendor" = "Astrooverz"
    "org.opencontainers.image.source" = "https://github.com/astrooverz/astro2.0"
    "org.opencontainers.image.version" = "${TAG}"
    "org.opencontainers.image.created" = "2024-01-01T00:00:00Z"
    "org.opencontainers.image.revision" = "${TAG}"
    "org.opencontainers.image.licenses" = "MIT"
  }
}

target "caddy-release" {
  inherits = ["caddy-latest"]
  tags = [
    "${REGISTRY}/${IMAGE_NAME}/caddy:${TAG}",
    "${REGISTRY}/${IMAGE_NAME}/caddy:latest",
    "${REGISTRY}/${IMAGE_NAME}/caddy:stable"
  ]
  labels = {
    "org.opencontainers.image.title" = "Astrooverz Caddy"
    "org.opencontainers.image.description" = "Production-ready Caddy web server for Astrooverz"
    "org.opencontainers.image.vendor" = "Astrooverz"
    "org.opencontainers.image.source" = "https://github.com/astrooverz/astro2.0"
    "org.opencontainers.image.version" = "${TAG}"
    "org.opencontainers.image.created" = "2024-01-01T00:00:00Z"
    "org.opencontainers.image.revision" = "${TAG}"
    "org.opencontainers.image.licenses" = "MIT"
  }
}
