import threading
import time

from project.domain.sessions.session_bl import SessionsBl


def start_maintenance_thread():
    def loop():
        while True:
            try:
                SessionsBl.maintenance_tick()
                time.sleep(30)
            except Exception:
                pass
                time.sleep(5) # частота проверки 5 сек: увидит >60 сек тишины и время окончания
    th = threading.Thread(target=loop, daemon=True)
    th.start()