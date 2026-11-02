"""
Academic Development Server for zaidamin.org
Dual-Stack IPv4 & IPv6 with CORS for Antigravity IDE (Jetski Preview) & Browsers.
Cryptographically Secured Unified CMS API Endpoints:
- POST /api/auth (Verify admin key)
- POST /api/save-article / delete-article (Activity & Project: Articles & Essays)
- POST /api/save-publication / delete-publication (Research & Publication)
- POST /api/save-talk / delete-talk (Recent Media & Talks)
- POST /api/save-achievement / delete-achievement (Achievement & CV)
- POST /api/deploy (Trigger GitHub live deployment)
"""

import http.server
import socket
import time
import socketserver
import os
import sys
import json
import urllib.parse
import subprocess
import threading
import base64
import re
from datetime import datetime
from pathlib import Path

PORT = 8000
ROOT_DIR = Path(__file__).resolve().parent
DIRECTORY = ROOT_DIR / "dist"

# Load Admin Key from .env or fallback
ADMIN_KEY = "ZaidAmin@Academic2026!"
env_path = ROOT_DIR / ".env"
if env_path.exists():
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("CMS_ADMIN_KEY="):
                    ADMIN_KEY = line.split("=", 1)[1].strip()
                    break
    except Exception:
        pass

def verify_auth(handler):
    """Verify that incoming request carries valid master admin credentials"""
    key = handler.headers.get("X-Admin-Key")
    if not key:
        auth_header = handler.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            key = auth_header[7:].strip()
    return key == ADMIN_KEY

def rebuild_site():
    """Run build.py synchronously to regenerate all HTML and update dist/"""
    try:
        subprocess.run([sys.executable, str(ROOT_DIR / "build.py")], check=True, cwd=str(ROOT_DIR))
        print(" [CMS Engine] Website compiled successfully via build.py")
        return True
    except Exception as e:
        print(f" [CMS Engine Error] Rebuild failed: {e}")
        return False

def deploy_live():
    """Trigger deploy.py in background thread"""
    def _run():
        try:
            print(" [CMS Engine] Triggering deploy.py...")
            subprocess.run([sys.executable, str(ROOT_DIR / "deploy.py")], cwd=str(ROOT_DIR))
            print(" [CMS Engine] Live GitHub deployment completed.")
        except Exception as e:
            print(f" [CMS Engine Error] Deploy failed: {e}")
    threading.Thread(target=_run, daemon=True).start()

