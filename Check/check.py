import numpy as np
import PIL.ImageGrab
import cv2


def matching(main_image_name, template_image_name, need_for_taking_screenshot=False, threshold=0.8,
             func=None, area_of_screenshot=None):
    """Функция для сравнения 2ух изображений\n
    main_image_name - название основного изображения\n
    template_image_name - названия шаблона для сравнения\n
    need_for_taking_screenshot - нужно ли делать скриншот\n
    threshold - минимальный уровень совпадения 2ух изображений\n
    func - нужно ли возвращать координаты\n
    area_of_screenshot - область в которой нужно сделать скриншот. (указывать как тапл). Если оставить None, то будет сделан скриншот всего экрана
    """
    if need_for_taking_screenshot:
        if area_of_screenshot:
            PIL.ImageGrab.grab(bbox=area_of_screenshot).save(main_image_name)
        else:
            PIL.ImageGrab.grab().save(main_image_name)
    img_rgb = cv2.imread(main_image_name)
    template = cv2.imread(template_image_name)
    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    if func is None:
        for pt in zip(*loc[::-1]):
            return True
        return False
    for pt in zip(*loc[::-1]):
        return pt
    return False


def take_screenshot(image_name, area_of_screenshot):
    """Функция для создания скриншота\n
    image_name - название изображения скриншота\n
    area_of_screenshot - область скриншота(указывать как тапл)
    """
    if area_of_screenshot:
        PIL.ImageGrab.grab(bbox=area_of_screenshot).save(image_name)
    else:
        PIL.ImageGrab.grab().save(image_name)


def x():
    take_screenshot('Images\\x.png', (1505, 760, 1565, 805))


def lineage():
    take_screenshot('Images\\lineage.png', (5, 5, 125, 35))


def match_x():
    x()
    if matching('Images\\x_original.png', 'Images\\x.png') is True:
        return True

    return False


def match_lineage():
    lineage()
    if matching('Images\\lineage_original.png', 'Images\\lineage.png') is True:
        return True

    return False


def find_character():
    take_screenshot('Images\\last_account_original.png', (1078, 264, 1365, 284))




