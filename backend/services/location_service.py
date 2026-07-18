import requests
import time
from typing import List, Dict, Optional
import traceback


class LocationService:
    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.overpass_url = "https://overpass-api.de/api/interpreter"
        self.headers = {"User-Agent": "BankingChatbot/1.0"}
        print("✓ LocationService initialized")
    
    def geocode_location(self, location: str) -> Optional[Dict]:
        """Convert location string to coordinates"""
        try:
            print(f"[GEOCODE] Searching for: {location}")
            time.sleep(1)  # Rate limiting for Nominatim
            
            params = {
                "q": location,
                "format": "jsonv2",
                "addressdetails": 1,
                "limit": 1
            }
            
            response = requests.get(
                self.nominatim_url, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            
            print(f"[GEOCODE] Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"[GEOCODE] Error: Status {response.status_code}")
                print(f"[GEOCODE] Response: {response.text[:200]}")
                return None
            
            data = response.json()
            print(f"[GEOCODE] Results found: {len(data)}")
            
            if not data:
                print("[GEOCODE] No results found")
                return None
            
            result = {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"]),
                "display_name": data[0].get("display_name", location)
            }
            
            print(f"[GEOCODE] Success: lat={result['lat']}, lon={result['lon']}")
            return result
            
        except requests.exceptions.Timeout:
            print("[GEOCODE] Request timeout")
            return None
        except requests.exceptions.RequestException as e:
            print(f"[GEOCODE] Request error: {e}")
            return None
        except Exception as e:
            print(f"[GEOCODE] Unexpected error: {e}")
            traceback.print_exc()
            return None
    
    def find_banks_atms(self, lat: float, lon: float, radius: int = 5000, limit: int = 10) -> List[Dict]:
        """Find banks and ATMs near coordinates"""
        try:
            print(f"[BANKS] Searching near lat={lat}, lon={lon}, radius={radius}m")
            
            overpass_query = f"""
            [out:json][timeout:25];
            (
              node["amenity"="bank"](around:{radius},{lat},{lon});
              node["amenity"="atm"](around:{radius},{lat},{lon});
            );
            out body;
            """
            
            response = requests.post(
                self.overpass_url,
                data=overpass_query,
                headers=self.headers,
                timeout=30
            )
            
            print(f"[BANKS] Overpass status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"[BANKS] Overpass error: {response.status_code}")
                print(f"[BANKS] Response: {response.text[:200]}")
                return []
            
            data = response.json()
            elements = data.get("elements", [])
            print(f"[BANKS] Found {len(elements)} elements")
            
            banks = []
            
            for element in elements:
                tags = element.get("tags", {})
                element_lat = element.get("lat")
                element_lon = element.get("lon")
                
                if not element_lat or not element_lon:
                    continue
                
                # Calculate distance
                distance = self._calculate_distance(lat, lon, element_lat, element_lon)
                
                bank = {
                    "name": tags.get("name", "Unnamed Facility"),
                    "type": tags.get("amenity", "unknown").upper(),
                    "brand": tags.get("brand", ""),
                    "lat": element_lat,
                    "lon": element_lon,
                    "distance_km": round(distance, 2),
                    "address": self._format_address(tags),
                    "phone": tags.get("phone", ""),
                    "opening_hours": tags.get("opening_hours", "")
                }
                banks.append(bank)
            
            # Sort by distance
            banks.sort(key=lambda x: x["distance_km"])
            
            result = banks[:limit]
            print(f"[BANKS] Returning {len(result)} results")
            
            return result
            
        except requests.exceptions.Timeout:
            print("[BANKS] Request timeout")
            return []
        except requests.exceptions.RequestException as e:
            print(f"[BANKS] Request error: {e}")
            return []
        except Exception as e:
            print(f"[BANKS] Unexpected error: {e}")
            traceback.print_exc()
            return []
    
    def _format_address(self, tags: Dict) -> str:
        """Format address from OSM tags"""
        parts = [
            tags.get("addr:housenumber", ""),
            tags.get("addr:street", ""),
            tags.get("addr:suburb", ""),
            tags.get("addr:city", ""),
            tags.get("addr:state", ""),
            tags.get("addr:postcode", "")
        ]
        
        # Filter out empty parts and join
        address_parts = [p.strip() for p in parts if p and p.strip()]
        
        if not address_parts:
            return "Address not available"
        
        return ", ".join(address_parts)
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance in kilometers using Haversine formula"""
        try:
            from math import radians, sin, cos, sqrt, atan2
            
            R = 6371  # Earth's radius in km
            
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            
            distance = R * c
            
            return distance
            
        except Exception as e:
            print(f"[DISTANCE] Calculation error: {e}")
            return 0.0
    
    def search_by_location(self, location: str, limit: int = 10) -> Dict:
        """Main method: Search banks/ATMs by location string"""
        try:
            print(f"[SEARCH] Starting search for: {location}")
            
            if not location or not location.strip():
                return {
                    "success": False,
                    "error": "Location cannot be empty",
                    "results": []
                }
            
            # Geocode location
            coords = self.geocode_location(location.strip())
            
            if not coords:
                return {
                    "success": False,
                    "error": "Location not found. Please try a different location or be more specific.",
                    "results": []
                }
            
            print(f"[SEARCH] Geocoding successful, searching for banks...")
            
            # Find banks/ATMs
            banks = self.find_banks_atms(coords["lat"], coords["lon"], limit=limit)
            
            if not banks:
                return {
                    "success": True,
                    "error": "No banks or ATMs found within 5km of this location. Try a different area.",
                    "results": [],
                    "location": coords["display_name"],
                    "coordinates": {"lat": coords["lat"], "lon": coords["lon"]},
                    "count": 0
                }
            
            print(f"[SEARCH] Search complete: {len(banks)} results")
            
            return {
                "success": True,
                "location": coords["display_name"],
                "coordinates": {"lat": coords["lat"], "lon": coords["lon"]},
                "results": banks,
                "count": len(banks)
            }
            
        except Exception as e:
            print(f"[SEARCH] Error: {e}")
            traceback.print_exc()
            return {
                "success": False,
                "error": f"Search failed: {str(e)}",
                "results": []
            }


# Test function
if __name__ == "__main__":
    service = LocationService()
    
    # Test locations
    test_locations = [
        "Mumbai, India",
        "Bangalore, MG Road",
        "Delhi, Connaught Place"
    ]
    
    for location in test_locations:
        print("\n" + "="*60)
        print(f"Testing: {location}")
        print("="*60)
        
        result = service.search_by_location(location, limit=20)
        
        if result['success']:
            print(f"✓ Found {result['count']} results")
            for idx, bank in enumerate(result['results'][:3], 1):
                print(f"{idx}. {bank['name']} ({bank['type']}) - {bank['distance_km']} km")
        else:
            print(f"✗ Error: {result['error']}")
