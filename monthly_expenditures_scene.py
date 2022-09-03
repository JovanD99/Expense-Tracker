import pygame
from pygame.locals import *
import sys
import pygwidgets
import pyghelpers
from DisplayMoney_class import DisplayMoney
from InputNumberField_class import InputNumber
from spender_functions import *
from constants import *


class MonthlyScene(pyghelpers.Scene):

    background = pygame.image.load("images/money_background.jpg")
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.elements = []
        self.changing_elements = []
        self.sum = pygwidgets.DisplayText(
            window, (30, WINDOW_HEIGHT-70), "Вкупно: ", fontSize=34)
        self.elements.append(self.sum)
        #v
        self. backButton = pygwidgets.TextButton(
            window, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 70), "Назад", fontSize=34, )
        self.elements.append(self.backButton)
        #v
        self.panel = Rect(0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100)
        #v

    def getSceneKey(self):
        return MONTHLY_SCENE

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()

            if self.backButton.handleEvent(event):
                self.goToScene(MAIN_SCENE)

    def draw(self):
        self.window.blit(MonthlyScene.background, (0,0))
        # if not self.noExpenses:
        #     pygame.draw.rect(self.window, (80, 80, 80), self.panel)
        for el in self.elements:
            el.draw()
        for el in self.changing_elements:
            el.draw()

    def receive(self, receiveID, data):
        pass

    def respond(self, requestID):
        if requestID == GET_DATA:
            return 'Here is data from NextScene'

    def enter(self, date):
        """data is a tupple, at index 0 there is a list of expenses and dates 
        from the current month, at index 1 is the input provided by the user"""
        self.noExpenses = False
        self.dateDisplay = pygwidgets.DisplayText(self.window, (30, 30), fontSize=50,
        value=f"Датум: {date}")
        self.changing_elements.append(self.dateDisplay)
        summ = 0
        entries = get_entries_on_month(date)

        if entries == None or len(entries) == 0:
            self.noExpenses = True
            entry = pygwidgets.DisplayText(self.window, (30, 160), "Во овој месец нема никакви трошоци", fontSize=34)
            self.changing_elements.append(entry)
            self.sum.hide()
        else:
            self.date = date
            y_pos = 160
            for tupple in entries:
                entry = pygwidgets.DisplayText(self.window, (30, y_pos), f"{tupple[2]}.{tupple[3]}.{tupple[4]}:     {tupple[0]} денари",
                fontSize=34, width=WINDOW_WIDTH)
                self.changing_elements.append(entry)
                y_pos += 35
                summ += tupple[0]

            self.sum.show()
            self.sum.setValue(f"Вкупно: {summ} денари")

    def leave(self):
        self.changing_elements = []
        
