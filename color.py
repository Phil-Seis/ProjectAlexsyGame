""""
CMSC 495 7384 Capstone in Computer Science (2248)
University of Maryland Global Campus

Group 3: Ronald Parra De Jesus, Anthony Petrowich, Colton Purdy, Kelvin Rubio-Amaya, Asher Russell, Philip Seisman
and Julian Sotelo
Professor Davis

Project File: color.py
File Description: Stores color values for every piece and grid.
"""

class Color:
    bg = (3, 18, 33)
    cyan = (0,240,240)
    blue = (0,0,240)
    orange = (221,164,34)
    yellow = (241, 239, 47)
    green = (138,234,40)
    purple = (136,44,237)
    red = (207,54,22)

    @classmethod
    def get_color(cls):
        """Returns list of every initialized color."""
        return [cls.bg,cls.cyan,cls.blue,cls.orange,cls.yellow,cls.green,cls.purple,cls.red]
