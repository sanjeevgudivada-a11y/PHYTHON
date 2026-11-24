#!/usr/bin/env python3
"""Run every case-study solution, capture its output and render screenshots.

For each folder  NN-*/ containing exactly one top-level *.py solution script:
  1. run the script and save stdout to   <folder>/outputs/run_output.txt
  2. split the output on lines starting with "=== " (test-case markers)
  3. render each chunk as a terminal-style PNG screenshot in <folder>/outputs/
"""

import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

BG = "#0d1117"
BAR = "#161b22"
FG = "#e6edf3"
DIM = "#8b949e"
ACCENT = "#7ee787"
LINE_H = 25
BAR_H = 38
PAD = 18
MAX_LINES_PER_PAGE = 56


def find_cases():
    cases = []
    for name in sorted(os.listdir(ROOT)):
        d = os.path.join(ROOT, name)
        if not os.path.isdir(d) or not re.match(r"^\d\d-", name):
            continue
        scripts = [f for f in sorted(os.listdir(d))
                   if f.endswith(".py") and os.path.isfile(os.path.join(d, f))]
        if scripts:
            cases.append((name, scripts[0]))
    return cases


def split_tests(output):
    """Split captured output into chunks on '=== ' marker lines.
    Text before the first marker stays with the first chunk."""
    lines = output.splitlines()
    chunks, cur = [], []
    seen_marker = False
    for ln in lines:
        if ln.startswith("=== ") and seen_marker:
            chunks.append(cur)
            cur = [ln]
        else:
            if ln.startswith("=== "):
                seen_marker = True
            cur.append(ln)
    if cur:
        chunks.append(cur)
    return chunks


def chunk_name(idx, chunk):
    for ln in chunk:
        if ln.startswith("=== "):
            m = re.search(r"TEST\s*CASE\s*0*([0-9]+)", ln, re.I)
            if m:
                return "test%d" % int(m.group(1))
            slug = re.sub(r"[^a-z0-9]+", "_", ln[4:].lower()).strip("_")
            return (slug or "part%d" % idx)[:40]
    return "output" if idx == 0 else "part%d" % idx


def render_png(lines, title, out_path):
    # choose font size so the widest line fits
    for size in (15, 14, 13, 12, 11):
        font = ImageFont.truetype(MONO, size)
        bold = ImageFont.truetype(MONO_BOLD, size)
        widest = max((font.getlength(l) for l in lines), default=0)
        width = int(widest) + 2 * PAD
        if width <= 1500:
            break
    width = max(width, 760)
    height = BAR_H + len(lines) * LINE_H + 2 * PAD
    img = Image.new("RGB", (width, height), BG)
    dr = ImageDraw.Draw(img)
    # title bar
    dr.rectangle([0, 0, width, BAR_H], fill=BAR)
    for i, c in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        dr.ellipse([14 + i * 20, 13, 24 + i * 20, 23], fill=c)
    dr.text((84, 11), title, font=bold, fill=DIM)
    # body
    y = BAR_H + PAD
    for ln in lines:
        color = ACCENT if ln.startswith("===") else FG
        dr.text((PAD, y), ln, font=font, fill=color)
        y += LINE_H
    img.save(out_path)
    return out_path


def main():
    cases = find_cases()
    if not cases:
        print("No case folders found.")
        return
    for folder, script in cases:
        d = os.path.join(ROOT, folder)
        out_dir = os.path.join(d, "outputs")
        os.makedirs(out_dir, exist_ok=True)
        proc = subprocess.run([sys.executable, script], cwd=d,
                              capture_output=True, text=True)
        output = proc.stdout
        if proc.stderr.strip():
            output += "\n[stderr]\n" + proc.stderr
        with open(os.path.join(out_dir, "run_output.txt"), "w",
                  encoding="utf-8") as f:
            f.write(output)
        status = "ok" if proc.returncode == 0 else "EXIT %d" % proc.returncode
        # clean old screenshots for this case
        for f in os.listdir(out_dir):
            if f.startswith("screenshot") and f.endswith(".png"):
                os.remove(os.path.join(out_dir, f))
        chunks = split_tests(output)
        made = []
        for i, chunk in enumerate(chunks):
            name = chunk_name(i, chunk)
            pages = [chunk[j:j + MAX_LINES_PER_PAGE]
                     for j in range(0, len(chunk), MAX_LINES_PER_PAGE)]
            for p, page in enumerate(pages, 1):
                if len(pages) > 1:
                    fname = "screenshot_%s_p%d.png" % (name, p)
                else:
                    fname = "screenshot_%s.png" % name
                title = "%s/%s  -  %s" % (folder, script, name)
                made.append(os.path.basename(
                    render_png(page, title, os.path.join(out_dir, fname))))
        print("%-42s %-8s -> %s" % (folder, status, ", ".join(made)))


if __name__ == "__main__":
    main()
