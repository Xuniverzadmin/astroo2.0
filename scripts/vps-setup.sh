#!/bin/bash

# Astrooverz VPS Initial Setup Script
# This script sets up a fresh VPS for running the Astrooverz application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/opt/astrooverz"
LOG_FILE="/var/log/astrooverz-setup.log"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

# Function to check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "This script must be run as root"
        exit 1
    fi
}

# Function to setup logging
setup_logging() {
    mkdir -p "$(dirname "$LOG_FILE")"
    touch "$LOG_FILE"
    print_status "Logging to: $LOG_FILE"
}

# Function to update system packages
update_system() {
    print_status "Updating system packages..."
    
    apt update
    apt upgrade -y
    
    print_success "System packages updated"
}

# Function to install essential packages
install_essential_packages() {
    print_status "Installing essential packages..."
    
    apt install -y \
        curl \
        wget \
        git \
        unzip \
        htop \
        nano \
        vim \
        ufw \
        fail2ban \
        cron \
        logrotate \
        rsync \
        jq
    
    print_success "Essential packages installed"
}

# Function to install Docker
install_docker() {
    print_status "Installing Docker..."
    
    # Remove old Docker versions
    apt remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
    
    # Install Docker dependencies
    apt install -y \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
    
    # Add Docker GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Add Docker repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Update package index
    apt update
    
    # Install Docker
    apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Start and enable Docker
    systemctl start docker
    systemctl enable docker
    
    # Add current user to docker group (if not root)
    if [ "$SUDO_USER" ]; then
        usermod -aG docker "$SUDO_USER"
    fi
    
    print_success "Docker installed and started"
}

# Function to install Docker Compose
install_docker_compose() {
    print_status "Installing Docker Compose..."
    
    # Install docker-compose-plugin (included with Docker)
    apt install -y docker-compose-plugin
    
    # Create symlink for docker-compose command
    ln -sf /usr/libexec/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose
    
    print_success "Docker Compose installed"
}

# Function to setup firewall
setup_firewall() {
    print_status "Setting up firewall..."
    
    # Reset UFW to defaults
    ufw --force reset
    
    # Set default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH
    ufw allow 22/tcp
    
    # Allow HTTP and HTTPS
    ufw allow 80/tcp
    ufw allow 443/tcp
    
    # Enable firewall
    ufw --force enable
    
    print_success "Firewall configured"
}

# Function to setup fail2ban
setup_fail2ban() {
    print_status "Setting up fail2ban..."
    
    # Create fail2ban configuration
    cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 3
bantime = 3600
EOF
    
    # Start and enable fail2ban
    systemctl start fail2ban
    systemctl enable fail2ban
    
    print_success "Fail2ban configured"
}

# Function to setup log rotation
setup_log_rotation() {
    print_status "Setting up log rotation..."
    
    # Create logrotate configuration for Astrooverz
    cat > /etc/logrotate.d/astrooverz << 'EOF'
/var/log/astrooverz/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        /bin/kill -USR1 $(cat /var/run/rsyslogd.pid 2>/dev/null) 2>/dev/null || true
    endscript
}
EOF
    
    print_success "Log rotation configured"
}

# Function to setup monitoring
setup_monitoring() {
    print_status "Setting up monitoring..."
    
    # Create monitoring script
    cat > /opt/astrooverz/monitor.sh << 'EOF'
#!/bin/bash

LOG_FILE="/var/log/astrooverz/monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] === Service Status ===" >> "$LOG_FILE"
docker-compose -f /opt/astrooverz/docker-compose.yml -f /opt/astrooverz/docker-compose.prod.yml ps >> "$LOG_FILE" 2>&1

echo "[$DATE] === Resource Usage ===" >> "$LOG_FILE"
docker stats --no-stream >> "$LOG_FILE" 2>&1

echo "[$DATE] === Disk Usage ===" >> "$LOG_FILE"
df -h >> "$LOG_FILE" 2>&1

echo "[$DATE] === Memory Usage ===" >> "$LOG_FILE"
free -h >> "$LOG_FILE" 2>&1

echo "[$DATE] === Health Checks ===" >> "$LOG_FILE"
curl -f http://localhost:8000/healthz >> "$LOG_FILE" 2>&1 && echo "Backend: OK" >> "$LOG_FILE" || echo "Backend: FAILED" >> "$LOG_FILE"
curl -f http://localhost:8000/api/healthz >> "$LOG_FILE" 2>&1 && echo "API: OK" >> "$LOG_FILE" || echo "API: FAILED" >> "$LOG_FILE"
curl -f http://localhost:5173 >> "$LOG_FILE" 2>&1 && echo "Frontend: OK" >> "$LOG_FILE" || echo "Frontend: FAILED" >> "$LOG_FILE"

echo "[$DATE] === End of Report ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
EOF
    
    chmod +x /opt/astrooverz/monitor.sh
    
    # Create log directory
    mkdir -p /var/log/astrooverz
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "*/5 * * * * /opt/astrooverz/monitor.sh") | crontab -
    
    print_success "Monitoring configured"
}

