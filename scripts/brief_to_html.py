#!/usr/bin/env python3
"""Turn output/YYYY-MM-DD/morning-brief.md into a styled, phone-friendly HTML page
for the private claude.ai brief page.

Usage: python3 scripts/brief_to_html.py output/2026-11-01/morning-brief.md [--out path.html]
Default output: alongside the .md, as morning-brief.html
"""
import argparse
import re
import subprocess
from pathlib import Path

CSS = r"""
<title>WORKTECH Morning Brief</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: one reading column, wide tables scroll inside their own frame; priority shown as chips */
:root{
  --bg:#f6f7f5; --surface:#ffffff; --ink:#18232e; --muted:#5b6670; --rule:#dde2e0;
  --accent:#1f6f6b; --a:#1f6f6b; --a-bg:#dcefed; --b:#8a5a12; --b-bg:#f6ead6; --c:#5b6670; --c-bg:#e9ecec;
  --flag:#9b3d2e;
  --display:"Newsreader", Georgia, "Times New Roman", serif;
  --body:"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono:"IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#11171c; --surface:#172028; --ink:#e4e9ec; --muted:#9aa6ae; --rule:#2a3540;
  --accent:#5cc2bb; --a:#7fd6cf; --a-bg:#173a38; --b:#e3b56b; --b-bg:#3a2c14; --c:#aab4ba; --c-bg:#26313a; --flag:#f08f7c; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#11171c; --surface:#172028; --ink:#e4e9ec; --muted:#9aa6ae; --rule:#2a3540;
  --accent:#5cc2bb; --a:#7fd6cf; --a-bg:#173a38; --b:#e3b56b; --b-bg:#3a2c14; --c:#aab4ba; --c-bg:#26313a; --flag:#f08f7c; color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:15px/1.6 var(--body);
  padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px));padding-block:28px 56px}
main{max-width:1040px;margin:0 auto;display:flex;flex-direction:column;gap:6px}
h1{font:600 clamp(1.6rem, 4vw, 2.3rem)/1.15 var(--display);margin:0 0 6px;text-wrap:balance;letter-spacing:-.01em}
h2{font:600 1.35rem/1.25 var(--display);margin:30px 0 8px;padding-top:14px;border-top:1px solid var(--rule);text-wrap:balance}
h3{font:600 1rem/1.35 var(--body);margin:18px 0 4px;color:var(--accent)}
p,li{max-width:72ch}
h1 + p{font-size:.95rem;color:var(--muted)}
h1 + p strong{color:var(--ink)}
a{color:var(--accent);text-underline-offset:2px}
a:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:2px}
blockquote{margin:10px 0;padding:10px 14px;background:var(--surface);border:1px solid var(--rule);border-radius:6px;color:var(--muted);font-size:.92rem}
blockquote p{margin:0}
ol,ul{padding-left:1.3em;margin:6px 0} li{margin:3px 0}
em{color:var(--muted);font-size:.9rem}
.tw{overflow-x:auto;background:var(--surface);border:1px solid var(--rule);border-radius:6px;margin:8px 0}
table{border-collapse:collapse;width:100%;font-size:.86rem;min-width:640px}
th{font:500 .72rem/1.3 var(--body);text-transform:uppercase;letter-spacing:.06em;color:var(--muted);text-align:left;padding:9px 10px;border-bottom:1px solid var(--rule);white-space:nowrap}
td{padding:9px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
tr:last-child td{border-bottom:0}
td.num{font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
.pri{display:inline-block;min-width:1.6em;text-align:center;font:600 .78rem/1.6 var(--mono);border-radius:4px;padding:0 6px}
.pri.a{color:var(--a);background:var(--a-bg)} .pri.b{color:var(--b);background:var(--b-bg)} .pri.c{color:var(--c);background:var(--c-bg)}
.flag{color:var(--flag);font-weight:500}
code{font-family:var(--mono);font-size:.85em}
@media (prefers-reduced-motion: reduce){*{scroll-behavior:auto}}
</style>
"""


def convert(md_path: Path) -> str:
    html = subprocess.run(["pandoc", str(md_path), "-f", "gfm", "-t", "html5"],
                          check=True, capture_output=True, text=True).stdout
    html = re.sub(r"<table>", '<div class="tw"><table>', html)
    html = re.sub(r"</table>", "</table></div>", html)
    html = re.sub(r"<td>([ABC])</td>", lambda m: f'<td><span class="pri {m.group(1).lower()}">{m.group(1)}</span></td>', html)
    html = re.sub(r"<td>(\d{1,2})</td>", r'<td class="num">\1</td>', html)
    html = html.replace("⚑", '<span class="flag">⚑</span>').replace("⚠", '<span class="flag">⚠</span>')
    html = re.sub(r"<a href=", '<a target="_blank" rel="noopener" href=', html)
    return CSS + "<main>\n" + html + "</main>\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("markdown")
    ap.add_argument("--out")
    a = ap.parse_args()
    src = Path(a.markdown)
    out = Path(a.out) if a.out else src.with_suffix(".html")
    out.write_text(convert(src), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