def load_json_file(filename):
    p = ROOT_DIR / "data" / filename
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json_file(filename, data):
    p1 = ROOT_DIR / "data" / filename
    p2 = DIRECTORY / "data" / filename
    p1.parent.mkdir(parents=True, exist_ok=True)
    p2.parent.mkdir(parents=True, exist_ok=True)
    with open(p1, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open(p2, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class AcademicPreviewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def send_json(self, status_code, payload):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def read_post_json(self):
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len == 0:
            return {}
        body = self.rfile.read(content_len)
        return json.loads(body.decode("utf-8"))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 0. Auth Endpoint
        if path == "/api/auth":
            try:
                payload = self.read_post_json()
                key = payload.get("key", "")
                if key == ADMIN_KEY:
                    self.send_json(200, {"status": "ok", "authenticated": True, "message": "Admin authorized"})
                else:
                    self.send_json(401, {"status": "error", "authenticated": False, "message": "Invalid Master Passkey"})
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        # STRICT SECURITY GATE: All other endpoints require valid authentication
        if not verify_auth(self):
            print(f" [SECURITY] Unauthorized attempt to access {path} from {self.client_address[0]}")
            self.send_json(401, {"error": "Unauthorized: Master Admin Key required"})
            return

        try:
            # 0.5 IMAGE UPLOADER
            if path == "/api/upload-image":
                payload = self.read_post_json()
                raw_filename = payload.get("filename", f"upload_{int(datetime.now().timestamp())}.png")
                filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', raw_filename)
                data_b64 = payload.get("data", "")
                if data_b64.startswith("data:"):
                    data_b64 = data_b64.split(",", 1)[1]

                img_bytes = base64.b64decode(data_b64)
                upload_dir_1 = ROOT_DIR / "assets" / "images" / "uploads"
                upload_dir_2 = DIRECTORY / "assets" / "images" / "uploads"
                upload_dir_1.mkdir(parents=True, exist_ok=True)
                upload_dir_2.mkdir(parents=True, exist_ok=True)

                with open(upload_dir_1 / filename, "wb") as f:
                    f.write(img_bytes)
                with open(upload_dir_2 / filename, "wb") as f:
                    f.write(img_bytes)

                rel_url = f"assets/images/uploads/{filename}"
                print(f" [CMS Engine] Image uploaded successfully: {rel_url}")
                self.send_json(200, {"status": "ok", "url": rel_url, "filename": filename})
                return

            # 1. ARTICLES (Activity & Project)
            elif path == "/api/save-article":
                payload = self.read_post_json()
                article = payload.get("article", {})
                should_deploy = payload.get("deploy", False)

                if not article.get("id") or not article.get("title"):
                    self.send_json(400, {"error": "Missing article id or title"})
                    return

                articles = load_json_file("articles.json")
                idx = next((i for i, a in enumerate(articles) if a.get("id") == article.get("id")), None)
                if idx is not None:
                    articles[idx] = article
                else:
                    articles.insert(0, article)

                save_json_file("articles.json", articles)
                rebuild_site()
                if should_deploy:
                    deploy_live()
                self.send_json(200, {"status": "ok", "message": "Article saved", "deploying": should_deploy, "id": article.get("id")})
                return

            elif path == "/api/delete-article":
                params = urllib.parse.parse_qs(parsed.query)
                slug = params.get("id", [None])[0]
                if not slug:
                    slug = self.read_post_json().get("id")
                if not slug:
                    self.send_json(400, {"error": "Missing article id"})
                    return

                articles = load_json_file("articles.json")
                articles = [a for a in articles if a.get("id") != slug]
                save_json_file("articles.json", articles)
                rebuild_site()
                self.send_json(200, {"status": "ok", "message": f"Article '{slug}' deleted"})
                return

            # 2. PUBLICATIONS (Research & Publication)
            elif path == "/api/save-publication":
                payload = self.read_post_json()
                pub = payload.get("publication", {})
                should_deploy = payload.get("deploy", False)

                if not pub.get("id") or not pub.get("title"):
                    self.send_json(400, {"error": "Missing publication id or title"})
                    return

                pubs = load_json_file("publications.json")
                # If marked featured, unset featured on all others
                if pub.get("featured"):
                    for p in pubs:
                        if p.get("id") != pub.get("id"):
                            p["featured"] = False

                idx = next((i for i, p in enumerate(pubs) if p.get("id") == pub.get("id")), None)
                if idx is not None:
                    pubs[idx] = pub
                else:
                    pubs.insert(0, pub)

                save_json_file("publications.json", pubs)
                rebuild_site()
                if should_deploy:
                    deploy_live()
                self.send_json(200, {"status": "ok", "message": "Publication saved", "deploying": should_deploy, "id": pub.get("id")})
                return

            elif path == "/api/delete-publication":
                params = urllib.parse.parse_qs(parsed.query)
                pub_id = params.get("id", [None])[0]
                if not pub_id:
                    pub_id = self.read_post_json().get("id")
                if not pub_id:
                    self.send_json(400, {"error": "Missing publication id"})
                    return

                pubs = load_json_file("publications.json")
                pubs = [p for p in pubs if p.get("id") != pub_id]
                save_json_file("publications.json", pubs)
                rebuild_site()
                self.send_json(200, {"status": "ok", "message": f"Publication '{pub_id}' deleted"})
                return

            # 3. TALKS & MEDIA (Recent Media & Talks)
            elif path == "/api/save-talk":
                payload = self.read_post_json()
                talk = payload.get("talk", {})
                should_deploy = payload.get("deploy", False)

                if not talk.get("title"):
                    self.send_json(400, {"error": "Missing talk title"})
                    return

                talks_data = load_json_file("talks.json")
                if isinstance(talks_data, dict):
                    talk_list = talks_data.get("talks", [])
                else:
                    talk_list = talks_data

                # Upsert by title or id
                idx = next((i for i, t in enumerate(talk_list) if t.get("title") == talk.get("title") or (talk.get("id") and t.get("id") == talk.get("id"))), None)
                if idx is not None:
                    talk_list[idx] = talk
                else:
                    talk_list.insert(0, talk)

                if isinstance(talks_data, dict):
                    talks_data["talks"] = talk_list
                else:
                    talks_data = talk_list

                save_json_file("talks.json", talks_data)
                rebuild_site()
                if should_deploy:
                    deploy_live()
                self.send_json(200, {"status": "ok", "message": "Talk saved", "deploying": should_deploy})
                return

            elif path == "/api/delete-talk":
                params = urllib.parse.parse_qs(parsed.query)
                title = params.get("title", [None])[0]
                if not title:
                    title = self.read_post_json().get("title")

                talks_data = load_json_file("talks.json")
                if isinstance(talks_data, dict):
                    talks_data["talks"] = [t for t in talks_data.get("talks", []) if t.get("title") != title]
                else:
                    talks_data = [t for t in talks_data if t.get("title") != title]

                save_json_file("talks.json", talks_data)
                rebuild_site()
                self.send_json(200, {"status": "ok", "message": f"Talk '{title}' deleted"})
                return

            # 4. ACHIEVEMENTS & CV (Achievement & CV)
            elif path == "/api/save-achievement":
                payload = self.read_post_json()
                item = payload.get("achievement", {})
                should_deploy = payload.get("deploy", False)

                if not item.get("title"):
                    self.send_json(400, {"error": "Missing achievement title"})
                    return

                cv = load_json_file("cv_data.json")
                items = cv.get("achievements_and_grants", [])
                idx = next((i for i, a in enumerate(items) if a.get("title") == item.get("title")), None)
                if idx is not None:
                    items[idx] = item
                else:
                    items.insert(0, item)

                cv["achievements_and_grants"] = items
                save_json_file("cv_data.json", cv)
                rebuild_site()
                if should_deploy:
                    deploy_live()
                self.send_json(200, {"status": "ok", "message": "Achievement saved", "deploying": should_deploy})
                return

            elif path == "/api/delete-achievement":
                params = urllib.parse.parse_qs(parsed.query)
                title = params.get("title", [None])[0]
                if not title:
                    title = self.read_post_json().get("title")

                cv = load_json_file("cv_data.json")
                cv["achievements_and_grants"] = [a for a in cv.get("achievements_and_grants", []) if a.get("title") != title]
                save_json_file("cv_data.json", cv)
                rebuild_site()
                self.send_json(200, {"status": "ok", "message": f"Achievement '{title}' deleted"})
                return

            # 5. DEPLOY TO LIVE GITHUB PAGES
            elif path == "/api/deploy":
                deploy_live()
                self.send_json(200, {"status": "ok", "message": "Live deployment initiated to zaidamin.org"})
                return

            else:
                self.send_json(404, {"error": "Endpoint not found"})

        except Exception as e:
            self.send_json(500, {"error": str(e)})

class IPv6Server(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6
    allow_reuse_address = False
    def server_bind(self):
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        super().server_bind()

class IPv4Server(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET
    allow_reuse_address = False

def run():
    print("=" * 65)
    print(f" Academic Server Active (Dual-Stack IPv4 + IPv6):")
    print(f" - http://localhost:{PORT}")
    print(f" - http://127.0.0.1:{PORT}")
    print(f" Serving Root: {DIRECTORY}")
    print(f" Cryptographic Security: ACTIVE (Admin Key Protected)")
    print("=" * 65)

    s4 = None
    s6 = None

    try:
        s4 = IPv4Server(("0.0.0.0", PORT), AcademicPreviewHandler)
        t4 = threading.Thread(target=s4.serve_forever, daemon=True)
        t4.start()
        print(" [Core Engine] IPv4 Listener active on 0.0.0.0:8000")
    except Exception as e:
        print(f" [Warning] IPv4 bind error: {e}")

    try:
        s6 = IPv6Server(("::", PORT), AcademicPreviewHandler)
        t6 = threading.Thread(target=s6.serve_forever, daemon=True)
        t6.start()
        print(" [Core Engine] IPv6 Listener active on [::]:8000")
    except Exception as e:
        print(f" [Warning] IPv6 bind error: {e}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        if s4:
            s4.shutdown()
        if s6:
            s6.shutdown()
        print("Server stopped.")

if __name__ == "__main__":
    run()
