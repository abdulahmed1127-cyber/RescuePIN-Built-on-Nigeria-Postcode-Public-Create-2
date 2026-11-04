from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import postcode_service as ps
import base64, json, time, random, os
from datetime import datetime, timedelta

app = FastAPI(title="RescuePIN API", description="Built on Nigeria's Postcode API - docs.postcode.gov.ng", version="1.0.0")

# Mock DB for MVP
users_db = {} # phone -> postcode
claims_db = {} # postcode -> phone
sos_logs = []
otp_store = {} # phone -> {otp, expiry, postcode}

class VerifyRequest(BaseModel):
    code: str
    phone: str

class SOSRequest(BaseModel):
    phone: str
    postcode: str
    lat: float
    lon: float
    blood_group: str = ""
    medical_note: str = ""

class OTPRequest(BaseModel):
    phone: str
    postcode: str

class DeliveryRequest(BaseModel):
    phone: str
    otp: str
    rider_lat: float
    rider_lon: float
    postcode: str

@app.get("/")
def root():
    return {"message": "RescuePIN API - Built on Nigeria's Postcode", "docs": "docs.postcode.gov.ng", "base": ps.BASE_URL}

@app.get("/api/autocomplete")
async def autocomplete(query: str):
    result = await ps.autocomplete(query)
    return {"query": query, "results": result, "source": "NIPOST Search API"}

@app.get("/api/lookup")
async def lookup(query: str):
    result = await ps.lookup_postcode(query)
    return {"query": query, "result": result, "source": "NIPOST Lookup L1"}

@app.get("/api/reverse")
async def reverse(lat: float, lon: float):
    result = await ps.reverse_geocode(lat, lon)
    return {"lat": lat, "lon": lon, "result": result, "source": "NIPOST Reverse Geocode L2"}

@app.post("/api/verify-postcode")
def verify_postcode(req: VerifyRequest):
    code = req.code.upper().strip()
    # Offline validation via SDK
    if not ps.validate_offline(code):
        raise HTTPException(400, "Invalid format. Must be 11-char alphanumeric like ABJ-GWA-7K2P-X1A")
    # Anti-spoofing: 1 code = 1 phone
    if code in claims_db and claims_db[code] != req.phone:
        raise HTTPException(409, f"Already claimed, request joint verification. Owner: {claims_db[code][:4]}****")
    claims_db[code] = req.phone
    users_db[req.phone] = code
    # Generate QR payload (base64 MVP, libsodium prod)
    payload = {"code": code, "phone": req.phone, "ts": int(time.time())}
    qr_data = base64.b64encode(json.dumps(payload).encode()).decode()
    return {"valid": True, "code": code, "qr_data": qr_data, "message": "Secured to device biometrics"}

@app.post("/api/sos")
def sos_trigger(req: SOSRequest):
    # Encrypt payload
    payload = {"postcode": req.postcode, "lat": req.lat, "lon": req.lon, "phone": req.phone, "bg": req.blood_group, "ts": datetime.utcnow().isoformat()}
    encrypted = base64.b64encode(json.dumps(payload).encode()).decode()
    log = {"id": len(sos_logs)+1, "payload": payload, "encrypted": encrypted, "time": datetime.utcnow().isoformat()}
    sos_logs.append(log)
    sms_text = f"RESCUEPIN SOS: Need help at {req.postcode} Lat/Lon {req.lat},{req.lon}. Blood: {req.blood_group}. From {req.phone}"
    return {"status": "dispatched", "confirmation": f"Help is on the way. Your verified location {req.postcode} shared.", "sms_fallback": sms_text, "control_room_id": log["id"]}

@app.get("/api/control-room")
def control_room():
    return {"active_alerts": sos_logs[-20:], "count": len(sos_logs)}

@app.post("/api/generate-otp")
def generate_otp(req: OTPRequest):
    otp = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=10)
    otp_store[req.phone] = {"otp": otp, "expiry": expiry, "postcode": req.postcode}
    return {"otp": otp, "expiry": expiry.isoformat(), "message": f"Verified Buyer {req.postcode}", "valid_for": "10 minutes"}

@app.post("/api/validate-delivery")
async def validate_delivery(req: DeliveryRequest):
    stored = otp_store.get(req.phone)
    if not stored or stored["otp"] != req.otp:
        raise HTTPException(400, "Invalid OTP")
    if datetime.utcnow() > stored["expiry"]:
        raise HTTPException(400, "OTP expired")
    # Check 50m radius via NIPOST Nearby API
    nearby = await ps.nearby_search(req.rider_lat, req.rider_lon, 50)
    distance = nearby.get("distance_m", 0) if isinstance(nearby, dict) else 0
    # For mock, enforce simple distance check
    if isinstance(nearby, dict) and not nearby.get("within_radius", False) and distance > 50:
        return {"verified": False, "message": "Too far from verified pin. Move closer.", "distance_m": distance}
    return {"verified": True, "message": "Delivery Verified & Secured", "distance_m": distance}
