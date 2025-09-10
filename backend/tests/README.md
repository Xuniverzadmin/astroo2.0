# Test Suite for Numerology Application

This directory contains comprehensive tests for the panchangam engine and related functionality.

## Test Structure

### Test Files

- **`test_panchangam_core.py`**: Core panchangam calculation tests
- **`test_health_endpoints.py`**: Health check endpoint tests
- **`__init__.py`**: Test package initialization

### Test Categories

#### Unit Tests (`TestPanchangamCore`)
- **Tithi Calculations**: Test tithi computation with known values
- **Nakshatra Calculations**: Test nakshatra computation with known values
- **Yoga Calculations**: Test yoga computation with known values
- **Karana Calculations**: Test karana computation with known values
- **Sunrise/Sunset Bounds**: Test timing calculations for different locations
- **Rahu/Yama/Gulikai Timing**: Test inauspicious period calculations
- **Hora Calculations**: Test planetary hour calculations
- **Gowri Panchangam**: Test auspicious/inauspicious period calculations
- **Complete Panchangam Assembly**: Test end-to-end panchangam generation
- **Known Dates Sanity**: Test calculations for important festival dates
- **Edge Cases**: Test boundary conditions and error handling
- **Astronomy Functions**: Test core astronomy calculations
- **Performance Tests**: Test calculation speed and efficiency

#### Integration Tests (`TestPanchangamIntegration`)
- **Multiple Locations**: Test panchangam for different Indian cities
- **Date Range Consistency**: Test consistency across multiple dates
- **Cross-Function Integration**: Test how different functions work together

#### Health Endpoint Tests (`TestHealthEndpoints`)
- **Root Health Check**: Test `/healthz` endpoint
- **API Health Check**: Test `/api/healthz` endpoint
- **Response Format**: Test correct JSON response format
- **Performance**: Test response time requirements
- **HTTP Methods**: Test that only GET requests are accepted
- **Headers**: Test appropriate HTTP headers
- **Consistency**: Test consistent responses across multiple requests

#### Health Integration Tests (`TestHealthEndpointIntegration`)
- **Multi-Endpoint Testing**: Test health endpoints with other endpoints
- **Load Testing**: Test health endpoints under concurrent load

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

### Test Runner Script

Use the provided test runner script for easy test execution:

```bash
# Run all tests
python run_tests.py all

# Run unit tests only
python run_tests.py unit

# Run integration tests only
python run_tests.py integration

# Run health endpoint tests only
python run_tests.py health

# Run tests with coverage report
python run_tests.py coverage

# Run only fast tests (exclude slow tests)
python run_tests.py fast

# Run a specific test file
python run_tests.py specific --test-path tests/test_panchangam_core.py

# Run a specific test function
python run_tests.py specific --test-path tests/test_panchangam_core.py::TestPanchangamCore::test_compute_tithi_basic
```

### Direct Pytest Commands

You can also run tests directly with pytest:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_panchangam_core.py -v

# Run specific test class
pytest tests/test_panchangam_core.py::TestPanchangamCore -v

# Run specific test function
pytest tests/test_panchangam_core.py::TestPanchangamCore::test_compute_tithi_basic -v

# Run with coverage
pytest tests/ --cov=numerology_app --cov-report=html

# Run only fast tests
pytest tests/ -m "not slow" -v

