# Planet Labs Satellite Geolocation Integration

**Satellite Intelligence for RIPA DDO Operations**

Integration with Planet Labs (https://www.planet.com) for geospatial intelligence supporting Deliberate Detention Operations.

---

## 🛰️ Overview

The Planet Labs integration provides satellite imagery and geospatial intelligence for:
- **Subject location verification** using satellite imagery
- **DDO operation planning** with area suitability assessment
- **Detention location optimization** based on satellite analysis
- **Movement pattern tracking** from historical GPS data
- **Operational intelligence** with points of interest identification

---

## 🔑 Key Features

### 1. Satellite Imagery Search
- Search Planet's archive for imagery at any global location
- Filter by date range, cloud cover, and resolution
- Access to PlanetScope constellation (3m resolution)
- Multiple imagery sources (PSScene, RapidEye, SkySat)

### 2. Geolocation Intelligence
- Comprehensive location analysis from satellite data
- Points of interest (POI) identification
- Access route and escape route analysis
- Area assessment for DDO suitability
- Officer positioning recommendations

### 3. DDO Area Assessment
Satellite-derived intelligence for detention planning:
- **Public exposure level** (low/medium/high)
- **Crowd density** assessment
- **Visibility from main roads**
- **Officer approach difficulty**
- **Subject escape route analysis**
- **Evidence preservation environment**
- **Operational recommendations** with optimal time windows

### 4. Subject Movement Tracking
- Analyze historical GPS data
- Identify frequently visited locations
- Calculate total distance traveled
- Movement pattern classification (routine vs. irregular)
- Optimal detention location recommendations

---

## 🚀 Setup

### Option 1: With Real Planet API (Production)

1. **Get Planet API Key**
```bash
# Sign up at https://www.planet.com/
# Navigate to Account Settings → API Keys
# Copy your API key
```

2. **Set Environment Variable**
```bash
# Add to .env file
PLANET_API_KEY=your_planet_api_key_here

# Or export directly
export PLANET_API_KEY=your_planet_api_key_here
```

3. **Verify Setup**
```bash
python planet_geolocation.py
```

### Option 2: Demo Mode (No API Key Required)

The system works in **demo mode** without a Planet API key. It generates realistic satellite imagery metadata for testing and demonstration purposes.

```bash
# Just run without setting PLANET_API_KEY
python planet_geolocation.py
```

---

## 📖 Usage Examples

### Example 1: Search Satellite Imagery

```python
from planet_geolocation import PlanetGeolocationService

# Initialize service
planet = PlanetGeolocationService()  # Uses PLANET_API_KEY env var

# Search for imagery at a location
latitude = 53.4808  # Manchester, UK
longitude = -2.2426

images = planet.search_imagery(
    latitude=latitude,
    longitude=longitude,
    radius_km=1.0,
    max_cloud_cover=0.2  # 20% max cloud cover
)

print(f"Found {len(images)} satellite images")
for img in images:
    print(f"  {img.image_id}: {img.acquisition_time} ({img.cloud_cover*100:.1f}% clouds)")
```

### Example 2: Get Geolocation Intelligence

```python
# Get comprehensive intel for a location
intel = planet.get_location_intelligence(
    latitude=53.4808,
    longitude=-2.2426,
    location_name="Subject residence - Manchester",
    subject_id="RUS_001"
)

print(f"Confidence: {intel.confidence*100:.0f}%")
print(f"Satellite images: {len(intel.satellite_images)}")
print(f"Points of interest: {len(intel.points_of_interest)}")

# Access DDO area assessment
if intel.area_assessment:
    assessment = intel.area_assessment
    print(f"Public Exposure: {assessment['public_exposure_level']}")
    print(f"Best Time Window: {assessment['best_time_window']}")
    print(f"Operational Recommendation: {assessment['operational_recommendation']}")
```

### Example 3: Enhance Detention Location

```python
from models_ripa import DetentionLocation
from planet_geolocation import PlanetGeolocationService

# Create detention location
location = DetentionLocation(
    location_id="LOC_001",
    description="Subject's residence",
    location_type="home",
    address="Manchester city centre",
    latitude=53.4808,
    longitude=-2.2426,
    public_exposure_level="MEDIUM",
    crowd_level="LOW",
    access_difficulty="MODERATE",
    escape_routes_count=2
)

# Enhance with satellite intelligence
planet = PlanetGeolocationService()
enhanced_location = planet.enhance_detention_location(location)

# Now includes satellite metadata
print(f"Satellite Coverage: {enhanced_location.satellite_coverage}")
print(f"Geospatial Confidence: {enhanced_location.geospatial_confidence}")
```

### Example 4: Track Subject Movement

```python
from datetime import datetime, timedelta

# Historical GPS locations (lat, lon, timestamp)
locations = [
    (53.4808, -2.2426, datetime.now() - timedelta(days=7)),
    (53.4812, -2.2430, datetime.now() - timedelta(days=6)),
    (53.4808, -2.2426, datetime.now() - timedelta(days=5)),  # Repeat visit
    (53.4808, -2.2426, datetime.now() - timedelta(days=4)),  # Repeat visit
    (53.4850, -2.2500, datetime.now() - timedelta(days=3)),
]

# Analyze movement patterns
analysis = planet.track_subject_movement(
    subject_id="RUS_001",
    historical_locations=locations
)

print(f"Total distance traveled: {analysis['total_distance_traveled_km']} km")
print(f"Movement pattern: {analysis['movement_pattern']}")
print(f"Frequent locations identified: {len(analysis['frequent_locations'])}")

# Get optimal detention locations
for loc in analysis['optimal_detention_locations']:
    print(f"  Rank {loc['rank']}: {loc['visit_count']} visits")
    print(f"  Lat: {loc['latitude']}, Lon: {loc['longitude']}")
    print(f"  Detention suitability: {loc['detention_suitability']}")
```

### Example 5: Create Live Location Data

```python
# Create RIPA-compliant live location data with satellite intel
live_data = planet.create_live_location_data(
    latitude=53.4808,
    longitude=-2.2426,
    location_name="Subject residence",
    location_type="residence"
)

print(f"Location: {live_data.location_description}")
print(f"Accuracy: {live_data.accuracy_meters}m")
print(f"Collection method: {live_data.collection_method}")
print(f"Satellite images available: {live_data.satellite_images_available}")
print(f"RIPA authorized: {live_data.ripa_authorized}")
```

---

## 🎯 DDO Integration

### Automatic DDO Area Assessment

The Planet integration automatically assesses locations for DDO suitability:

**Assessment Criteria:**
- **Public Exposure**: Low/Medium/High based on satellite imagery
- **Crowd Density**: Pedestrian traffic analysis
- **Visibility**: Sightlines from main roads
- **Access Routes**: Officer approach paths
- **Escape Routes**: Subject egress options
- **Evidence Environment**: Conditions for preservation

**DDO Recommendations:**
- **Optimal Time Windows**: Based on traffic and crowd patterns
- **Officer Positioning**: Entry and containment points
- **Risk Mitigation**: Specific to location characteristics
- **Resource Requirements**: Derived from area complexity

### Integration with DDO Planning Agent

```python
from agent_ddo_planning import DDOPlanningAgent
from planet_geolocation import PlanetGeolocationService

# Initialize services
planet = PlanetGeolocationService()
ddo_planner = DDOPlanningAgent(cohere_client)

# Get satellite intelligence for detention location
intel = planet.get_location_intelligence(
    latitude=53.4808,
    longitude=-2.2426,
    location_name="Target location",
    subject_id="RUS_001"
)

# Use in DDO plan generation
# The DDO planner can incorporate satellite assessment data
# into detention window scoring and risk assessment
```

---

## 📊 Satellite Imagery Details

### Planet Data Products

**PlanetScope (PSScene):**
- **Resolution**: 3.0m ground sample distance (GSD)
- **Revisit Rate**: Daily global coverage
- **Spectral Bands**: 4-band multispectral (RGB + NIR)
- **Swath Width**: 24.6 km × 16.4 km

**RapidEye:**
- **Resolution**: 5.0m GSD
- **5-band multispectral**

**SkySat:**
- **Resolution**: 0.5m GSD (panchromatic), 1.0m (multispectral)
- **Video capability**

### Imagery Metadata

Each satellite image includes:
- **Image ID**: Unique identifier
- **Acquisition Time**: Timestamp of capture
- **Cloud Cover**: Percentage (0.0-1.0)
- **Ground Sample Distance**: Resolution in meters
- **Satellite ID**: Specific satellite identifier
- **Bounding Box**: Geographic extent [west, south, east, north]
- **Thumbnail URL**: Preview image
- **Download URL**: Full resolution image

---

## 🔐 RIPA Compliance

### Authorization Requirements

All satellite geolocation data collection must be RIPA-authorized:

```python
# Example RIPA authorization for satellite intelligence
authorization_ref = "RIPA/2025/GEOINT/PLANET"

# Satellite collection is logged with RIPA compliance
live_data = planet.create_live_location_data(...)
# Automatically includes:
# - ripa_authorized: True
# - authorization_ref: "RIPA/2025/GEOINT/PLANET"
# - collection_method: "planet_satellite"
```

### Legal Framework

**Lawful Authority:**
- RIPA 2000 Part II (Surveillance)
- Directed Surveillance authorization required
- Satellite imagery constitutes directed surveillance if:
  - Systematic monitoring of a specific person/location
  - Conducted for investigatory purposes
  - Likely to obtain private information

**Best Practices:**
- Obtain proper RIPA authorization before satellite tasking
- Document necessity and proportionality
- Maintain chain of custody for imagery
- Include satellite data in evidence packages
- Disclose to defense as required

---

## 💡 Demo Mode Features

When running without a Planet API key, the system generates:

✅ **Realistic satellite imagery metadata**
- 3 recent images (weekly intervals)
- 3.0m GSD resolution
- Low cloud cover (5-11%)
- PlanetScope satellite identifiers

✅ **Comprehensive geolocation intelligence**
- Points of interest analysis
- DDO area assessment
- Route analysis
- Operational recommendations

✅ **Movement tracking analysis**
- Frequent location clustering
- Distance calculations
- Pattern classification

**Demo vs. Production:**
- Demo mode: Simulated metadata, no actual imagery
- Production mode: Real Planet API calls, actual satellite images
- All functionality works in both modes
- Demo mode perfect for training and testing

---

## 🌍 Global Coverage

Planet Labs provides:
- **Daily global coverage** (entire Earth photographed daily)
- **200+ satellites** in orbit
- **Historical archive** back to 2009 (RapidEye)
- **Any location on Earth** supported
- **Rapid revisit** for time-series analysis

**Example Locations for DDO:**
- Urban environments (Manchester, London, Moscow)
- Rural locations
- Border crossing points
- Airports and transport hubs
- Any GPS coordinates worldwide

---

## 📞 Support

**Planet Labs API:**
- Documentation: https://developers.planet.com/
- API Support: support@planet.com
- Rate Limits: Varies by subscription tier

**Integration Issues:**
- Test with `python planet_geolocation.py`
- Check `PLANET_API_KEY` environment variable
- Review error messages (API errors vs. demo mode)

**RIPA Compliance Questions:**
- Consult your legal department
- RIPA oversight body
- Intelligence supervisor

---

## 🔧 Advanced Features

### Custom Image Search

```python
# Search specific item types
images = planet.search_imagery(
    latitude=53.4808,
    longitude=-2.2426,
    item_types=['PSScene', 'REScene', 'SkySatScene'],
    max_cloud_cover=0.1,  # Very clear imagery
    start_date=datetime.now() - timedelta(days=90)
)
```

### Download Satellite Images

```python
# Download actual imagery (requires Planet API key)
success = planet.download_image(
    image=images[0],
    output_path="/path/to/save/image.tif",
    asset_type='analytic'  # or 'visual', 'analytic_sr'
)
```

### Haversine Distance Calculation

```python
# Calculate distance between two GPS points
distance_km = planet._haversine_distance(
    lat1=53.4808, lon1=-2.2426,
    lat2=53.4850, lon2=-2.2500
)
print(f"Distance: {distance_km:.2f} km")
```

---

## ✅ Success Criteria

Planet integration is successful when:

✅ Satellite imagery search returns relevant results
✅ DDO area assessment provides actionable intelligence
✅ Detention locations enhanced with geospatial data
✅ Subject movement patterns identified from GPS history
✅ Live location data includes satellite metadata
✅ RIPA compliance maintained throughout
✅ Demo mode works without API key
✅ Production mode integrates with real Planet API

---

**Status:** ✅ Operational
**Demo Mode:** Available
**Production Ready:** Yes (with Planet API key)
**Last Updated:** 2025-10-21

**Integration complete and ready for DDO operations! 🛰️**
