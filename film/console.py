"""Record the Google Cloud Console for the film.

The Console needs a logged-in Google session, which no service credential provides.
So this uses a DEDICATED browser profile that Oscar signs into once by hand. His
password never reaches this process, and his everyday Chrome profile is untouched.

    python3 film/console.py --login     # opens Chrome. Sign in, then close the window.
    python3 film/console.py --record    # replays the same profile and records the tour

Profile lives at ~/.ata-film-profile. Delete that directory to revoke.
"""
from playwright.sync_api import sync_playwright
import pathlib, shutil, subprocess, sys

PROFILE = str(pathlib.Path.home() / ".ata-film-profile")
PROJECT = "hack-fleet"
SERVICE = (f"https://console.cloud.google.com/run/detail/us-central1/fleet-wedge"
           f"/metrics?project={PROJECT}")
REVISIONS = (f"https://console.cloud.google.com/run/detail/us-central1/fleet-wedge"
             f"/revisions?project={PROJECT}")
LOGS = (f"https://console.cloud.google.com/run/detail/us-central1/fleet-wedge"
        f"/observability/logs?project={PROJECT}")
OUT = pathlib.Path("demo/seg-console.mp4")
TMP = pathlib.Path("demo/.console-raw")


def login():
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, channel="chrome", headless=False,
            viewport={"width": 1600, "height": 900},
            ignore_default_args=["--enable-automation", "--disable-extensions"],
            args=["--start-maximized",
                  "--disable-blink-features=AutomationControlled"])
        ctx.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        pg.goto(SERVICE)
        print("\n  Sign in to Google in the window that just opened.")
        print("  When the Cloud Run page for 'fleet-wedge' is on screen, CLOSE THE WINDOW.")
        print("  Nothing is recorded during this step.\n")
        try:
            pg.wait_for_event("close", timeout=0)
        except Exception:
            pass
        ctx.close()
    print("  Profile saved. Now run:  python3 film/console.py --record")


def record():
    if TMP.exists():
        shutil.rmtree(TMP)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, channel="chrome", headless=False,
            viewport={"width": 1600, "height": 900},
            record_video_dir=str(TMP),
            record_video_size={"width": 1600, "height": 900})
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        first = True
        for url, dwell in ((SERVICE, 5000), (LOGS, 5000)):  # revisions dropped: gcloud already named the revision, and the 4:00 cap is real
            pg.goto(url, wait_until="load")
            pg.wait_for_timeout(3000)
            if first:
                # the cookie banner sits across the bottom of every page until dismissed
                for sel in ("button:has-text('Understood')", "button:has-text('Accept all')"):
                    try:
                        pg.locator(sel).first.click(timeout=2500)
                        break
                    except Exception:
                        pass
                first = False
            pg.wait_for_timeout(dwell)
            pg.mouse.wheel(0, 400)
            pg.wait_for_timeout(4000)
        video = pg.video
        ctx.close()
        raw = pathlib.Path(video.path())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
                    "-vf", "scale=1920:1080:flags=lanczos,fps=30",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "21",
                    "-pix_fmt", "yuv420p", str(OUT)], check=True)
    shutil.rmtree(TMP, ignore_errors=True)
    print("WROTE", OUT)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--login"
    (login if mode == "--login" else record)()