# Run with detailed output
pytest tests/ -v -s --tb=long
```

## Test Data and Known Values

### Test Locations

The tests use several Indian cities for location-based testing:

- **Chennai**: 13.0827°N, 80.2707°E (Primary test location)
- **Mumbai**: 19.0760°N, 72.8777°E
- **Delhi**: 28.7041°N, 77.1025°E
- **Bangalore**: 12.9716°N, 77.5946°E
- **Hyderabad**: 17.3850°N, 78.4867°E

### Test Dates

Important dates used for testing:

- **Spring Equinox**: March 15, 2024
- **Summer Solstice**: June 21, 2024
- **Winter Solstice**: December 21, 2024
- **Diwali 2024**: October 31, 2024
- **Holi 2024**: March 25, 2024
- **Maha Shivaratri 2024**: March 8, 2024

### Expected Values

#### Tithi Ranges
- Tithi numbers: 1-30
- Tithi progress: 0.0-1.0
- Tithi percentage: 0.0-100.0

#### Nakshatra Ranges
- Nakshatra numbers: 1-27
- Nakshatra progress: 0.0-1.0
- Nakshatra percentage: 0.0-100.0

#### Yoga Ranges
- Yoga numbers: 1-27
- Yoga progress: 0.0-1.0
- Yoga percentage: 0.0-100.0

#### Timing Bounds
- **Sunrise**: 5:30 AM - 8:00 AM IST (varies by location and season)
- **Sunset**: 5:00 PM - 8:00 PM IST (varies by location and season)
- **Rahu/Yama/Gulikai Duration**: 1.5 hours each
- **Hora Duration**: 1 hour each (12 horas total)

## Test Coverage

### Target Coverage
- **Minimum Coverage**: 80%
- **Target Coverage**: 90%+
- **Critical Functions**: 100% coverage

### Coverage Areas
- **Core Calculations**: Tithi, Nakshatra, Yoga, Karana
- **Timing Calculations**: Sunrise, Sunset, Rahu Kalam, etc.
- **Astronomy Functions**: Sun/Moon longitude calculations
- **API Endpoints**: Health checks and panchangam endpoints
- **Error Handling**: Edge cases and boundary conditions

## Performance Benchmarks

### Response Time Requirements
- **Health Endpoints**: < 1 second
- **Panchangam Calculation**: < 5 seconds
- **Average Panchangam**: < 2 seconds
- **Concurrent Health Checks**: < 2 seconds average

### Load Testing
- **Concurrent Requests**: 20 simultaneous health checks
- **Date Range Testing**: 30 consecutive days
- **Location Testing**: 5 different cities

## Test Configuration

### Pytest Configuration (`pytest.ini`)
- **Test Discovery**: Automatic test discovery in `tests/` directory
- **Output Format**: Verbose with short traceback
- **Markers**: Support for `slow`, `integration`, `unit` markers
- **Warnings**: Filtered deprecation warnings

### Test Markers
- **`@pytest.mark.slow`**: Mark slow tests
- **`@pytest.mark.integration`**: Mark integration tests
- **`@pytest.mark.unit`**: Mark unit tests

## Continuous Integration

### GitHub Actions (Recommended)
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python run_tests.py coverage
```

### Local Development
```bash
# Run tests before committing
python run_tests.py all

# Run with coverage
python run_tests.py coverage

# Check coverage report
open htmlcov/index.html
```

## Troubleshooting

### Common Issues

#### Import Errors
```
ModuleNotFoundError: No module named 'numerology_app'
```
**Solution**: Ensure you're running tests from the `backend/` directory

#### Skyfield Errors
```
ImportError: cannot import name 'load' from 'skyfield.api'
```
**Solution**: Install skyfield: `pip install skyfield==1.49`

#### Redis Connection Errors
```
redis.exceptions.ConnectionError: Error connecting to Redis
```
**Solution**: Tests should work without Redis, but ensure Redis is available for integration tests

#### Database Connection Errors
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Solution**: Tests should work without database, but ensure PostgreSQL is available for integration tests

### Debug Mode
```bash
# Run tests with debug output
pytest tests/ -v -s --tb=long --pdb

# Run specific test with debug
pytest tests/test_panchangam_core.py::TestPanchangamCore::test_compute_tithi_basic -v -s --pdb
```

### Test Isolation
Each test is designed to be independent and can be run in isolation:
```bash
# Run single test
pytest tests/test_panchangam_core.py::TestPanchangamCore::test_compute_tithi_basic -v

# Run tests in random order
pytest tests/ --random-order
```

## Adding New Tests

### Test Naming Convention
- **Test Files**: `test_*.py`
- **Test Classes**: `Test*`
- **Test Functions**: `test_*`

### Test Structure
```python
class TestNewFeature:
    """Test cases for new feature."""
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        # Arrange
        input_data = "test"
        
        # Act
        result = function_under_test(input_data)
        
        # Assert
        assert result == expected_output
    
    def test_edge_case(self):
        """Test edge case."""
        # Test boundary conditions
        pass
```

### Test Data
- Use realistic test data
- Include edge cases and boundary conditions
- Test both success and failure scenarios
- Use known values where possible

### Performance Tests
```python
def test_performance(self):
    """Test performance requirements."""
    import time
    
    start_time = time.time()
    result = expensive_function()
    end_time = time.time()
    
    assert end_time - start_time < 5.0  # 5 second limit
    assert result is not None
```

## Test Maintenance

### Regular Updates
- Update test data for new years
- Add tests for new features
- Update performance benchmarks
- Review and update test coverage

### Test Review Checklist
- [ ] All new code has corresponding tests
- [ ] Tests cover edge cases and error conditions
- [ ] Performance tests validate response time requirements
- [ ] Integration tests verify end-to-end functionality
- [ ] Test documentation is updated
- [ ] Coverage meets minimum requirements (80%+)
