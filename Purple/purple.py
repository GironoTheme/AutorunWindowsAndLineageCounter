from Purple import go_to_la
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
from time import sleep
from logger import logger
import os


def find_purple_launcher(max_depth=3):
    try:
        drives = [f"{chr(drive)}:\\" for drive in range(ord('A'), ord('Z') + 1) if os.path.exists(f"{chr(drive)}:\\")]
        for drive in drives:
            for root, dirs, files in os.walk(drive):
                if root.count(os.sep) - drive.count(os.sep) > max_depth:
                    del dirs[:]
                    continue
                if 'PurpleLauncher.exe' in files:
                    full_path = os.path.join(root, 'PurpleLauncher.exe')
                    if 'Purple' in full_path:
                        return full_path
        logger.warning("PurpleLauncher.exe не найден.")
        return None
    except Exception as e:
        logger.error(f"Ошибка при поиске PurpleLauncher.exe: {e}")
        return None


launcher_path = find_purple_launcher()


class Window:
    def __init__(self):
        self.app = None

    def launch_purple(self):
        try:
            logger.info("Trying to connect to existing PURPLE window...")
            self.app = Application(backend="uia").connect(title='PURPLE')

        except (ElementNotFoundError, TimeoutError) as e:
            logger.info(f"PURPLE окно не найдено: {e}. Запуск нового экземпляра...")

            self.app = Application(backend="uia").start(launcher_path)
            sleep(35)

            try:
                self.app.connect(title='PURPLE')

            except (ElementNotFoundError, TimeoutError) as e:
                logger.error(f"Не удалось запустить или подключиться к окну PURPLE: {e}")
                return

            except Exception as e:
                logger.error(f"Произошла непредвиденная ошибка при запуске PURPLE: {e}")
                return

        self.app = self.app.PURPLE

        try:
            if not self.app.is_minimized():
                self.app.minimize()
            self.app.maximize()
            self.app.restore()

        except (ElementNotFoundError, TimeoutError) as e:
            logger.warning(f"Не удалось выполнить операцию на окне PURPLE: {e}")
            self.launch_purple()

        go_to_la.go_to_lineage(self.app)


class PurpleSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if PurpleSingleton._instance is None:
            PurpleSingleton._instance = Window()
        return PurpleSingleton._instance
