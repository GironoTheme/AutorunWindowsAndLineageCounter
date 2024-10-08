from pywinauto.findwindows import ElementNotFoundError
from Counter.launch_search import launch_search
from Purple import go_to_la
from Purple.going_through_main_accounts import going_through_main_accounts
from Purple import skip_an_unauthorized_account
from LA.run_la_windows import run_lineage_windows
from time import sleep
from logger import logger
from Purple.purple import PurpleSingleton


class AutorunLineageWindows:
    def __init__(self):
        self.app = None
        self.launch_purple = None

    def launch(self):
        self._get_purple()
        self._manipulations()
        going_through_main_accounts.iter_main_accounts(self._manipulations)
        launch_search()

    def _get_purple(self):
        sleep(4)
        purple_instance = PurpleSingleton.get_instance()
        self.launch_purple = purple_instance.launch_purple
        self.launch_purple()

        self.app = purple_instance.app

    def _check_authorization(self):
        sleep(8)
        if skip_an_unauthorized_account.check(self.app) is True:
            self.launch_purple()
            go_to_la.go_to_lineage(self.app)
            sleep(4)
            return True

        return False

    def _manipulations(self):
        self._start_game_on_main_account()
        self._multi_account_management()

    def _start_game_on_main_account(self):
        def _start_game():
            self.app.child_window(title="Start Game", auto_id="PlayButton",
                                  control_type="Button").wrapper_object().click_input()
            if self._check_authorization() is False:
                self._up_purple()

        sleep(1)
        try:
            self.app.child_window(title="Running game", control_type="Text").is_visible()

        except:
            try:
                _start_game()

            except:
                sleep(300)
                _start_game()

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
            index = 0
            while index < len(checkboxes):
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

                    index += 1

                except Exception as e:
                    logger.warning(f"Не удалось взаимодействовать с CheckBox {index}: {e}\nПерезапускаю PURPLE")
                    self._restart_purple_and_go_to_multi_accounts()
                    index = 0

        try:
            self.app.child_window(auto_id="CloseButton", control_type="Button").wrapper_object().click_input()
        except:
            logger.warning("")
            pass

    def _restart_purple_and_go_to_multi_accounts(self):
        logger.info('Перезапуск Purple')
        self._kill_purple()

        self._get_purple()

        self._open_multi_account()
        self._open_multi_account_settings()

    def _kill_purple(self):
        sleep(1)
        self.app.child_window(auto_id="PART_Close", control_type="Button").click_input()
        sleep(2)

        self.app.child_window(title="Close", control_type="Text").click_input()
        sleep(7)

    def _checking_checkboxes(self, checkboxes):
        return bool(checkboxes)

    def _up_purple(self):
        sleep(85)
        run_lineage_windows.switch_windows()

        try:
            self.app.set_focus()
            self.app.minimize()
            self.app.maximize()
            self.app.restore()
            sleep(1)
        except (ElementNotFoundError, TimeoutError) as e:
            logger.warning(f"Не удалось выполнить операцию на окне PURPLE: {e}")
            self.launch_purple()

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
