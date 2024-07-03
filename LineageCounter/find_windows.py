import win32gui


def find_windows():
    def _is_toplevel(hwnd):
        return win32gui.GetParent(hwnd) == 0 and win32gui.IsWindowVisible(hwnd)

    hwnd_list = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd) if _is_toplevel(hwnd) else None, hwnd_list)
    lst_processes = [hwnd for hwnd in hwnd_list if 'Lineage2M' in win32gui.GetWindowText(hwnd)]

    return len(lst_processes)



