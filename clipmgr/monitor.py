import time, threading

class ClipboardMonitor:
    def __init__(self, interval=0.5, max_history=200):
        self.interval = interval
        self.max_history = max_history
        self.history = []
        self._running = False
        self._thread = None
        self._last = None

    def _get_clipboard(self):
        try:
            import subprocess
            r = subprocess.run(['xclip', '-selection', 'clipboard', '-o'],
                              capture_output=True, text=True, timeout=2)
            return r.stdout if r.returncode == 0 else None
        except Exception:
            return None

    def _poll(self):
        while self._running:
            content = self._get_clipboard()
            if content and content != self._last:
                self._last = content
                self.history.append({'text': content, 'ts': time.time()})
                if len(self.history) > self.max_history:
                    self.history.pop(0)
            time.sleep(self.interval)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._poll, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
