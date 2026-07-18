import requests
import time
from datetime import datetime

def bank_locator(user_location: str) -> list:
    """Find nearby banks and ATMs using OpenStreetMap APIs"""
    try:
        time.sleep(1) 
        print(f"Geocoding: {user_location}")
        
        # Step 1: Convert location to coordinates using Nominatim
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": user_location, 
            "format": "jsonv2", 
            "addressdetails": 1, 
            "limit": 1
        }
        headers = {"User-Agent": "MBankLocator/1.0"}
        
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Nominatim error: Status {response.status_code} - {response.text}")
            return [{"error": f"Location service error: {response.status_code}"}]
            
        data = response.json()
        if not data:
            print("Geocoding failed: No results")
            return [{"error": "Location not found. Please try a different location."}]
            
        lat, lng = float(data[0]["lat"]), float(data[0]["lon"])
        print(f"Coordinates: lat={lat}, lon={lng}")
        
        # Step 2: Find banks/ATMs using Overpass API
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        node["amenity"~"bank|atm"](around:5000,{lat},{lng});
        out body;
        """
        
        response = requests.post(overpass_url, data=overpass_query, headers=headers)
        if response.status_code != 200:
            print(f"Overpass error: Status {response.status_code}")
            return [{"error": "Bank and ATM search failed"}]
            
        data = response.json()
        banks = []
        
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            bank = {
                "name": tags.get("name", "Unnamed Facility"),
                "type": tags.get("amenity"),
                "lat": element.get("lat"),
                "lon": element.get("lon"),
                "address": ", ".join([
                    tags.get("addr:housenumber", ""),
                    tags.get("addr:street", ""),
                    tags.get("addr:city", "")
                ]).strip(", ")
            }
            banks.append(bank)
        
        
        banks = sorted(banks, key=lambda x: 
            (x["lat"] - lat)**2 + (x["lon"] - lng)**2)[:10]
        
        if not banks:
            return [{"error": "No banks or ATMs found in this area"}]
            
        print(f"Found {len(banks)} banks/ATMs")
        return banks
        
    except Exception as e:
        print(f"Locator error: {str(e)}")
        return [{"error": f"Failed to locate facilities: {str(e)}"}]

if __name__ == "__main__":
    location = "1600 Amphitheatre Parkway, Mountain View, CA"
    results = bank_locator(location)
    for result in results:
        print(result)