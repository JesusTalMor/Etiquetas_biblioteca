import PySimpleGUI as sg

import pop_ups as pop
import string_helper as sh

"""En este modulo se almacenan las ventanas auxiliares de trabajo."""

# * Tema principal de las ventanas
sg.LOOK_AND_FEEL_TABLE["MyCreatedTheme"] = {
  "BACKGROUND": "#3016F3",
  "TEXT": "#000000",
  "INPUT": "#DEE6F7",
  "TEXT_INPUT": "#000000",
  "SCROLL": "#DEE6F7",
  "BUTTON": ("#000000", "#FFFFFF"),
  "PROGRESS": ("#DEE6F7", "#DEE6F7"),
  "BORDER": 2,
  "SLIDER_DEPTH": 0,
  "PROGRESS_DEPTH": 0,
}
sg.theme("MyCreatedTheme")

if __name__ == "__main__":
  pass