# CI/CD Pipeline Documentation

This directory contains GitHub Actions workflows for continuous integration and deployment of the Astrooverz application.

## Workflows Overview

### 1. CI Pipeline (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main`, `develop`, or `feat/*` branches
- Pull requests to `main` or `develop` branches

**Jobs:**

#### Backend Tests
- **Services**: PostgreSQL 15, Redis 7
- **Python Setup**: Python 3.11 with pip caching
- **Test Execution**: Unit tests, integration tests, coverage reports
- **Coverage**: Minimum 70% coverage required
- **Code Quality**: Linting and type checking

#### Frontend Tests
- **Node.js Setup**: Node.js 18 with npm caching
- **Test Execution**: Linting, unit tests, build verification
- **Build Artifacts**: Frontend build artifacts uploaded

#### Docker Build and Push
- **Multi-Architecture**: Linux AMD64 and ARM64
- **Registry**: GitHub Container Registry (ghcr.io)
- **Images**: Backend, Frontend, Caddy
- **Caching**: GitHub Actions cache for faster builds
- **Tags**: Branch-based and SHA-based tagging

#### Security Scanning
- **Tool**: Trivy vulnerability scanner
- **Target**: Latest backend image
- **Output**: SARIF format for GitHub Security tab
- **Trigger**: Only on main branch pushes

#### Integration Tests
- **Environment**: Full Docker Compose stack
- **Tests**: End-to-end API testing
- **Health Checks**: Service health verification
- **API Testing**: Panchangam API functionality

#### Performance Tests
- **Tool**: k6 load testing
- **Scenarios**: Health endpoints, Panchangam API
- **Load**: 10 concurrent users for 5 minutes
- **Metrics**: Response time, success rate

### 2. Deployment Pipeline (`.github/workflows/deploy.yml`)

**Triggers:**
- Push to `main` branch
- Manual workflow dispatch

**Jobs:**

#### Pre-deployment Checks
- **Branch Protection**: Only main branch allowed
- **Secret Verification**: Required secrets validation
- **CI Pipeline**: Ensures CI pipeline passed

#### Deploy to VPS
- **SSH Connection**: Secure SSH to VPS
- **Code Update**: Git pull latest changes
- **Environment Setup**: Production environment configuration
- **Docker Compose**: Multi-file compose with production overrides
- **Health Verification**: Service health checks
- **Cleanup**: Old image cleanup

#### Post-deployment Monitoring
- **Service Status**: Container and resource monitoring
- **External Access**: Public endpoint testing
- **Notifications**: Success/failure notifications

#### Rollback (Manual)
- **Trigger**: Manual workflow dispatch with rollback option
- **Process**: Stop services, rollback to previous version
- **Verification**: Health check after rollback

## Configuration

### Required Secrets

Add these secrets to your GitHub repository:

```bash
# VPS Connection
VPS_HOST=your-vps-ip-or-domain
VPS_USER=your-username
VPS_SSH_KEY=your-private-ssh-key

# Container Registry (automatically provided)
GITHUB_TOKEN=automatically-provided
```

### Environment Variables

The workflows use these environment variables:

```yaml
REGISTRY: ghcr.io
IMAGE_NAME: your-username/astro2.0
```

### Docker Bake Configuration

The `docker-bake.hcl` file defines multi-architecture builds:

- **Platforms**: `linux/amd64`, `linux/arm64`
- **Targets**: Backend, Frontend, Caddy
- **Stages**: Development, Production, Release
- **Caching**: GitHub Actions cache integration

## Usage

### Running CI Pipeline

The CI pipeline runs automatically on:
- Push to main/develop/feat branches
- Pull requests

Manual triggers:
```bash
# Run specific job
gh workflow run ci.yml

# Run with specific inputs
gh workflow run ci.yml -f environment=staging
```

### Running Deployment

Automatic deployment:
- Push to main branch

Manual deployment:
```bash
# Deploy to production
gh workflow run deploy.yml

# Deploy to staging
gh workflow run deploy.yml -f environment=staging

# Rollback
gh workflow run deploy.yml -f environment=rollback
```

### Local Development

Build images locally:
```bash
# Build all images
docker buildx bake

# Build specific target
docker buildx bake backend-latest

# Build for specific architecture
docker buildx bake --set backend-latest.platforms=linux/amd64
```

## Monitoring and Troubleshooting

### CI Pipeline Monitoring

Check pipeline status:
```bash
# View workflow runs
gh run list

# View specific run
gh run view <run-id>

# Download logs
gh run download <run-id>
```

### Deployment Monitoring

Check deployment status:
```bash
# SSH to VPS
ssh user@your-vps

# Check service status
cd /opt/astrooverz
docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

# Check resource usage
docker stats
```

### Common Issues

#### CI Pipeline Failures

**Backend Tests Failing:**
- Check database connection
- Verify Redis availability
- Review test coverage requirements

**Frontend Build Failing:**
- Check Node.js version compatibility
- Verify npm dependencies
- Review build configuration

**Docker Build Failing:**
- Check Dockerfile syntax
- Verify multi-arch support
- Review registry permissions

#### Deployment Failures

**SSH Connection Issues:**
- Verify SSH key format
- Check VPS accessibility
- Review firewall settings

**Service Health Check Failures:**
- Check service logs
- Verify environment variables
- Review port configurations

**Image Pull Failures:**
- Check registry authentication
- Verify image availability
- Review network connectivity

### Performance Optimization

#### CI Pipeline Optimization

**Caching:**
- Python pip cache
- Node.js npm cache
- Docker layer caching
- GitHub Actions cache

**Parallel Execution:**
- Backend and frontend tests run in parallel
- Docker builds use buildx for parallel builds
- Multi-architecture builds in parallel

#### Deployment Optimization

**Image Optimization:**
- Multi-stage builds
- Minimal base images
- Layer caching
- Security scanning

**Service Optimization:**
- Health checks
- Resource limits
- Restart policies
- Log management

## Security Considerations

### Container Security

**Base Images:**
- Official images only
- Regular updates
- Minimal attack surface

**Runtime Security:**
- Non-root users
- Read-only filesystems
- Resource limits
- Network policies

### Deployment Security

**SSH Security:**
- Key-based authentication
- Disabled password auth
- Limited user permissions

**Network Security:**
- Firewall configuration
- SSL/TLS termination
- Secure headers

### Registry Security

**Access Control:**
- GitHub token authentication
- Repository-based permissions
- Image signing (future)

**Vulnerability Scanning:**
- Trivy integration
- Regular scans
- Automated alerts

## Future Enhancements

### Planned Features

**Advanced Monitoring:**
- Prometheus metrics
- Grafana dashboards
- Alerting rules

**Security Enhancements:**
- Image signing
- SBOM generation
- Runtime security scanning

**Performance Improvements:**
- CDN integration
- Edge deployment
- Auto-scaling

**Development Experience:**
- Preview deployments
- Feature flags
- A/B testing

### Contributing

To contribute to the CI/CD pipeline:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make changes to workflows**
4. **Test locally with act**
5. **Submit a pull request**

### Local Testing

Test workflows locally:
```bash
# Install act
npm install -g @nektos/act

# Run CI workflow
act push

# Run deployment workflow
act workflow_dispatch
```

### Documentation Updates

When updating workflows:
1. Update this README
2. Document new secrets
3. Update environment variables
4. Add troubleshooting steps
