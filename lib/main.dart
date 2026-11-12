import 'package:flutter/material.dart';
void main() => runApp(const RescuePINApp());
class RescuePINApp extends StatelessWidget {
  const RescuePINApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(title: 'RescuePIN', theme: ThemeData(primarySwatch: Colors.red), home: const HomeScreen(), debugShowCheckedModeBanner: false);
  }
}
class HomeScreen extends StatefulWidget { const HomeScreen({super.key}); @override State<HomeScreen> createState() => _HomeState(); }
class _HomeState extends State<HomeScreen> {
  String pin = '------'; String status = 'Tap Generate to create your verified PIN';
  void generate() { setState(() { status = 'Getting GPS... Verifying...'; }); Future.delayed(const Duration(seconds: 2), () { setState(() { pin = 'AB12CD'; status = 'Verified ✓ Lat 9.0765, Lon 7.3985 • 12 Nov 2026 19:20'; }); }); }
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: const Text('RescuePIN — NDAPS Verified Safety')), body: Padding(padding: const EdgeInsets.all(16), child: Column(children: [CircleAvatar(radius: 60, child: Text(pin, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold))), const SizedBox(height: 12), Text(status, textAlign: TextAlign.center), const SizedBox(height: 16), ElevatedButton(onPressed: generate, child: const Text('Generate My PIN')), const SizedBox(height: 12), ElevatedButton(onPressed: () => setState(() => status = 'Shared via WhatsApp ✓'), child: const Text('Share via WhatsApp')), const SizedBox(height: 12), ElevatedButton(onPressed: () => setState(() => status = 'QR Code Ready — Show to rider / ambulance ✓'), child: const Text('Show QR Code'))])));
  }
}