import os
from time import sleep
from ahk import AHK
from Check.check import match_x


def find_auto_hot_key():
    drives = [f"{chr(drive)}:\\" for drive in range(ord('A'), ord('Z') + 1) if os.path.exists(f"{chr(drive)}:\\")]

    for drive in drives:
        for root, dirs, files in os.walk(drive):
            if 'AutoHotkey.exe' in files:
                full_path = os.path.join(root, 'AutoHotkey.exe')
                return full_path

    return None


ahk = AHK(executable_path=find_auto_hot_key())


def move_and_click(x, y):
    ahk.mouse_move(x=x, y=y, blocking=True)
    ahk.click()


class GoToWorld:
    def manipulations_in_window(self, hwnd):
        sleep(3)
        self._maximize_window()
        self._click_to_x()
        self._click_to_my_characters()
        self._click_to_connect()
        self._click_on_auto_hunt()
        self._click_to_energy_saving()
        self._click_on_battery()

    def _maximize_window(self):
        sleep(1.5)
        ahk.mouse_move(25, 20)
        ahk.double_click()
        sleep(4)

    def _click_to_x(self):
        if match_x() is True:
            move_and_click(1535, 780)
            sleep(2)
            ahk.click()
            sleep(7)

    def _click_to_my_characters(self):
        move_and_click(1660, 815)
        sleep(4)

    def _click_to_connect(self):
        move_and_click(1500, 280)
        sleep(20)

    def _click_on_auto_hunt(self):
        move_and_click(1530, 550)
        sleep(1)

    def _click_to_energy_saving(self):
        move_and_click(65, 640)
        sleep(3)

    def _click_on_battery(self):
        move_and_click(930, 550)


go_to_world = GoToWorld()
