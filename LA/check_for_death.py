from pathlib import Path
from ahk import AHK
from time import sleep
from Check.check import matching, take_screenshot
import pytesseract
import os

def find_file(file_name):
    drives = [f"{chr(drive)}:\\" for drive in range(ord('A'), ord('Z') + 1) if os.path.exists(f"{chr(drive)}:\\")]
    for drive in drives:
        for root_path in Path(drive).rglob(file_name):
            return root_path

    return None


ahk = AHK(executable_path=str(find_file("AutoHotkey.exe")))
path_to_tesseract = find_file("tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = path_to_tesseract


def move_and_click(x, y):
    ahk.mouse_move(x=x, y=y, blocking=True)
    ahk.click()


def is_dead():
    """Проверка на то, умер ли персонаж"""

    take_screenshot(f'Images\\is_dead.png', area_of_screenshot=(730, 825, 1125, 920))

    dead_button_1 = matching(f'Images\\imgs\\is_dead.png',
                             f'Images\\dead.png', need_for_taking_screenshot=False)

    dead_button_2 = matching(f'Images\\is_dead.png',
                             f'Images\\dead2.png', need_for_taking_screenshot=False)

    if dead_button_1 or dead_button_2:
        sleep(10)
        revive()
        return True

    return False


def revive():
    def __send_to_last_location():
        move_and_click(x=350, y=180)
        move_and_click(x=250, y=350)
        move_and_click(x=420, y=460)

        sleep(4)

        move_and_click(x=1530, y=550)

    move_and_click(x=900, y=870)

    sleep(5)

    move_and_click(x=1250, y=80)
    take_screenshot('Images\\amount_of_free_revives.png', area_of_screenshot=(385, 600, 420, 640))

    try:
        amount_of_free_revives = int(pytesseract.image_to_string('Images\\amount_of_free_revives.png',
                                     config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))

    except:
        move_and_click(x=1050, y=700)

        __send_to_last_location()
        return

    while matching('Images\\is_items_lose_via_death.png', 'Images\\adena.png', need_for_taking_screenshot=True,
                   area_of_screenshot=(430, 600, 480, 650)) is False:
        move_and_click(x=500, y=620)

    if amount_of_free_revives == 0:
        ahk.key_press('esc')
        __send_to_last_location()
        return

    counter = 0
    if amount_of_free_revives > 3:
        amount_of_free_revives = 3
    else:
        amount_of_free_revives = 1

    for i in range(amount_of_free_revives):
        move_and_click(x=500, y=250 + counter)
        counter += 100

    move_and_click(x=520, y=740)
    move_and_click(x=1050, y=700)
    move_and_click(x=400, y=190)

    while matching('Images\\is_items_lose_via_death.png',
                   'Images\\adena.png',
                   need_for_taking_screenshot=True,
                   area_of_screenshot=(430, 600, 480, 650)) is False:

        move_and_click(x=500, y=620)

    for i in range(4):
        move_and_click(x=500, y=250 + (i * 100))

    move_and_click(x=520, y=740)
    move_and_click(x=1050, y=700)

    move_and_click(x=530, y=170)

    __send_to_last_location()

