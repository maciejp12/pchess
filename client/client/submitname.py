import pygame
from .button import Button


class SubmitName(Button):


    def __init__(self, x, y, wid, hei, f, t, cli):
        super().__init__(x, y, wid, hei, f, t)
        self.client = cli


    def action(self, event):
        new_name = self.client.name_input.text
        if new_name == '':
            #TODO handle name errors (also too long name)
            return

        self.client.init_connection(new_name)
