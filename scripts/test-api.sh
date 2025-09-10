#!/bin/bash

# Astrooverz API Testing Script
# This script tests the backend API endpoints to verify they're working correctly

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_URL="http://backend:8000"
LOCAL_URL="http://localhost:8000"
TEST_DATE="2025-09-10"
TEST_LAT="13.0827"
TEST_LON="80.2707"
TEST_TZ="Asia/Kolkata"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to test health endpoint
test_health_endpoint() {
    local url="$1"
    local name="$2"
    
    print_status "Testing $name health endpoint: $url/healthz"
    
    if response=$(curl -s -w "\n%{http_code}" "$url/healthz" 2>/dev/null); then
        http_code=$(echo "$response" | tail -n1)
        body=$(echo "$response" | head -n -1)
        
        if [ "$http_code" = "200" ]; then
            print_success "$name health endpoint is working"
            echo "Response: $body"
            return 0
        else
            print_error "$name health endpoint returned HTTP $http_code"
            echo "Response: $body"
            return 1
        fi
    else
        print_error "$name health endpoint is not accessible"
        return 1
    fi
}

# Function to test API health endpoint
test_api_health_endpoint() {
    local url="$1"
    local name="$2"
    
    print_status "Testing $name API health endpoint: $url/api/healthz"
    
    if response=$(curl -s -w "\n%{http_code}" "$url/api/healthz" 2>/dev/null); then
        http_code=$(echo "$response" | tail -n1)
        body=$(echo "$response" | head -n -1)
        
        if [ "$http_code" = "200" ]; then
            print_success "$name API health endpoint is working"
            echo "Response: $body"
            return 0
        else
            print_error "$name API health endpoint returned HTTP $http_code"
            echo "Response: $body"
            return 1
        fi
    else
        print_error "$name API health endpoint is not accessible"
        return 1
    fi
}

# Function to test panchangam API
test_panchangam_api() {
    local url="$1"
    local name="$2"
    local date="$3"
    local lat="$4"
    local lon="$5"
    local tz="$6"
    
    print_status "Testing $name panchangam API: $url/api/panchangam/$date?lat=$lat&lon=$lon&tz=$tz"
    
    local api_url="$url/api/panchangam/$date?lat=$lat&lon=$lon&tz=$tz"
    
    if response=$(curl -s -w "\n%{http_code}" "$api_url" 2>/dev/null); then
        http_code=$(echo "$response" | tail -n1)
        body=$(echo "$response" | head -n -1)
        
        if [ "$http_code" = "200" ]; then
            print_success "$name panchangam API is working"
            echo "Response (first 400 chars):"
            echo "$body" | head -c 400
            echo ""
            echo "..."
            return 0
        else
            print_error "$name panchangam API returned HTTP $http_code"
            echo "Response: $body"
            return 1
        fi
    else
        print_error "$name panchangam API is not accessible"
        return 1
    fi
}

