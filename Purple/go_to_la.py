from time import sleep


def go_to_lineage(app):
    try:
        app.child_window(title="File Scan and Game Settings", auto_id="BtnGameSetting", control_type="Button").is_visible()
    except:
        app.child_window(title="NGPClient.Models.GameCard.GameCardItem", auto_id="Lineage2M",
                         control_type="ListItem").click_input()
        sleep(17)