# Function to setup backup
setup_backup() {
    print_status "Setting up backup system..."
    
    # Create backup script
    cat > /opt/astrooverz/backup.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/opt/astrooverz/backups"
DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/var/log/astrooverz/backup.log"

mkdir -p "$BACKUP_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting backup..." >> "$LOG_FILE"

# Database backup
if docker-compose -f /opt/astrooverz/docker-compose.yml -f /opt/astrooverz/docker-compose.prod.yml exec -T db pg_dump -U astrooverz astrooverz > "$BACKUP_DIR/astrooverz_$DATE.sql" 2>/dev/null; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Database backup created: astrooverz_$DATE.sql" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Database backup failed" >> "$LOG_FILE"
fi

# Configuration backup
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" -C /opt/astrooverz .env docker-compose.prod.yml 2>/dev/null

# Clean up old backups (keep last 7 days)
find "$BACKUP_DIR" -name "astrooverz_*.sql" -mtime +7 -delete 2>/dev/null
find "$BACKUP_DIR" -name "config_*.tar.gz" -mtime +7 -delete 2>/dev/null

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup completed" >> "$LOG_FILE"
EOF
    
    chmod +x /opt/astrooverz/backup.sh
    
    # Add to crontab (daily at 2 AM)
    (crontab -l 2>/dev/null; echo "0 2 * * * /opt/astrooverz/backup.sh") | crontab -
    
    print_success "Backup system configured"
}

# Function to setup project directory
setup_project_directory() {
    print_status "Setting up project directory..."
    
    # Create project directory
    mkdir -p "$PROJECT_DIR"
    
    # Set proper permissions
    chown -R root:root "$PROJECT_DIR"
    chmod 755 "$PROJECT_DIR"
    
    print_success "Project directory created: $PROJECT_DIR"
}

# Function to setup environment
setup_environment() {
    print_status "Setting up environment configuration..."
    
    cd "$PROJECT_DIR"
    
    # Create basic .env file
    cat > .env << 'EOF'
# Astrooverz Production Environment Configuration

# Database Configuration
DATABASE_URL=postgresql://astrooverz:astrooverz123@db:5432/astrooverz

# Redis Configuration
REDIS_URL=redis://redis:6379

# Panchangam Configuration
AYANAMSA=Lahiri
MONTH_SYSTEM=Amanta
DAY_BOUNDARY=sunrise

# Job Scheduling Configuration
SCHED_ENABLED=true
CITY_PRECOMPUTE=IN_TOP200
PRECOMPUTE_DAYS=30
PRECOMPUTE_TIME=02:30

# API Configuration
API_V1_STR=/api
PROJECT_NAME=Astrooverz Numerology API

# CORS Configuration
BACKEND_CORS_ORIGINS=["*"]

# Default Timezone
DEFAULT_TZ=Asia/Kolkata
EOF
    
    print_success "Environment configuration created"
}

# Function to setup systemd service
setup_systemd_service() {
    print_status "Setting up systemd service..."
    
    # Create systemd service file
    cat > /etc/systemd/system/astrooverz.service << 'EOF'
[Unit]
Description=Astrooverz Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/astrooverz
ExecStart=/usr/local/bin/docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF
    
    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable astrooverz.service
    
    print_success "Systemd service configured"
}

