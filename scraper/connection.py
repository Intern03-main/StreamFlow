import time
import socket


def wait_for_connection(url, page):
    """Wait for an internet connection and reload the page when active."""
    while not is_connected():
        print("[WARNING] Internet disconnected. Retrying...")
        time.sleep(10)

    print("[INFO] Internet connection restored. Reloading page...")
    safe_page_goto(page, url)


def is_connected(host="8.8.8.8", port=53, timeout=3):
    """Check if the internet connection is active."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection((host, port))
        return True
    except OSError:
        return False


def safe_page_goto(page, url, retries=5, wait_time=10):
    """Load a page with retries if internet fails."""
    attempt = 0
    while attempt < retries:
        try:
            print(f"[INFO] Loading {url}... (Attempt {attempt + 1}/{retries})")
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_load_state("load")
            time.sleep(3)
            return
        except Exception as e:
            print(f"[WARNING] Failed to load page: {e}")
            attempt += 1
            time.sleep(wait_time)

    print("[ERROR] All attempts to load the page failed. Exiting...")
    raise Exception("Failed to load page after multiple retries.")
