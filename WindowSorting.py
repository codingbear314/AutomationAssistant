from pywinauto import Desktop

XresolutionA = 2256
YresolutionA = 1504

def get_window_info():
    # Get all top-level windows
    desktop = Desktop(backend="win32")
    windows = desktop.windows()

    window_info_list = []

    # Iterate over the windows to get the required information
    for depth, window in enumerate(windows):
        if window.is_visible() and window.window_text().strip() and window.window_text() not in ["Program Manager", "Start", "Windows 입력 환경"]:
            name = window.window_text()
            window_id = window.handle
            rect = window.rectangle()
            coordinates = (rect.left, rect.top)
            size = (rect.width(), rect.height())
            window_info_list.append((name, window_id, coordinates, size, depth + 1))

    # Sort the list by depth (which is the last element in the tuple)
    window_info_list.sort(key=lambda x: x[4])

    return window_info_list

# Get and sort window information
windows_info = get_window_info()

# Print the sorted window information
for info in windows_info:
    print(info)
