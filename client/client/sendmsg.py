import pygame
from .button import Button


class SendMsg(Button):


    def __init__(self, x, y, wid, hei, f, t, cli):
        super().__init__(x, y, wid, hei, f, t)
        self.client = cli


    def action(self, event):
        self.confirm_send()


    def confirm_send(self):
        text = self.client.msg_input.text

        if text != '':
            self.client.send_message(text)
            self.client.msg_input.set_text('')


