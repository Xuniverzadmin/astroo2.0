# Caddy Dockerfile for multi-architecture builds
FROM caddy:2-alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile

# Create non-root user for security
RUN addgroup -g 1001 -S caddy && \
    adduser -S -D -H -u 1001 -h /var/lib/caddy -s /sbin/nologin -G caddy -g caddy caddy

# Set proper permissions
RUN chown -R caddy:caddy /etc/caddy && \
    chown -R caddy:caddy /var/lib/caddy && \
    chown -R caddy:caddy /var/log/caddy

# Switch to non-root user
USER caddy

# Expose ports
EXPOSE 80 443

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:2019/config/ || exit 1

# Start Caddy
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
