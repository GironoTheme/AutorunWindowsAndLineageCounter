from time import sleep


def check(app):
    sleep(10)
    try:
        if app.child_window(auto_id="SignInGateView", control_type="Custom").exists():
            app.child_window(auto_id="PART_Close", control_type="Button").click_input()
            sleep(3)
            return True

    except:
        try:
            app.child_window(auto_id="CloseButton", control_type="Button").click_input()
            sleep(1)
            return True
        except:
            return False
