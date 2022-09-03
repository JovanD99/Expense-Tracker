import pygame
from pygame.locals import *
import sys
import pygwidgets
import pyghelpers
from DisplayMoney_class import DisplayMoney
from InputNumberField_class import InputNumber
from spender_functions import *
# from ammount_check import amount_check
from constants import *



class MainScene(pyghelpers.Scene):

    background = pygame.image.load("images/money_background.jpg")
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def __init__(self, window):
        
        
        self.window = window
        self.elements = []
        self.balance = get_balance()
        self.budget = get_budget()
        #var
        title = pygwidgets.DisplayText(window, (0, 10),
        "Expense tracker", fontSize=36, width=WINDOW_WIDTH, justified="center")
        self.elements.append(title)
        #var
        self.balanceLabel = pygwidgets.DisplayText(window, (20, 70), "Your balance:", fontSize=30,
        justified="right")
        self.elements.append(self.balanceLabel)
        #var
        self.balanceDisplay = DisplayMoney(window, (260, 70), self.balance, fontSize=30,
        width=130, justified="right", currencySign="$", showCents=True,
        currencySignOnLeft=False)
        self.elements.append(self.balanceDisplay)
        #var
        self.expenceLabel = pygwidgets.DisplayText(window, (20, 140), "Enter expense:", fontSize=30,
        justified="right")
        self.elements.append(self.expenceLabel)
        #var
        self.expenceInputField = InputNumber(window, (20, 170), "", fontSize=37, width=190)
        self.elements.append(self.expenceInputField)
        #var
        self.expenceDescriptionLabel = pygwidgets.DisplayText(window, (340, 140), "Description:", fontSize=30,
        width=190, justified="left")
        self.elements.append(self.expenceDescriptionLabel)
        #var
        self.descriptionInputField = pygwidgets.InputText(window, (340, 170), "", fontSize=37,
        width=190)
        self.elements.append(self.descriptionInputField)
        #var
        self.okButton = pygwidgets.TextButton(
        window, (570, 170), "OK", height=23, fontSize=25)
        self.elements.append(self.okButton)
        #var
        self.spentLabel = pygwidgets.DisplayText(window, (20, 230), "Spent:",
        fontSize=30, justified="right")
        self.elements.append(self.spentLabel)
        #var
        self.spentDisplay = DisplayMoney(window, (70, 230), self.budget - self.balance,
        textColor=BLACK, width=130, currencySign="$",currencySignOnLeft=False, 
        showCents=True, fontSize=30, justified="right")
        self.elements.append(self.spentDisplay)
        #var
        self.newMontlhybalanceLabel = pygwidgets.DisplayText(window, (20, 280), "New monthly budget:", fontSize=30,
        justified="right")
        self.elements.append(self.newMontlhybalanceLabel)
        #var
        self.newMonthlybalanceInputField = InputNumber(window, (260, 280), fontSize=37,
        width=190)
        self.elements.append(self.newMonthlybalanceInputField)
        #var
        self.okButtonNewbalance = pygwidgets.TextButton(
            window, (490, 280), "OK", height=25)
        self.elements.append(self.okButtonNewbalance)
        #var
        self.oDatePromptLabel = pygwidgets.InputText(
            window, (20, 350), "dd/mm/yyyy", fontSize=37)
        self.elements.append(self.oDatePromptLabel)
        #var
        self.oShowButtom = pygwidgets.TextButton(
            window, (240, 350), "Show", fontSize=24)
        self.elements.append(self.oShowButtom)
        #var
        self.oMonthYear = pygwidgets.InputText(
            window, (20, 420), "mm/yyyy", fontSize=37)
        self.elements.append(self.oMonthYear)
        #var
        self.oShowButtom2 = pygwidgets.TextButton(
            window, (240, 420), "Show", fontSize=24)
        self.elements.append(self.oShowButtom2)
    
    
    def getSceneKey(self):
        return MAIN_SCENE

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if event.type == pygame.QUIT:
                pygame.QUIT
                sys.exit()

            if self.expenceInputField.handleEvent(event) or self.okButton.handleEvent(event)\
            or self.descriptionInputField.handleEvent(event):

                self.expense = self.expenceInputField.getValue()
                self.description = self.descriptionInputField.getValue()
                self.balance -= self.expense
                enter_expense(self.expense, self.description)
                self.spent = self.budget - self.balance
                self.spentDisplay.setValue(self.spent)
                self.balanceDisplay.setValue(self.balance)
                self.expenceInputField.setValue("")
                self.descriptionInputField.setValue("")
                

            if (self.newMonthlybalanceInputField.handleEvent(event) or self.okButtonNewbalance.handleEvent(event)) and self.newMonthlybalanceInputField.getValue() != 0:
                self.balance = self.newMonthlybalanceInputField.getValue()
                self.budget = self.newMonthlybalanceInputField.getValue()
                self.balanceDisplay.setValue(self.balance)
                self.newMonthlybalanceInputField.setValue("")
                self.spentDisplay.setValue(0)
                enter_new_budget(self.budget)

            if self.oDatePromptLabel.handleEvent(event) or self.oShowButtom.handleEvent(event):
                date = self.oDatePromptLabel.getValue().strip()
                self.goToScene(NEXT_SCENE, date)

            if self.oMonthYear.handleEvent(event) or self.oShowButtom2.handleEvent(event):
                date = self.oMonthYear.getValue().strip()
                self.goToScene(MONTHLY_SCENE, date)

    def draw(self):
        self.window.blit(MainScene.background, (0,0))
        for el in self.elements:
            el.draw()

    def receive(self, receiveID, data):
        pass

    def respond(self, requestID):
        if requestID == GET_DATA:
            return 'Here is data from scene A'

    def leave(self):
        pass
        
        
    
    
        
