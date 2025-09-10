# Festivals Package

This package provides a Domain Specific Language (DSL) for defining Hindu festivals and a service for building festival calendars and muhurtham calculations.

## Components

### 1. rules.py - Festival Rules DSL

Defines a simple DSL for specifying when festivals occur based on panchangam elements.

#### DSL Syntax

The DSL supports the following operators and conditions:

**Panchangam Elements:**
- `tithi=N (shukla|krishna)` - Tithi number and paksha
- `nakshatra=N` - Nakshatra number (1-27)
- `yoga=N` - Yoga number (1-27)
- `karana=NAME` - Karana name

**Time Conditions:**
- `weekday=NAME` - Day of week (monday, tuesday, etc.)
- `pradosha_kala` - Pradosha time (1.5 hours before sunset)
- `brahma_muhurta` - Brahma muhurta (1.5 hours before sunrise)
- `amavasya` - New moon day
- `purnima` - Full moon day
- `ekadashi` - 11th tithi

**Logical Operators:**
- `&` (AND) - All conditions must be true
- `|` (OR) - Any condition can be true
- `!` (NOT) - Negate a condition
- `()` - Grouping for complex expressions

#### Example Rules

```python
# Maha Shivaratri - 14th tithi of Krishna paksha
FestivalRule(
    name="Maha Shivaratri",
    when="tithi=14 krishna",
    observe="sunset",
    region="ALL"
)

# Holi - 15th tithi of Krishna paksha with specific nakshatra
FestivalRule(
    name="Holi",
    when="tithi=15 krishna & nakshatra=1",
    observe="sunset",
    region="ALL"
)

# Complex condition with multiple elements
FestivalRule(
    name="Special Festival",
    when="(tithi=10 shukla | tithi=10 krishna) & !weekday=sunday",
    observe="sunrise",
    region="TN"
)
```

#### Predefined Festival Rules

The module includes predefined rules for major Hindu festivals:

- **Major Festivals**: Diwali, Holi, Dussehra, Ganesh Chaturthi, Krishna Janmashtami
- **Regional Festivals**: Pongal (TN), Onam (KL)
- **Religious Observances**: Ekadashi, Amavasya, Purnima
- **Special Days**: Karva Chauth, Navratri, Rama Navami

### 2. service.py - Festival Service

Provides services for building festival calendars and calculating muhurtham periods.

#### Key Methods

**build_month(year, month, lat, lon, tz, region)**
- Builds a festival calendar for a specific month
- Evaluates all festival rules against each day
- Returns list of festival day dictionaries

**build_muhurtham_periods(date, lat, lon, tz, event_type)**
- Calculates auspicious time periods for specific events
- Supports event types: marriage, house_warming, business_opening, vehicle_purchase, general
- Returns list of muhurtham period dictionaries

#### Event Types and Muhurtham Rules

**Marriage:**
- Preferred periods: amrutha, siddha, laabha, dhanam
- Avoid periods: marana, rogam, kantaka
- Timing: Morning or evening, 2-4 hours duration

**House Warming:**
- Preferred periods: amrutha, siddha, laabha
- Avoid periods: marana, rogam
- Timing: Morning, 1-2 hours duration

**Business Opening:**
- Preferred periods: amrutha, siddha, laabha, dhanam
- Avoid periods: marana, rogam
- Timing: Morning, 1-2 hours duration

**Vehicle Purchase:**
- Preferred periods: amrutha, siddha, laabha
- Avoid periods: marana, rogam, kantaka
- Timing: Morning, 1 hour duration

## API Integration

### /api/festivals Endpoint

```http
GET /api/festivals?year=2024&month=3&lat=13.0827&lon=80.2707&tz=Asia/Kolkata&region=TN
```

**Parameters:**
- `year`: Year (1900-2100)
- `month`: Month (1-12), optional
- `lat`: Latitude in degrees
- `lon`: Longitude in degrees
- `tz`: Timezone string
- `region`: Region code (ALL, TN, KL, KA, AP, etc.)

