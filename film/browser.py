"""Browser segment of the demo film.

Drives the LIVE service in a real Chromium and records the viewport. Nothing is
mocked, nothing is sped up, no frame is composited afterwards. Rebuild with:

    cd ~/CODE/hack-fleet-ata && python3 film/browser.py
"""
from playwright.sync_api import sync_playwright
import pathlib, shutil, subprocess, sys

BASE = "https://fleet-wedge-33kamss2jq-uc.a.run.app/hold/"
PR = "https://github.com/Morkeeth/agent-work-record-witness-ata/pull/1/checks"
OUT = pathlib.Path("demo/seg-browser.mp4")
TMP = pathlib.Path("demo/.browser-raw")

CURSOR = """
(() => {
  const d = document.createElement('div');
  d.id = '__vo_cursor';
  d.style.cssText = 'position:fixed;z-index:2147483647;width:18px;height:18px;'
    + 'margin:-9px 0 0 -9px;border-radius:50%;background:rgba(26,115,232,.35);'
    + 'border:2px solid #1a73e8;pointer-events:none;left:-100px;top:-100px;'
    + 'transition:left .35s ease,top .35s ease;';
  document.documentElement.appendChild(d);
  window.__vo_to = (x, y) => { d.style.left = x + 'px'; d.style.top = y + 'px'; };
})()
"""


def point(pg, selector):
    """Move the on-screen cursor over an element, then click it."""
    el = pg.locator(selector).first
    el.scroll_into_view_if_needed()
    box = el.bounding_box()
    if box:
        pg.evaluate("([x,y])=>window.__vo_to(x,y)",
                    [box["x"] + box["width"] / 2, box["y"] + box["height"] / 2])
        pg.wait_for_timeout(700)
    el.click()


def main():
    if TMP.exists():
        shutil.rmtree(TMP)
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1600, "height": 900},
                            record_video_dir=str(TMP),
                            record_video_size={"width": 1600, "height": 900})
        pg = ctx.new_page()

        # 1 · the finding — what it measured on us before anyone else
        pg.goto(BASE + "#finding", wait_until="load")
        pg.add_init_script(CURSOR)
        pg.evaluate(CURSOR)
        pg.wait_for_timeout(4000)
        pg.mouse.wheel(0, 450); pg.wait_for_timeout(5000)
        pg.mouse.wheel(0, 450); pg.wait_for_timeout(4000)

        # 2 · the record — a held claim that opens back to its session
        pg.goto(BASE + "?record=H-a6151a95ac", wait_until="load")
        pg.evaluate(CURSOR); pg.wait_for_timeout(4000)
        pg.mouse.wheel(0, 400); pg.wait_for_timeout(5000)
        pg.mouse.wheel(0, 500); pg.wait_for_timeout(5000)

        # 3 · where it runs on Google
        point(pg, "text=Google stack"); pg.wait_for_timeout(4000)
        pg.mouse.wheel(0, 500); pg.wait_for_timeout(5000)
        pg.mouse.wheel(0, 500); pg.wait_for_timeout(4000)

        # 4 · the queue humans actually open
        point(pg, "text=Hold queue"); pg.wait_for_timeout(4500)

        # 5 · the record, and the number that does not flatter us
        point(pg, "text=Audit"); pg.wait_for_timeout(6000)
        pg.mouse.wheel(0, 350); pg.wait_for_timeout(4000)

        # 5b · how a stranger installs it, and the policy it runs under
        point(pg, "text=Install"); pg.wait_for_timeout(5000)
        pg.mouse.wheel(0, 450); pg.wait_for_timeout(5000)
        point(pg, "text=Policy"); pg.wait_for_timeout(5000)

        # 6 · the check, red on a real pull request
        pg.goto(PR, wait_until="load"); pg.wait_for_timeout(4000)
        pg.evaluate(CURSOR)
        try:
            point(pg, "text=HOLD Outcome Clearance")
            pg.wait_for_timeout(3000)
            point(pg, "text=verify-claims")
            pg.wait_for_timeout(7000)
        except Exception:
            pg.wait_for_timeout(8000)

        video = pg.video
        ctx.close(); b.close()
        raw = pathlib.Path(video.path())

    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
                    "-vf", "scale=1920:1080:flags=lanczos,fps=30",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "21",
                    "-pix_fmt", "yuv420p", str(OUT)], check=True)
    shutil.rmtree(TMP, ignore_errors=True)
    print("WROTE", OUT)


if __name__ == "__main__":
    sys.exit(main())
