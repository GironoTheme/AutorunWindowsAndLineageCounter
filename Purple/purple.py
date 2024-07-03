from Purple import go_to_lineage
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
from time import sleep
import os


def find_purple_launcher():
    drives = [f"{chr(drive)}:\\" for drive in range(ord('A'), ord('Z') + 1) if os.path.exists(f"{chr(drive)}:\\")]

    for drive in drives:
        for root, dirs, files in os.walk(drive):
            if 'PurpleLauncher.exe' in files:
                full_path = os.path.join(root, 'PurpleLauncher.exe')
                if 'Purple' in full_path:
                    return full_path

    return None


launcher_path = find_purple_launcher()


class Window:
    def __init__(self):
        self.app = None

    def launch_purple(self):
        if self.app is not None:
            try:
                self.app.window(title='PURPLE')
                return
            except Exception:
                self.app = None

        try:
            self.app = Application(backend="uia").connect(title='PURPLE')

        except ElementNotFoundError:
            self.app = Application(backend="uia").start(launcher_path)
            sleep(35)
            self.app.connect(title='PURPLE')

        self.app = self.app.PURPLE

        self.app.minimize()
        self.app.maximize()
        self.app.restore()

        go_to_lineage.go_to_lineage(self.app)


class PurpleSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        PurpleSingleton._instance = Window()
        return PurpleSingleton._instance