# Function to test multiple dates
test_multiple_dates() {
    local url="$1"
    local name="$2"
    
    print_status "Testing $name panchangam API with multiple dates..."
    
    local dates=("2024-03-15" "2024-06-21" "2024-12-21" "2025-01-01" "2025-09-10")
    local success_count=0
    local total_count=${#dates[@]}
    
    for date in "${dates[@]}"; do
        if test_panchangam_api "$url" "$name" "$date" "$TEST_LAT" "$TEST_LON" "$TEST_TZ" >/dev/null 2>&1; then
            ((success_count++))
        fi
    done
    
    if [ $success_count -eq $total_count ]; then
        print_success "All $total_count date tests passed for $name"
        return 0
    else
        print_warning "$success_count/$total_count date tests passed for $name"
        return 1
    fi
}

# Function to test multiple locations
test_multiple_locations() {
    local url="$1"
    local name="$2"
    
    print_status "Testing $name panchangam API with multiple locations..."
    
    local locations=(
        "13.0827,80.2707,Asia/Kolkata:Chennai"
        "19.0760,72.8777,Asia/Kolkata:Mumbai"
        "28.7041,77.1025,Asia/Kolkata:Delhi"
        "12.9716,77.5946,Asia/Kolkata:Bangalore"
        "17.3850,78.4867,Asia/Kolkata:Hyderabad"
    )
    
    local success_count=0
    local total_count=${#locations[@]}
    
    for location in "${locations[@]}"; do
        IFS=':' read -r coords city <<< "$location"
        IFS=',' read -r lat lon tz <<< "$coords"
        
        if test_panchangam_api "$url" "$name" "$TEST_DATE" "$lat" "$lon" "$tz" >/dev/null 2>&1; then
            ((success_count++))
        fi
    done
    
    if [ $success_count -eq $total_count ]; then
        print_success "All $total_count location tests passed for $name"
        return 0
    else
        print_warning "$success_count/$total_count location tests passed for $name"
        return 1
    fi
}

# Function to test API performance
test_api_performance() {
    local url="$1"
    local name="$2"
    
    print_status "Testing $name API performance..."
    
    local start_time=$(date +%s.%N)
    
    for i in {1..10}; do
        curl -s "$url/api/panchangam/$TEST_DATE?lat=$TEST_LAT&lon=$TEST_LON&tz=$TEST_TZ" >/dev/null 2>&1
    done
    
    local end_time=$(date +%s.%N)
    local duration=$(echo "$end_time - $start_time" | bc -l)
    local avg_duration=$(echo "scale=3; $duration / 10" | bc -l)
    
    print_status "Average response time for $name: ${avg_duration}s"
    
    if (( $(echo "$avg_duration < 5.0" | bc -l) )); then
        print_success "Performance is good (< 5s average)"
        return 0
    else
        print_warning "Performance is slow (> 5s average)"
        return 1
    fi
}

# Function to test all endpoints for a URL
test_all_endpoints() {
    local url="$1"
    local name="$2"
    
    print_status "Testing all endpoints for $name ($url)"
    echo "=========================================="
    
    local total_tests=0
    local passed_tests=0
    
    # Test health endpoint
    ((total_tests++))
    if test_health_endpoint "$url" "$name"; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test API health endpoint
    ((total_tests++))
    if test_api_health_endpoint "$url" "$name"; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test panchangam API
    ((total_tests++))
    if test_panchangam_api "$url" "$name" "$TEST_DATE" "$TEST_LAT" "$TEST_LON" "$TEST_TZ"; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test multiple dates
    ((total_tests++))
    if test_multiple_dates "$url" "$name"; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test multiple locations
    ((total_tests++))
    if test_multiple_locations "$url" "$name"; then
        ((passed_tests++))
    fi
    echo ""
    
    # Test performance
    ((total_tests++))
    if test_api_performance "$url" "$name"; then
        ((passed_tests++))
    fi
    echo ""
    
    echo "=========================================="
    print_status "Test Summary for $name: $passed_tests/$total_tests tests passed"
    
    if [ $passed_tests -eq $total_tests ]; then
        print_success "All tests passed for $name!"
        return 0
    else
        print_warning "Some tests failed for $name"
        return 1
    fi
}

# Function to show help
show_help() {
    echo "Astrooverz API Testing Script"
    echo ""
    echo "Usage: $0 [COMMAND] [URL]"
    echo ""
    echo "Commands:"
    echo "  test        - Test all endpoints (default)"
    echo "  health      - Test health endpoints only"
    echo "  panchangam  - Test panchangam API only"
    echo "  performance - Test API performance only"
    echo "  help        - Show this help message"
    echo ""
    echo "URLs:"
    echo "  backend     - Test backend service (http://backend:8000)"
    echo "  local       - Test local service (http://localhost:8000)"
    echo "  custom      - Test custom URL (provide as second argument)"
    echo ""
    echo "Examples:"
    echo "  $0 test backend                    # Test all endpoints on backend service"
    echo "  $0 health local                   # Test health endpoints on local service"
    echo "  $0 panchangam http://example.com  # Test panchangam API on custom URL"
    echo "  $0 performance backend            # Test performance on backend service"
}

# Function to run specific tests
run_health_tests() {
    local url="$1"
    local name="$2"
    
    print_status "Running health tests for $name ($url)"
    echo "=========================================="
    
    test_health_endpoint "$url" "$name"
    echo ""
    test_api_health_endpoint "$url" "$name"
}

run_panchangam_tests() {
    local url="$1"
    local name="$2"
    
    print_status "Running panchangam tests for $name ($url)"
    echo "=========================================="
    
    test_panchangam_api "$url" "$name" "$TEST_DATE" "$TEST_LAT" "$TEST_LON" "$TEST_TZ"
    echo ""
    test_multiple_dates "$url" "$name"
    echo ""
    test_multiple_locations "$url" "$name"
}

run_performance_tests() {
    local url="$1"
    local name="$2"
    
    print_status "Running performance tests for $name ($url)"
    echo "=========================================="
    
    test_api_performance "$url" "$name"
}

# Main script logic
main() {
    local command="${1:-test}"
    local url_input="${2:-backend}"
    
    # Determine URL based on input
    case "$url_input" in
        backend)
            url="$BACKEND_URL"
            name="Backend"
            ;;
        local)
            url="$LOCAL_URL"
            name="Local"
            ;;
        *)
            url="$url_input"
            name="Custom"
            ;;
    esac
    
    print_status "Starting API tests for $name ($url)"
    echo ""
    
    case "$command" in
        test)
            test_all_endpoints "$url" "$name"
            ;;
        health)
            run_health_tests "$url" "$name"
            ;;
        panchangam)
            run_panchangam_tests "$url" "$name"
            ;;
        performance)
            run_performance_tests "$url" "$name"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
