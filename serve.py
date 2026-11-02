"""
Academic Development Server for zaidamin.org
Dual-Stack IPv4 & IPv6 with CORS for Antigravity IDE (Jetski Preview) & Browsers.
Includes CMS API Endpoints:
- POST /api/save-article (Save/update article & rebuild site)
- POST /api/delete-article?id=<slug> (Delete article & rebuild site)
- POST /api/deploy (Trigger GitHub live deployment)
"""

import http.server
import socket
import socketserver
import os
import sys
import json
import urllib.parse
import subprocess
import threading
from pathlib import Path

PORT = 8000
ROOT_DIR = Path(__file__).resolve().parent
DIRECTORY = ROOT_DIR / "dist"

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
            print(" [CMS Engine] Deployment completed.")
        except Exception as e:
            print(f" [CMS Engine Error] Deploy failed: {e}")
    threading.Thread(target=_run, daemon=True).start()

class AcademicPreviewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        # Enable CORS and iframe embedding for Antigravity IDE webviews (Jetski / Simple Browser)
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

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. Save Article Endpoint
        if path == "/api/save-article":
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                payload = json.loads(body.decode('utf-8'))
                
                article = payload.get('article', {})
                should_deploy = payload.get('deploy', False)

                if not article.get('id') or not article.get('title'):
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Missing id or title"}).encode('utf-8'))
                    return

                # Load existing articles
                articles_path = ROOT_DIR / "data" / "articles.json"
                if articles_path.exists():
                    with open(articles_path, 'r', encoding='utf-8') as f:
                        articles = json.load(f)
                else:
                    articles = []

                # Upsert article
                existing_idx = next((i for i, a in enumerate(articles) if a.get('id') == article.get('id')), None)
                if existing_idx is not None:
                    articles[existing_idx] = article
                else:
                    articles.insert(0, article)

                # Save to data/articles.json and dist/data/articles.json
                articles_path.parent.mkdir(parents=True, exist_ok=True)
                with open(articles_path, 'w', encoding='utf-8') as f:
                    json.dump(articles, f, indent=2, ensure_ascii=False)

                dist_art_path = DIRECTORY / "data" / "articles.json"
                dist_art_path.parent.mkdir(parents=True, exist_ok=True)
                with open(dist_art_path, 'w', encoding='utf-8') as f:
                    json.dump(articles, f, indent=2, ensure_ascii=False)

                # Rebuild site
                rebuild_site()

                # Deploy if requested
                if should_deploy:
                    deploy_live()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok",
                    "message": "Article saved and site rebuilt successfully",
                    "deploying": should_deploy,
                    "id": article.get('id')
                }).encode('utf-8'))
                return

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

        # 2. Delete Article Endpoint
        elif path == "/api/delete-article":
            try:
                params = urllib.parse.parse_qs(parsed.query)
                slug = params.get('id', [None])[0]

                if not slug:
                    content_len = int(self.headers.get('Content-Length', 0))
                    if content_len > 0:
                        body = self.rfile.read(content_len)
                        payload = json.loads(body.decode('utf-8'))
                        slug = payload.get('id')

                if not slug:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Missing article id"}).encode('utf-8'))
                    return

                articles_path = ROOT_DIR / "data" / "articles.json"
                if articles_path.exists():
                    with open(articles_path, 'r', encoding='utf-8') as f:
                        articles = json.load(f)
                    
                    articles = [a for a in articles if a.get('id') != slug]

                    with open(articles_path, 'w', encoding='utf-8') as f:
                        json.dump(articles, f, indent=2, ensure_ascii=False)

                    dist_art_path = DIRECTORY / "data" / "articles.json"
                    dist_art_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(dist_art_path, 'w', encoding='utf-8') as f:
                        json.dump(articles, f, indent=2, ensure_ascii=False)

                    rebuild_site()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "message": f"Article '{slug}' deleted"}).encode('utf-8'))
                return

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

        # 3. Deploy Live Site Endpoint
        elif path == "/api/deploy":
            try:
                deploy_live()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "message": "Deployment initiated"}).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode('utf-8'))

class DualStackServer(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6

    def server_bind(self):
        # Allow IPv4 and IPv6 on same socket
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

def run():
    with DualStackServer(("::", PORT), AcademicPreviewHandler) as httpd:
        print("=" * 60)
        print(f" Academic Server Active (Dual-Stack IPv4 + IPv6):")
        print(f" - http://127.0.0.1:{PORT}")
        print(f" - http://localhost:{PORT}")
        print(f" Serving Root: {DIRECTORY}")
        print(f" CMS API Enabled: /api/save-article, /api/delete-article, /api/deploy")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run()
