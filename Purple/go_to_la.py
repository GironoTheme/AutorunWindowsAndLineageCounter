def go_to_lineage(app):
    try:
        app.child_window(title="NGPClient.Models.PurpleHomeMenuItem", auto_id="L2M",
                              control_type="ListItem").is_visible()
    except:
        app.child_window(title="NGPClient.Models.PurpleBadgedMenuItem", auto_id="Game",
                              control_type="ListItem").click_input()
        app.child_window(title="Lineage2M", control_type="Text").click_input()


