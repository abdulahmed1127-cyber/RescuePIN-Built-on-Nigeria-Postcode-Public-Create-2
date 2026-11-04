# postcode_service.py - Built on Nigeria's Postcode API
# Docs: docs.postcode.gov.ng | Base: https://api.postcode.gov.ng
import httpx
import re
import os
from typing import Optional

BASE_URL = os.getenv("NIPOST_BASE_URL", "https://api.postcode.gov.ng")
API_KEY = os.getenv("NIPOST_API_KEY", "") 

POSTCODE_REGEX = re.compile(r"^[A-Z0-9]{3}-[A-Z0-9]{3}-[A-Z0-9]{4}-[A-Z0-9]{1}$|^[A-Z0-9]{11}$")

MOCK_ABUJA_DATA = {
    "gwarimpa": {"code": "ABJ-GWA-7K2P-X1A", "address": "House 12, 3rd Avenue, Gwarimpa, Abuja", "lat": 9.102, "lon": 7.421, "lga": "AMAC", "state": "FCT"},
    "lugbe": {"code": "ABJ-LUG-3M9A-B2C", "address": "Plot 45, FHA Lugbe, Abuja", "lat": 8.957, "lon": 7.354, "lga": "AMAC", "state": "FCT"},
    "wuse": {"code": "ABJ-WUS-9L1Q-Z8D", "address": "Wuse Zone 5, Abuja", "lat": 9.063, "lon": 7.462, "lga": "AMAC", "state": "FCT"},
    "maitama": {"code": "ABJ-MTA-4P6R-Y3E", "address": "Maitama District, Abuja", "lat": 9.082, "lon": 7.492, "lga": "AMAC", "state": "FCT"},
}

def validate_offline(code: str) -> bool:
    return bool(POSTCODE_REGEX.match(code.replace(" ", "").replace("-","").upper() if len(code.replace("-",""))==11 else code.upper()))

async def autocomplete(query: str):
    if not API_KEY:
        return [v for k,v in MOCK_ABUJA_DATA.items() if query.lower() in k or query.lower() in v["address"].lower()]
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/autocomplete", params={"query": query}, headers={"x-api-key": API_KEY}, timeout=10)
        resp.raise_for_status()
        return resp.json()

async def lookup_postcode(query: str):
    if not API_KEY:
        for k,v in MOCK_ABUJA_DATA.items():
            if query.lower() in k or query.lower() in v["address"].lower():
                return v
        return MOCK_ABUJA_DATA["gwarimpa"]
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/lookup", params={"query": query}, headers={"x-api-key": API_KEY}, timeout=10)
        resp.raise_for_status()
        return resp.json()

async def reverse_geocode(lat: float, lon: float):
    if not API_KEY:
        return MOCK_ABUJA_DATA["wuse"]
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/reverse", params={"lat": lat, "lon": lon}, headers={"x-api-key": API_KEY}, timeout=10)
        resp.raise_for_status()
        return resp.json()

async def nearby_search(lat: float, lon: float, radius_m: int = 50):
    if not API_KEY:
        return {"within_radius": True, "distance_m": 22, "mock": True}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/nearby", params={"lat": lat, "lon": lon, "radius": radius_m}, headers={"x-api-key": API_KEY}, timeout=10)
        resp.raise_for_status()
        return resp.json()
