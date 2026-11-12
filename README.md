# RescuePIN — NDAPS Verified Safety
### No Address? No Problem. Your PIN Finds You.

▶️ **Live Demo:** [Try RescuePIN Demo](https://github.[STRIPPED 76 bytes])

RescuePIN solves Nigeria's addressing problem: millions of homes, markets, farms and IDP camps have no formal address. RescuePIN gives every location a GPS-verified PIN + QR + USSD fallback — so ambulances, deliveries, enumerators and emergency teams can find you.

> Author: Abdulkadir Ahmed — FCT Abuja, Nigeria
> aabdulkadir222@gmail.com | +234 806 316 6737

## 🚨 Problem
- No formal address = ambulance can't find you, delivery fails, enumeration misses you
- Fake addresses, vague directions: "behind mosque, near big tree"
- Emergency response delayed by 30-90 mins in rural / informal areas

## ✅ What It Does
1. **GPS-Verified PIN** — Tap to generate 6-digit PIN + GPS coordinates, encrypted, tamper-proof
2. **QR Code** — Print / share QR, scan to navigate
3. **USSD Fallback** — Works without smartphone / data: dial code, get PIN by SMS
4. **Verified Location** — Photo + GPS + timestamp
5. **Share** — 【entity-WhatsApp¦canonical_name=WhatsApp】, SMS, Email: "My RescuePIN is AB12CD — Find me here"
6. **For Teams** — Enumerators, health workers, delivery riders verify location on arrival

## 📱 Screens
Home • Generate PIN • My PINs • Scan QR • Share • Verify • Emergency

## 🛠️ Tech Stack
- **App:** Flutter (Dart) — Android + iOS
- **Backend:** Firebase Auth, Firestore, Cloud Functions
- **Maps:** Google Maps / OpenStreetMap
- **GPS:** Geolocator, QR: qr_flutter
- **USSD/SMS:** Africa's Talking / Termii (Nigeria)
- **Encryption:** AES-256, SHA-256 hash

## 🔒 Privacy
- Only share PIN when you choose. PIN expires / can be revoked.
- No tracking without consent. NDPA compliant.

## 📂 Repo Structure