# Function to setup SSL certificates (Let's Encrypt)
setup_ssl() {
    print_status "Setting up SSL certificates..."
    
    # Install certbot
    apt install -y certbot python3-certbot-nginx
    
    print_warning "SSL setup requires domain configuration"
    print_warning "Run the following command after setting up your domain:"
    print_warning "certbot --nginx -d yourdomain.com"
    
    print_success "SSL tools installed"
}

# Function to optimize system
optimize_system() {
    print_status "Optimizing system..."
    
    # Increase file limits
    cat >> /etc/security/limits.conf << 'EOF'
* soft nofile 65536
* hard nofile 65536
* soft nproc 65536
* hard nproc 65536
EOF
    
    # Optimize kernel parameters
    cat >> /etc/sysctl.conf << 'EOF'
# Network optimizations
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 65536 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_congestion_control = bbr

# File system optimizations
fs.file-max = 2097152
vm.swappiness = 10
EOF
    
    # Apply sysctl changes
    sysctl -p
    
    print_success "System optimized"
}

# Function to show final instructions
show_final_instructions() {
    print_success "VPS setup completed successfully!"
    
    echo ""
    echo "=========================================="
    echo "Next Steps:"
    echo "=========================================="
    echo ""
    echo "1. Clone your repository:"
    echo "   cd $PROJECT_DIR"
    echo "   git clone https://github.com/YOUR_USERNAME/astro2.0.git ."
    echo ""
    echo "2. Configure environment:"
    echo "   nano .env"
    echo ""
    echo "3. Deploy the application:"
    echo "   chmod +x scripts/deploy.sh"
    echo "   ./scripts/deploy.sh deploy"
    echo ""
    echo "4. Configure your domain (if applicable):"
    echo "   certbot --nginx -d yourdomain.com"
    echo ""
    echo "5. Monitor the application:"
    echo "   ./scripts/deploy.sh status"
    echo "   tail -f /var/log/astrooverz/monitor.log"
    echo ""
    echo "=========================================="
    echo "Useful Commands:"
    echo "=========================================="
    echo ""
    echo "Check status:     ./scripts/deploy.sh status"
    echo "View logs:        ./scripts/deploy.sh logs"
    echo "Restart services: ./scripts/deploy.sh restart"
    echo "Update app:       ./scripts/deploy.sh update"
    echo "Backup database:  ./scripts/deploy.sh backup"
    echo ""
    echo "=========================================="
    echo "Security Notes:"
    echo "=========================================="
    echo ""
    echo "- Firewall is configured (ports 22, 80, 443 open)"
    echo "- Fail2ban is active for SSH protection"
    echo "- Regular backups are scheduled (daily at 2 AM)"
    echo "- Monitoring is active (every 5 minutes)"
    echo ""
    echo "Log files:"
    echo "- Setup log: $LOG_FILE"
    echo "- Monitor log: /var/log/astrooverz/monitor.log"
    echo "- Backup log: /var/log/astrooverz/backup.log"
    echo ""
}

# Main setup function
main_setup() {
    print_status "Starting VPS setup for Astrooverz..."
    
    check_root
    setup_logging
    update_system
    install_essential_packages
    install_docker
    install_docker_compose
    setup_firewall
    setup_fail2ban
    setup_log_rotation
    setup_project_directory
    setup_environment
    setup_systemd_service
    setup_monitoring
    setup_backup
    setup_ssl
    optimize_system
    
    show_final_instructions
}

# Function to show help
show_help() {
    echo "Astrooverz VPS Setup Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup      - Full VPS setup (default)"
    echo "  docker     - Install Docker only"
    echo "  security   - Setup security (firewall, fail2ban)"
    echo "  monitoring - Setup monitoring and backup"
    echo "  help       - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup      # Full setup"
    echo "  $0 docker     # Install Docker only"
    echo "  $0 security   # Setup security only"
}

# Main script logic
main() {
    case "${1:-setup}" in
        setup)
            main_setup
            ;;
        docker)
            check_root
            setup_logging
            install_docker
            install_docker_compose
            ;;
        security)
            check_root
            setup_logging
            setup_firewall
            setup_fail2ban
            ;;
        monitoring)
            check_root
            setup_logging
            setup_monitoring
            setup_backup
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
