import pygame
from .button import Button


class SubmitName(Button):


    def __init__(self, x, y, wid, hei, f, t, cli):
        super().__init__(x, y, wid, hei, f, t)
        self.client = cli

