from Purple import go_to_lineage
from Purple.going_through_main_accounts import going_through_main_accounts
from Purple import skip_an_unauthorized_account
from Lineage.run_lineage_windows import run_lineage_windows
from time import sleep

from Purple.purple import PurpleSingleton


class AutorunLineageWindows:
    def __init__(self):
        self.app = None
        self.launch_purple = None

    def launch(self):
        self._get_purple()

        self._manipulations()

        going_through_main_accounts.iter_main_accounts(self._manipulations)

    def _get_purple(self):
        sleep(4)
        purple_instance = PurpleSingleton.get_instance()
        self.launch_purple = purple_instance.launch_purple()
        self.app = purple_instance.app

    def _check_authorization(self):
        sleep(6)
        if skip_an_unauthorized_account.check(self.app) is True:
            self.launch_purple()
            go_to_lineage.go_to_lineage(self.app)
            sleep(4)
            return True

        return False

    def _manipulations(self):
        self._start_game_on_main_account()
        self._multi_account_management()

    def _start_game_on_main_account(self):
        sleep(1)
        try:
            self.app.child_window(title="Running game", control_type="Text").is_visible()

        except:
            self.app.child_window(title="Start Game", auto_id="PlayButton", control_type="Button").wrapper_object().click_input()

            if self._check_authorization() is False:
                self._up_purple()

    def _multi_account_management(self):
        sleep(2)
        self._open_multi_account()
        self._open_multi_account_settings()
        self._enumeration_accounts()

    def _open_multi_account(self):
        sleep(1)
        multi_account = self.app.child_window(auto_id="BtnOpenMultiAccount", control_type="Button")
        multi_account.wait('visible')

        if multi_account.get_toggle_state() == 0:
            multi_account.wrapper_object().click_input()

    def _open_multi_account_settings(self):
        sleep(1)
        self.app.child_window(auto_id="AccountManagementButton", control_type="Button").wrapper_object().click_input()

    def _enumeration_accounts(self):
        sleep(1)

        all_checkboxes = self.app.descendants(control_type="CheckBox")

        checkboxes = [checkbox for checkbox in all_checkboxes if
                      checkbox.element_info.automation_id == "MultiAccountListCheckBox"]

        if self._checking_checkboxes(checkboxes):
            for index, checkbox in enumerate(checkboxes):
                try:
                    sleep(1)
                    if index != 0:
                        self._open_multi_account()
                        self._open_multi_account_settings()

                    all_checkboxes = self.app.descendants(control_type="CheckBox")
                    checkboxes = [checkbox for checkbox in all_checkboxes if
                                  checkbox.element_info.automation_id == "MultiAccountListCheckBox"]

                    checkbox = checkboxes[index]
                    is_checked = checkbox.get_toggle_state()

                    if index == 0 and is_checked == 1:
                        self._start_game_for_multi_accounts()

                    elif index == 0 and is_checked == 0:
                        for el in range(index + 1, len(checkboxes)):
                            if checkboxes[el].get_toggle_state() == 1:
                                checkboxes[el].click_input()
                                break

                        checkbox.click_input()
                        self._start_game_for_multi_accounts()

                    if index > 0:

                        prev_checkbox = checkboxes[index - 1]
                        prev_checkbox.click_input()
                        sleep(1)

                        checkbox.click_input()
                        self._start_game_for_multi_accounts()

                    if index >= len(checkboxes):
                        print(f"Checkbox {index} no longer exists, ending loop.")
                        break

                except Exception as e:
                    print(f"Не удалось взаимодействовать с CheckBox {index}: {e}")

        try:
            self.app.child_window(auto_id="CloseButton", control_type="Button").wrapper_object().click_input()
        except:
            pass

    def _checking_checkboxes(self, checkboxes):
        if not checkboxes:
            return False
        else:
            return True

    def _up_purple(self):
        sleep(85)
        run_lineage_windows.switch_windows()

        self.app.set_focus()
        self.app.minimize()
        self.app.maximize()
        self.app.restore()
        sleep(1)

    def _start_game_for_multi_accounts(self):
        sleep(1)

        self.app.child_window(title="Confirm", control_type="Button").click_input()
        sleep(1)

        if self._check_authorization() is False:
            self._open_multi_account()
            sleep(4)

            try:
                self.app.child_window(title="Running game", auto_id="BtnGameRunning", control_type="Button").is_visible()

            except:
                self.app.child_window(auto_id="BtnGameRun", control_type="Button").click_input()

                if self._check_authorization() is False:
                    self._up_purple()


autorun_lineage_windows = AutorunLineageWindows()
