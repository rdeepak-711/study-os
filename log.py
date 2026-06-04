#!/usr/bin/env python3
"""
Daily log server for study-os.

Run it:   python3 study-os/log.py
Then open http://localhost:8777 in your browser, type today's log, hit Save.
Python writes log/<today>.md, commits everything (including any DSA/DDIA files
you added), and pushes to GitHub. One submit = one green square.

Stdlib only. No pip installs.
"""
import http.server, socketserver, subprocess, urllib.parse, datetime, os, html, json

PORT = 8777
ROOT = os.path.dirname(os.path.abspath(__file__))   # study-os/
LOGDIR = os.path.join(ROOT, "log")

PAGE = """<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width, initial-scale=1">
<title>study-os · daily log</title><style>
:root{{--bg:#f6f5f2;--card:#fffdfa;--ink:#23211d;--ink2:#6b665d;--line:#e4e0d8;
--accent:#3a5a7d;--good:#3f7d54;--good-soft:#e6f0e8;--warn:#a8542a;--warn-soft:#f4e7df}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font:15px/1.55 -apple-system,system-ui,sans-serif;background:var(--bg);color:var(--ink);
max-width:680px;margin:0 auto;padding:32px 24px}}
h1{{font-size:1.4rem;letter-spacing:-.02em}}
.sub{{color:var(--ink2);font-size:.9rem;margin:4px 0 22px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px}}
label{{font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:var(--ink2);display:block;margin-bottom:7px}}
input,textarea{{font:inherit;width:100%;border:1px solid #d6d1c7;border-radius:8px;padding:10px;background:var(--bg);color:var(--ink)}}
textarea{{min-height:150px;resize:vertical}}
.row{{display:flex;gap:14px;align-items:flex-end;margin-top:14px}}
.row > div:first-child{{flex:1}}
button{{font:inherit;font-weight:600;background:var(--accent);color:#fff;border:none;border-radius:8px;padding:11px 22px;cursor:pointer;margin-top:16px}}
button:hover{{filter:brightness(1.08)}}
.msg{{border-radius:8px;padding:13px 15px;margin-bottom:18px;font-size:.92rem;white-space:pre-wrap}}
.ok{{background:var(--good-soft);color:var(--good)}}
.err{{background:var(--warn-soft);color:var(--warn)}}
.hint{{font-size:.82rem;color:var(--ink2);margin-top:14px}}
code{{background:var(--bg);padding:1px 6px;border-radius:5px}}
</style></head><body>
<h1>Daily log</h1>
<div class=sub>{date} · writes <code>log/{date}.md</code>, commits everything, pushes to GitHub.</div>
{msg}
<form method=post action=/log class=card>
  <label>What did you do today? What broke? What clicked?</label>
  <textarea name=note autofocus placeholder="e.g. Rebuilt the FastAPI endpoint from scratch, no Claude. Forgot the Depends() syntax, looked it up once. DDIA ch.1 notes done.">{prefill}</textarea>
  <div class=row>
    <div><label>Sessions done (~1.5h each)</label><input name=sessions type=number min=0 step=1 value="{sessions}"></div>
    <button type=submit>Save &amp; push</button>
  </div>
  <div class=hint>Tip: add your DSA solution files into <code>dsa/</code> and DDIA notes into <code>ddia/</code> first, then Save here. This commits them all in one shot.</div>
</form>
</body></html>"""

def today():
    return datetime.date.today().isoformat()

def read_today():
    p = os.path.join(LOGDIR, today() + ".md")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""

def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)

def render(msg="", msg_cls="", prefill="", sessions=""):
    m = f'<div class="msg {msg_cls}">{html.escape(msg)}</div>' if msg else ""
    return PAGE.format(date=today(), msg=m, prefill=html.escape(prefill),
                       sessions=html.escape(str(sessions)))

class H(http.server.BaseHTTPRequestHandler):
    def _send(self, body, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_GET(self):
        if self.path.startswith("/log"):
            self.send_response(303); self.send_header("Location", "/"); self.end_headers(); return
        self._send(render(prefill=read_today()))

    def log_message(self, *a):  # quiet
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        form = urllib.parse.parse_qs(self.rfile.read(n).decode("utf-8"))
        note = (form.get("note", [""])[0]).strip()
        sessions = (form.get("sessions", [""])[0]).strip()
        if not note:
            self._send(render("Write something first.", "err", "", sessions)); return

        # 1. write the log file (append if logging twice in a day)
        os.makedirs(LOGDIR, exist_ok=True)
        path = os.path.join(LOGDIR, today() + ".md")
        stamp = datetime.datetime.now().strftime("%H:%M")
        header = "" if os.path.exists(path) else f"# {today()}\n\n"
        entry = f"{header}**{stamp}** ({sessions or '?'} sessions)\n\n{note}\n\n---\n\n"
        with open(path, "a", encoding="utf-8") as f:
            f.write(entry)

        # 2. commit everything + push
        git("add", "-A")
        c = git("commit", "-m", f"log {today()}: {note[:60]}")
        if c.returncode != 0 and "nothing to commit" not in (c.stdout + c.stderr):
            self._send(render("Saved the file, but commit failed:\n" + c.stdout + c.stderr, "err", "", sessions)); return
        p = git("push")
        if p.returncode != 0:
            self._send(render("Logged & committed locally, but PUSH failed (offline?). Run study-os/save.sh later.\n" + p.stderr, "err")); return

        self._send(render(f"Saved, committed & pushed. Green square earned. ({sessions or '?'} sessions logged)", "ok"))

if __name__ == "__main__":
    os.makedirs(LOGDIR, exist_ok=True)
    with socketserver.TCPServer(("127.0.0.1", PORT), H) as s:
        print(f"\n  study-os daily log → http://localhost:{PORT}\n  (Ctrl+C to stop)\n")
        try:
            s.serve_forever()
        except KeyboardInterrupt:
            print("\n  stopped.\n")
