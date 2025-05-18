import sys
from PyQt5 import QtWidgets
from detection import get_latest_screenshot, detect_matches
from overlay import OverlayWindow
import threading

STEAM_FOLDER = 'c:\\temp\\screenshots\\'
TEMPLATE_PATHS = [
    'maps\\test_1.png',
    'maps\\test_2.png',
    'maps\\test_3.png'
]

def main():
    screenshot = get_latest_screenshot(STEAM_FOLDER)
    if not screenshot:
        print("No screenshot found.")
        return

    print(f"Latest screenshot found: {screenshot}")

    rectangles, image = detect_matches(screenshot, TEMPLATE_PATHS)
    if rectangles:
        app = QtWidgets.QApplication(sys.argv)
        overlay = OverlayWindow(rectangles)
        overlay.toggle_signal.connect(overlay.toggle_vissibility)
        listener_thread = threading.Thread(target=OverlayWindow.listen_for_hotkey, args=(overlay,))
        listener_thread.start()
        sys.exit(app.exec_())
    else:
        print("No matches found.")

if __name__ == "__main__":
    main()
