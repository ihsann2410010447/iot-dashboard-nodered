# IoT Dashboard: Node-RED + MQTT + SQLite + WebSocket

Simulasi ESP32 mengirim suhu dan kelembaban lewat MQTT ke Node-RED. Node-RED menyimpan data ke SQLite, menyiarkan ke dashboard lewat WebSocket, dan menyediakan REST API yang dilindungi API key.

## Fitur tambahan
| Fitur | Implementasi |
|---|---|
| `PUT /api/threshold` + notifikasi | Batas disimpan di context file. Saat suhu melewati batas: pesan `alert` dikirim ke WebSocket (banner di dashboard) dan ke MQTT topic `iot/alert` (cooldown 30 detik). |
| Grafik real-time | Chart.js di `dashboard/index.html` (suhu, batas, kelembaban). |
| Autentikasi | Header `X-API-Key` dicek di semua endpoint `/api/*`. |
| WebSocket | Path `/ws`. Dashboard tidak polling; REST hanya dipakai sekali untuk data awal. |
| History di database | Tabel `readings` di SQLite (`iot.sqlite`), bukan flow context. |

## Instalasi
1. Palet Node-RED: instal `node-red-node-sqlite`.
2. Di `~/.node-red/settings.js` aktifkan CORS agar dashboard bisa memanggil API:
   httpNodeCors: {
       origin: "*",
       methods: "GET,PUT,POST,DELETE,OPTIONS",
       allowedHeaders: "Content-Type,X-API-Key"
   },
   - Batas suhu disimpan di memori Node-RED, sehingga kembali ke 30 °C saat Node-RED di-restart.
4. Jalankan Node-RED dengan API key: `API_KEY=rahasia123 node-red` (tanpa env, default `iot-secret-123`).
5. Hapus tab flow lama, lalu Import `flows.json` dan Deploy.
6. Samakan `API_KEY` di `dashboard/index.html` dengan key di langkah 3.
7. Jalankan broker MQTT (mosquitto), lalu `python simulator/simulasi_esp32.py`.
8. Buka `dashboard/index.html` di browser.

## Endpoint
| Method | Path | Keterangan |
|---|---|---|
| GET | `/api/suhu` | Data sensor terbaru |
| GET | `/api/history?n=50` | Data dari SQLite (maks 500) |
| POST | `/api/kontrol` | Body `{"device":"lamp","action":"on"}` |
| GET / PUT | `/api/threshold` | Body PUT `{"threshold":32}` |
| WS | `/ws` | Stream `sensor`, `alert`, `threshold` |

```bash
curl -X PUT http://localhost:1880/api/threshold -H "X-API-Key: iot-secret-123" -H "Content-Type: application/json" -d '{"threshold":28}'
curl http://localhost:1880/api/suhu            # 401 tanpa key
```

## Catatan
- WebSocket `/ws` tidak memakai API key (browser tidak bisa mengirim header kustom di WebSocket). Untuk produksi, tambahkan token lewat query string atau reverse proxy.
- API key di JavaScript dashboard terlihat oleh pengguna browser; cukup untuk tugas ini, bukan untuk produksi.
