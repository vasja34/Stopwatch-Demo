from time import time

import PySimpleGUI as sg

cross_img = b"iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAACXBIWXMAAAsSAAALEgHS3X78AAAARUlEQVQYlWP4////hP///wv8//+fAQcGyU2AMRbgUAyXwxDApgjEx6obm0ZsVi2DYhSnMDEQC0i1mijPEB08hAP8//8JALwsGfAL5j7MAAAAAElFTkSuQmCC"


def create_window():
    """
        It creates a window of size 300x300 pixels with a few elements in it.
        The window has no titlebar and has a button called "Start" and a button called "Lap".
        The "Lap" button is not visible.

    :return: A window object
    """
    sg.theme("black")
    layout = [
        [sg.Push(), sg.Image(cross_img, pad=0, enable_events=True, key="-CLOSE-")],
        [sg.VPush()],
        [sg.Text("", font="Young 50", key="-TIME-")],
        [
            sg.Button(
                "Start",
                button_color=("#FFFFFF", "#FF0000"),
                border_width=0,
                key="-START_STOP-",
            ),
            sg.Button(
                "Lap",
                button_color=("#FFFFFF", "#FF0000"),
                border_width=0,
                key="-LAP-",
                visible=False,
            ),
        ],
        [sg.Column([[]], key="-LAPS-")],
        [sg.VPush()],
    ]

    return sg.Window(
        "Stopwatch",
        layout,
        size=(300, 300),
        no_titlebar=True,
        element_justification="center",
    )


window = create_window()
start_time = 0
active = False
lap_amount = 1

while True:
    event, values = window.read(timeout=10)
    if event in (sg.WIN_CLOSED, "-CLOSE-"):
        break

    if event == "-START_STOP-":
        if active:
            # from active to stop
            active = False
            window["-START_STOP-"].update("Reset")
            window["-LAP-"].update(visible=False)
        elif start_time > 0:
            window.close()
            window = create_window()
            start_time = 0
            lap_amount = 1
        else:
            start_time = time()
            active = True
            window["-START_STOP-"].update("Stop")
            window["-LAP-"].update(visible=True)

    if active:
        elapsed_time = round(time() - start_time, 1)
        window["-TIME-"].update(elapsed_time)

    if event == "-LAP-":
        window.extend_layout(
            window["-LAPS-"],
            [[sg.Text(lap_amount), sg.VSeparator(), sg.Text(elapsed_time)]],
        )
        lap_amount += 1

window.close()
