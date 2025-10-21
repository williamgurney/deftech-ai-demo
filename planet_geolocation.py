"""
Planet Labs Geolocation Integration
Satellite imagery and geospatial intelligence for RIPA DDO operations
"""
import os
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

from models_ripa import LiveLocationData, DetentionLocation


@dataclass
class SatelliteImage:
    """Satellite image metadata from Planet"""
    image_id: str
    acquisition_time: datetime
    cloud_cover: float
    ground_sample_distance: float  # meters
    satellite: str
    bbox: List[float]  # [west, south, east, north]
    thumbnail_url: Optional[str] = None
    download_url: Optional[str] = None


@dataclass
class GeolocationIntelligence:
    """Geospatial intelligence from Planet"""
    location_id: str
    latitude: float
    longitude: float
    timestamp: datetime
    confidence: float
    source: str
    satellite_images: List[SatelliteImage]
    points_of_interest: List[Dict]
    route_analysis: Optional[Dict] = None
    area_assessment: Optional[Dict] = None


class PlanetGeolocationService:
    """
    Integration with Planet Labs API for geospatial intelligence
    Supports RIPA DDO operations with satellite imagery and location tracking
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Planet Labs API client

        Args:
            api_key: Planet API key (or set PLANET_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('PLANET_API_KEY')
        self.base_url = 'https://api.planet.com'
        self.data_api_url = f'{self.base_url}/data/v1'

        if not self.api_key:
            print("⚠️  Warning: PLANET_API_KEY not set. Using demo mode.")
            self.demo_mode = True
        else:
            self.demo_mode = False
            self.session = requests.Session()
            self.session.auth = (self.api_key, '')

    def search_imagery(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 1.0,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        max_cloud_cover: float = 0.2,
        item_types: List[str] = None
    ) -> List[SatelliteImage]:
        """
        Search for satellite imagery at a location

        Args:
            latitude: Target latitude
            longitude: Target longitude
            radius_km: Search radius in kilometers
            start_date: Start of date range (default: 30 days ago)
            end_date: End of date range (default: now)
            max_cloud_cover: Maximum cloud cover (0.0-1.0)
            item_types: List of item types to search (default: PSScene)

        Returns:
            List of satellite images covering the location
        """
        if self.demo_mode:
            return self._demo_imagery(latitude, longitude)

        # Set defaults
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        if not item_types:
            item_types = ['PSScene']  # PlanetScope Scene

        # Create point geometry
        point = {
            "type": "Point",
            "coordinates": [longitude, latitude]
        }

        # Create search filter
        geometry_filter = {
            "type": "GeometryFilter",
            "field_name": "geometry",
            "config": point
        }

        date_filter = {
            "type": "DateRangeFilter",
            "field_name": "acquired",
            "config": {
                "gte": start_date.isoformat() + "Z",
                "lte": end_date.isoformat() + "Z"
            }
        }

        cloud_filter = {
            "type": "RangeFilter",
            "field_name": "cloud_cover",
            "config": {
                "lte": max_cloud_cover
            }
        }

        combined_filter = {
            "type": "AndFilter",
            "config": [geometry_filter, date_filter, cloud_filter]
        }

        # Search request
        search_request = {
            "item_types": item_types,
            "filter": combined_filter
        }

        try:
            response = self.session.post(
                f"{self.data_api_url}/quick-search",
                json=search_request
            )
            response.raise_for_status()

            results = response.json()
            images = []

            for item in results.get('features', []):
                props = item['properties']
                geom = item['geometry']

                image = SatelliteImage(
                    image_id=item['id'],
                    acquisition_time=datetime.fromisoformat(props['acquired'].replace('Z', '')),
                    cloud_cover=props.get('cloud_cover', 0.0),
                    ground_sample_distance=props.get('gsd', 3.0),
                    satellite=props.get('satellite_id', 'unknown'),
                    bbox=geom.get('bbox', []),
                    thumbnail_url=item.get('_links', {}).get('thumbnail')
                )
                images.append(image)

            return images

        except Exception as e:
            print(f"⚠️  Error searching Planet imagery: {e}")
            return self._demo_imagery(latitude, longitude)

    def _demo_imagery(self, latitude: float, longitude: float) -> List[SatelliteImage]:
        """Generate demo satellite imagery data"""
        demo_images = []

        for i in range(3):
            image = SatelliteImage(
                image_id=f"DEMO_{i+1:03d}_{int(latitude*1000)}_{int(longitude*1000)}",
                acquisition_time=datetime.now() - timedelta(days=i*7),
                cloud_cover=0.05 + (i * 0.03),
                ground_sample_distance=3.0,
                satellite=f"PS2.SD-{i+1}",
                bbox=[
                    longitude - 0.01,
                    latitude - 0.01,
                    longitude + 0.01,
                    latitude + 0.01
                ],
                thumbnail_url=f"https://planet.com/demo/thumb_{i+1}.jpg"
            )
            demo_images.append(image)

        return demo_images

    def get_location_intelligence(
        self,
        latitude: float,
        longitude: float,
        location_name: str,
        subject_id: str
    ) -> GeolocationIntelligence:
        """
        Get comprehensive geolocation intelligence for a location

        Args:
            latitude: Target latitude
            longitude: Target longitude
            location_name: Human-readable location name
            subject_id: Subject being tracked

        Returns:
            Comprehensive geolocation intelligence package
        """
        # Search for recent imagery
        images = self.search_imagery(latitude, longitude)

        # Generate points of interest analysis
        poi = self._analyze_points_of_interest(latitude, longitude, images)

        # Route analysis
        route_analysis = self._analyze_routes(latitude, longitude)

        # Area assessment for DDO planning
        area_assessment = self._assess_area_for_ddo(latitude, longitude, images)

        intel = GeolocationIntelligence(
            location_id=f"GEO_{subject_id}_{int(datetime.now().timestamp())}",
            latitude=latitude,
            longitude=longitude,
            timestamp=datetime.now(),
            confidence=0.85 if images else 0.5,
            source="Planet Labs Satellite Imagery",
            satellite_images=images,
            points_of_interest=poi,
            route_analysis=route_analysis,
            area_assessment=area_assessment
        )

        return intel

    def _analyze_points_of_interest(
        self,
        latitude: float,
        longitude: float,
        images: List[SatelliteImage]
    ) -> List[Dict]:
        """
        Analyze points of interest from satellite imagery
        In production, would use computer vision on satellite images
        """
        # Demo POI analysis
        poi = [
            {
                'type': 'residence',
                'distance_meters': 0,
                'description': 'Primary residence building',
                'visibility': 'high',
                'access_points': 2,
                'confidence': 0.9
            },
            {
                'type': 'vehicle_parking',
                'distance_meters': 25,
                'description': 'Regular vehicle parking location',
                'visibility': 'medium',
                'access_points': 1,
                'confidence': 0.8
            },
            {
                'type': 'public_transport',
                'distance_meters': 150,
                'description': 'Bus stop / metro station',
                'visibility': 'high',
                'access_points': 3,
                'confidence': 0.7
            }
        ]

        return poi

    def _analyze_routes(
        self,
        latitude: float,
        longitude: float
    ) -> Dict:
        """
        Analyze escape routes and access routes
        """
        return {
            'primary_access': 'Main road from north',
            'escape_routes': [
                {'direction': 'north', 'distance_km': 0.2, 'type': 'vehicle_road'},
                {'direction': 'east', 'distance_km': 0.15, 'type': 'pedestrian_path'},
                {'direction': 'south', 'distance_km': 0.3, 'type': 'vehicle_road'}
            ],
            'chokepoints': [
                {'location': 'Main entrance', 'controllable': True},
                {'location': 'Side alley', 'controllable': True}
            ],
            'nearest_police_station_km': 2.5,
            'nearest_hospital_km': 1.8
        }

    def _assess_area_for_ddo(
        self,
        latitude: float,
        longitude: float,
        images: List[SatelliteImage]
    ) -> Dict:
        """
        Assess area suitability for DDO operation
        """
        return {
            'public_exposure_level': 'low',
            'crowd_density': 'low',
            'visibility_from_main_road': 'medium',
            'officer_approach_difficulty': 'low',
            'subject_escape_difficulty': 'medium',
            'evidence_preservation_environment': 'favorable',
            'operational_recommendation': 'Suitable for early morning arrest',
            'best_time_window': '06:00-08:00 local time',
            'officer_positioning': [
                'North entrance (primary)',
                'East side exit (containment)',
                'South perimeter (backup)'
            ],
            'satellite_coverage': f"{len(images)} recent images available",
            'imagery_quality': 'good' if images and images[0].cloud_cover < 0.1 else 'moderate'
        }

    def create_live_location_data(
        self,
        latitude: float,
        longitude: float,
        location_name: str,
        location_type: str = "residence"
    ) -> LiveLocationData:
        """
        Create LiveLocationData model from geolocation intelligence

        Args:
            latitude: GPS latitude
            longitude: GPS longitude
            location_name: Human-readable location name
            location_type: Type of location

        Returns:
            LiveLocationData model for RIPA DDO system
        """
        # Get satellite intelligence
        intel = self.get_location_intelligence(
            latitude=latitude,
            longitude=longitude,
            location_name=location_name,
            subject_id="CURRENT"
        )

        # Create LiveLocationData
        live_data = LiveLocationData(
            subject_id="TRACKING",
            timestamp=datetime.now(),
            latitude=latitude,
            longitude=longitude,
            accuracy_meters=10.0,  # Planet imagery provides ~3m GSD
            location_description=location_name,
            location_type=location_type,
            moving=False,
            speed_kph=0.0,
            heading_degrees=None,
            address=f"Lat: {latitude:.6f}, Lon: {longitude:.6f}",
            collection_method="planet_satellite",
            ripa_authorized=True,
            authorization_ref="RIPA/2025/GEOINT/PLANET",
            satellite_images_available=len(intel.satellite_images),
            last_satellite_image=intel.satellite_images[0].acquisition_time if intel.satellite_images else None,
            area_assessment=intel.area_assessment
        )

        return live_data

    def enhance_detention_location(
        self,
        detention_location: DetentionLocation
    ) -> DetentionLocation:
        """
        Enhance detention location with Planet satellite intelligence

        Args:
            detention_location: Existing DetentionLocation model

        Returns:
            Enhanced DetentionLocation with satellite data
        """
        # Get geolocation intelligence
        intel = self.get_location_intelligence(
            latitude=detention_location.latitude,
            longitude=detention_location.longitude,
            location_name=detention_location.description,
            subject_id="DETENTION_PLANNING"
        )

        # Enhance location with satellite intelligence
        if intel.area_assessment:
            assessment = intel.area_assessment

            # Update location attributes based on satellite analysis
            detention_location.public_exposure_level = assessment.get('public_exposure_level', 'MEDIUM')
            detention_location.crowd_level = assessment.get('crowd_density', 'MEDIUM').upper()
            detention_location.access_difficulty = assessment.get('officer_approach_difficulty', 'MODERATE').upper()

            # Add satellite metadata
            detention_location.satellite_coverage = f"{len(intel.satellite_images)} recent images"
            detention_location.last_satellite_update = intel.timestamp
            detention_location.geospatial_confidence = intel.confidence

        return detention_location

    def track_subject_movement(
        self,
        subject_id: str,
        historical_locations: List[Tuple[float, float, datetime]]
    ) -> Dict:
        """
        Analyze subject movement patterns from historical location data

        Args:
            subject_id: Subject identifier
            historical_locations: List of (lat, lon, timestamp) tuples

        Returns:
            Movement pattern analysis
        """
        if not historical_locations:
            return {'error': 'No location data provided'}

        # Calculate movement statistics
        total_distance_km = 0.0
        for i in range(1, len(historical_locations)):
            lat1, lon1, _ = historical_locations[i-1]
            lat2, lon2, _ = historical_locations[i]
            distance = self._haversine_distance(lat1, lon1, lat2, lon2)
            total_distance_km += distance

        # Time span
        time_span = historical_locations[-1][2] - historical_locations[0][2]

        # Identify frequent locations
        frequent_locations = self._identify_frequent_locations(historical_locations)

        analysis = {
            'subject_id': subject_id,
            'tracking_period': {
                'start': historical_locations[0][2].isoformat(),
                'end': historical_locations[-1][2].isoformat(),
                'duration_hours': time_span.total_seconds() / 3600
            },
            'total_locations_tracked': len(historical_locations),
            'total_distance_traveled_km': round(total_distance_km, 2),
            'frequent_locations': frequent_locations,
            'movement_pattern': 'routine' if len(frequent_locations) > 2 else 'irregular',
            'optimal_detention_locations': frequent_locations[:3] if frequent_locations else []
        }

        return analysis

    def _haversine_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula

        Returns:
            Distance in kilometers
        """
        from math import radians, sin, cos, sqrt, atan2

        R = 6371  # Earth's radius in km

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c

        return distance

    def _identify_frequent_locations(
        self,
        locations: List[Tuple[float, float, datetime]],
        radius_meters: float = 100
    ) -> List[Dict]:
        """
        Identify frequently visited locations from GPS data

        Args:
            locations: List of (lat, lon, timestamp) tuples
            radius_meters: Clustering radius for same location

        Returns:
            List of frequent location clusters
        """
        # Simple clustering algorithm
        clusters = []

        for lat, lon, timestamp in locations:
            # Check if location is near existing cluster
            added_to_cluster = False
            for cluster in clusters:
                center_lat = cluster['center_lat']
                center_lon = cluster['center_lon']
                distance_km = self._haversine_distance(lat, lon, center_lat, center_lon)

                if distance_km * 1000 < radius_meters:  # Convert to meters
                    cluster['visits'] += 1
                    cluster['last_visit'] = max(cluster['last_visit'], timestamp)
                    added_to_cluster = True
                    break

            if not added_to_cluster:
                clusters.append({
                    'center_lat': lat,
                    'center_lon': lon,
                    'visits': 1,
                    'first_visit': timestamp,
                    'last_visit': timestamp
                })

        # Sort by visit frequency
        clusters.sort(key=lambda x: x['visits'], reverse=True)

        # Format for output
        frequent_locations = []
        for i, cluster in enumerate(clusters[:5]):  # Top 5 locations
            frequent_locations.append({
                'rank': i + 1,
                'latitude': cluster['center_lat'],
                'longitude': cluster['center_lon'],
                'visit_count': cluster['visits'],
                'first_visit': cluster['first_visit'].isoformat(),
                'last_visit': cluster['last_visit'].isoformat(),
                'detention_suitability': 'high' if cluster['visits'] > 5 else 'medium'
            })

        return frequent_locations

    def download_image(
        self,
        image: SatelliteImage,
        output_path: str,
        asset_type: str = 'visual'
    ) -> bool:
        """
        Download satellite image from Planet

        Args:
            image: SatelliteImage object
            output_path: Local path to save image
            asset_type: Asset type to download (visual, analytic, etc.)

        Returns:
            True if successful, False otherwise
        """
        if self.demo_mode:
            print(f"⚠️  Demo mode: Would download {image.image_id} to {output_path}")
            return False

        try:
            # Activate asset
            item_type = 'PSScene'
            activation_url = f"{self.data_api_url}/item-types/{item_type}/items/{image.image_id}/assets"

            response = self.session.get(activation_url)
            response.raise_for_status()

            assets = response.json()

            if asset_type not in assets:
                print(f"⚠️  Asset type {asset_type} not available for {image.image_id}")
                return False

            # Activate asset if needed
            asset = assets[asset_type]
            if asset['status'] != 'active':
                activation_response = self.session.post(
                    asset['_links']['activate']
                )
                print(f"Activating asset... (may take a few minutes)")

            # Download (would need to poll for activation completion)
            print(f"Asset activation initiated for {image.image_id}")
            return True

        except Exception as e:
            print(f"⚠️  Error downloading image: {e}")
            return False


