#!/usr/bin/env python3
"""Geometry QA for generated flowcharts.

Parses every flowchart.svg and reports:
  * flow lines that pass THROUGH a node box (must be zero)
  * line/line crossings (informational - acceptable if few)
Exit code 1 if any line pierces a node.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse(svg_text, is_background_rect):
    rects = []
    polys = []
    lines = []
    for m in re.finditer(
            r'<rect x="([-\d.]+)" y="([-\d.]+)" width="([\d.]+)" '
            r'height="([\d.]+)"[^/]*/>', svg_text):
        x, y, w, h = (float(g) for g in m.groups())
        if is_background_rect(x, y, w, h):
            continue
        rects.append((x, y, x + w, y + h))
    for m in re.finditer(r'<polygon points="([^"]+)"', svg_text):
        pts = []
        for pair in m.group(1).split():
            px, py = pair.split(",")
            pts.append((float(px), float(py)))
        if len(pts) == 3:          # arrowhead - ignore
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        polys.append((min(xs), min(ys), max(xs), max(ys)))
    for m in re.finditer(
            r'<line x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" '
            r'y2="([-\d.]+)"', svg_text):
        x1, y1, x2, y2 = (float(g) for g in m.groups())
        lines.append((x1, y1, x2, y2))
    return rects + polys, lines


def seg_hits_box(seg, box, pad=1.5):
    x1, y1, x2, y2 = seg
    bx1, by1, bx2, by2 = box
    bx1 += pad
    by1 += pad
    bx2 -= pad
    by2 -= pad
    if bx1 >= bx2 or by1 >= by2:
        return False
    if abs(y1 - y2) < 0.01:        # horizontal
        y = y1
        lo, hi = min(x1, x2), max(x1, x2)
        return by1 < y < by2 and lo < bx2 and hi > bx1 and not (
            hi <= bx1 or lo >= bx2)
    if abs(x1 - x2) < 0.01:        # vertical
        x = x1
        lo, hi = min(y1, y2), max(y1, y2)
        return bx1 < x < bx2 and lo < by2 and hi > by1 and not (
            hi <= by1 or lo >= by2)
    return False


def seg_crossings(lines):
    crossings = 0
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            a, b = lines[i], lines[j]
            a_h = abs(a[1] - a[3]) < 0.01
            b_h = abs(b[1] - b[3]) < 0.01
            if a_h == b_h:
                continue            # parallel (both H or both V)
            if a_h:
                hx1, hy, hx2 = a[0], a[1], a[2]
                vx, vy1, vy2 = b[0], b[1], b[3]
            else:
                hx1, hy, hx2 = b[0], b[1], b[2]
                vx, vy1, vy2 = a[0], a[1], a[3]
            if min(hx1, hx2) < vx < max(hx1, hx2) and \
               min(vy1, vy2) < hy < max(vy1, vy2):
                crossings += 1
    return crossings


def main():
    failures = 0
    for name in sorted(os.listdir(ROOT)):
        path = os.path.join(ROOT, name, "flowchart.svg")
        if not os.path.isfile(path):
            continue
        svg = open(path, encoding="utf-8").read()
        vb = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', svg)
        vx, vy, vw, vh = (float(g) for g in vb.groups())

        def is_bg(x, y, w, h, vx=vx, vy=vy, vw=vw, vh=vh):
            return abs(x - vx) < 1 and abs(y - vy) < 1 and \
                abs(w - vw) < 1 and abs(h - vh) < 1

        boxes, lines = parse(svg, is_bg)
        pierced = []
        for seg in lines:
            for idx, box in enumerate(boxes):
                if seg_hits_box(seg, box):
                    pierced.append((idx, seg, box))
        crossings = seg_crossings(lines)
        status = "OK" if not pierced else "PIERCED"
        print("%-46s nodes=%-3d lines=%-3d crossings=%-3d %s"
              % (name, len(boxes), len(lines), crossings, status))
        for idx, seg, box in pierced[:6]:
            print("    line %s pierces node box %s" % (seg, box))
        if pierced:
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
