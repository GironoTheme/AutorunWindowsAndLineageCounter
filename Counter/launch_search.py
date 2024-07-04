import pystray
from PIL import Image, ImageDraw, ImageFont
from Counter.find_windows import find_windows
import time
import threading


class TrayIcon:
    def __init__(self):
        self.icon = pystray.Icon("Dynamic Number")
        self.number = 0
        self.running = True

    def create_image(self):
        image = Image.new('RGB', (64, 64), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        text = str(self.number)

        font = ImageFont.truetype("arial", 50)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        draw.text(((64 - text_width) / 2, (64 - text_height) / 2), text, font=font, fill="black")

        return image

    def update_icon(self):
        while self.running:
            self.number = find_windows()
            self.icon.icon = self.create_image()
            self.icon.visible = True
            time.sleep(15)

    def start(self):
        menu = pystray.Menu(
            pystray.MenuItem('Exit', self.stop)
        )

        self.icon.menu = menu
        threading.Thread(target=self.update_icon).start()
        self.icon.notify('Программа запущена', 'Закрепите иконку на панели задач для постоянной видимости.')
        self.icon.run()

    def stop(self):
        self.running = False
        self.icon.stop()


def launch_search():
    tray_icon = TrayIcon()
    try:
        tray_icon.start()
    except KeyboardInterrupt:
        tray_icon.stop()