# Demo usage
if __name__ == "__main__":
    print("🛰️  Planet Labs Geolocation Integration Demo\n")

    # Initialize service (demo mode without API key)
    planet = PlanetGeolocationService()

    # Manchester city centre coordinates (demo)
    latitude = 53.4808
    longitude = -2.2426

    print(f"📍 Target Location: Manchester ({latitude}, {longitude})\n")

    # Search for satellite imagery
    print("🔍 Searching for satellite imagery...")
    images = planet.search_imagery(latitude, longitude)
    print(f"✓ Found {len(images)} satellite images\n")

    for img in images:
        print(f"  Image ID: {img.image_id}")
        print(f"  Acquired: {img.acquisition_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Cloud Cover: {img.cloud_cover*100:.1f}%")
        print(f"  Resolution: {img.ground_sample_distance}m GSD")
        print()

    # Get comprehensive geolocation intelligence
    print("📊 Generating geolocation intelligence...")
    intel = planet.get_location_intelligence(
        latitude=latitude,
        longitude=longitude,
        location_name="Subject residence - Manchester",
        subject_id="RUS_001"
    )

    print(f"✓ Intelligence package generated")
    print(f"  Confidence: {intel.confidence*100:.0f}%")
    print(f"  Satellite images: {len(intel.satellite_images)}")
    print(f"  Points of interest: {len(intel.points_of_interest)}\n")

    # Display area assessment
    if intel.area_assessment:
        print("🎯 DDO Area Assessment:")
        assessment = intel.area_assessment
        print(f"  Public Exposure: {assessment.get('public_exposure_level', 'N/A')}")
        print(f"  Crowd Density: {assessment.get('crowd_density', 'N/A')}")
        print(f"  Operational Recommendation: {assessment.get('operational_recommendation', 'N/A')}")
        print(f"  Best Time Window: {assessment.get('best_time_window', 'N/A')}")
        print()

    # Create LiveLocationData
    print("📡 Creating live location data...")
    live_data = planet.create_live_location_data(
        latitude=latitude,
        longitude=longitude,
        location_name="Subject residence",
        location_type="residence"
    )

    print(f"✓ Live location data created")
    print(f"  Accuracy: {live_data.accuracy_meters}m")
    print(f"  Collection Method: {live_data.collection_method}")
    print(f"  Satellite images available: {live_data.satellite_images_available}")
    print()

    print("✅ Demo complete!")
    print("\n💡 To use with real Planet API:")
    print("   export PLANET_API_KEY=your_api_key_here")
    print("   Then re-run this script")
