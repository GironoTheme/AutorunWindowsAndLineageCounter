from time import sleep
from pywinauto import mouse
from Purple import go_to_lineage, skip_an_unauthorized_account
from Purple.purple import PurpleSingleton


class GoingThroughMainAccounts:
    def __init__(self):
        self.app = None

    def _get_purple(self):
        purple_instance = PurpleSingleton.get_instance()
        purple_instance.launch_purple()

        self.app = purple_instance.app

    def _check_authorization(self):
        sleep(6)
        if skip_an_unauthorized_account.check(self.app) is True:
            self._get_purple()
            go_to_lineage.go_to_lineage(self.app)
            sleep(4)
            return True

        return False

    def iter_main_accounts(self, func):
        self._get_purple()

        accounts_used = ["b***ge@mail.ru", "dada***88@rambler.ru"]

        go_to_lineage.go_to_lineage(self.app)

        while True:
            self._open_main_accounts_management()

            current_account = self.app.child_window(auto_id="CurrentAccountDisplayAccount", control_type="Text").texts()[0]

            if current_account not in accounts_used:
                accounts_used.append(current_account)

            buttons = self._main_accounts()
            index = 0
            found_new_account = False

            while index < len(buttons):
                account_text = buttons[index].texts()[0]

                if account_text not in accounts_used:
                    buttons[index].click_input()
                    self.app.child_window(title="Confirm", control_type="Text").click_input()

                    if self._check_authorization():
                        accounts_used.append(account_text)
                        found_new_account = True
                        break

                    sleep(20)
                    accounts_used.append(account_text)

                    go_to_lineage.go_to_lineage(self.app)
                    func()
                    found_new_account = True
                    break

                index += 1

            if index == 4:
                element = self.app.child_window(auto_id="VerticalScrollBar", control_type="ScrollBar")
                rect = element.rectangle()
                mouse.scroll(coords=(rect.left, rect.top), wheel_dist=-5)

            if not found_new_account and index >= len(buttons):
                break

    def _open_main_accounts_management(self):
        self.app.child_window(title="NGPClient.Models.PurpleBadgedMenuItem", auto_id="MyPage",
                              control_type="ListItem").wrapper_object().click_input()

    def _main_accounts(self):
        parent_pane = self.app.child_window(auto_id="ListBox", control_type="List")
        return parent_pane.descendants(control_type="Text")


going_through_main_accounts = GoingThroughMainAccounts()