**Response:**
```json
{
  "year": 2024,
  "month": 3,
  "region": "TN",
  "location": {
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata"
  },
  "festivals": [
    {
      "date": "2024-03-08",
      "name": "Maha Shivaratri",
      "description": "Great night of Lord Shiva",
      "festival_type": "religious",
      "importance": "high",
      "is_public_holiday": true,
      "rituals": {...},
      "customs": {...},
      "auspicious_times": {...}
    }
  ],
  "total_count": 1
}
```

### /api/muhurtham Endpoint

```http
GET /api/muhurtham?date=2024-03-15&lat=13.0827&lon=80.2707&tz=Asia/Kolkata&event_type=marriage
```

**Parameters:**
- `date`: Date for muhurtham calculation (YYYY-MM-DD)
- `lat`: Latitude in degrees
- `lon`: Longitude in degrees
- `tz`: Timezone string
- `event_type`: Type of event (marriage, house_warming, business_opening, vehicle_purchase, general)

**Response:**
```json
{
  "date": "2024-03-15",
  "event_type": "marriage",
  "location": {
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata"
  },
  "auspicious_periods": [
    {
      "name": "amrutha",
      "start": "2024-03-15T06:00:00+05:30",
      "end": "2024-03-15T07:30:00+05:30",
      "duration_hours": 1.5,
      "suitability": "Excellent",
      "recommended_activities": ["All auspicious activities", "Starting new ventures"],
      "avoid_activities": ["None"]
    }
  ],
  "panchangam_context": {...},
  "total_periods": 4
}
```

## Region Codes

- `ALL`: All regions (national festivals)
- `TN`: Tamil Nadu
- `KL`: Kerala
- `KA`: Karnataka
- `AP`: Andhra Pradesh
- `TS`: Telangana
- `MH`: Maharashtra
- `GJ`: Gujarat
- `RJ`: Rajasthan
- `UP`: Uttar Pradesh
- `MP`: Madhya Pradesh
- `WB`: West Bengal
- `OR`: Odisha
- `AS`: Assam
- `PB`: Punjab
- `HR`: Haryana
- `DL`: Delhi
- `JK`: Jammu and Kashmir
- `HP`: Himachal Pradesh
- `UK`: Uttarakhand
- `BR`: Bihar
- `JH`: Jharkhand
- `CT`: Chhattisgarh
- `GA`: Goa
- `MN`: Manipur
- `MZ`: Mizoram
- `NL`: Nagaland
- `TR`: Tripura
- `SK`: Sikkim
- `AR`: Arunachal Pradesh
- `ML`: Meghalaya

## Usage Examples

### Adding a New Festival Rule

```python
from .rules import FestivalRule, FestivalType, Importance

# Add a new regional festival
new_festival = FestivalRule(
    name="Local Festival",
    when="tithi=5 shukla & weekday=monday",
    observe="sunrise",
    region="TN",
    festival_type=FestivalType.REGIONAL,
    importance=Importance.MEDIUM,
    description="Local harvest festival",
    is_public_holiday=False
)

# Add to FESTIVAL_RULES list
FESTIVAL_RULES.append(new_festival)
```

### Custom Festival Evaluation

```python
from .rules import FestivalRuleEvaluator
from .service import festival_service

# Create evaluator
evaluator = FestivalRuleEvaluator()

# Check if a rule matches a specific date
rule = FestivalRule(name="Test", when="tithi=15 krishna")
matches = evaluator.evaluate_rule(rule, date(2024, 3, 8), 13.0827, 80.2707, "Asia/Kolkata")

# Build festival calendar
festivals = festival_service.build_month(2024, 3, 13.0827, 80.2707, "Asia/Kolkata", "TN")
```

## Database Integration

The service includes methods for saving and retrieving festival data from the database:

- `save_festivals_to_db(festivals)` - Save festival data to database
- `get_festivals_from_db(year, month, region)` - Retrieve festivals from database

This allows for caching festival calculations and building historical festival calendars.
