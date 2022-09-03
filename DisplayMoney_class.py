import string
from pygame.locals import *
import pygwidgets
from ammount_check import amount_check
import re

BLACK = (0,0,0)

class DisplayMoney(pygwidgets.DisplayText):
    """This class formats the display text into 'money' form with 
    a currency sign on the side and comma separators"""

    def __init__(self, window, loc=..., value='', fontName=None, fontSize=18, width=None, 
    height=None, textColor=BLACK, backgroundColor=None, justified='left', nickname=None, 
    currencySign='$', currencySignOnLeft = True, showCents = True):

        self.currencySign = currencySign
        self.currencySignOnLeft = currencySignOnLeft
        self.showCents = showCents
        if value is None:
            value = 0.00
        super().__init__(window, loc, value, fontName, fontSize, width,
            height, textColor, backgroundColor, justified, nickname)
        
    def setValue(self, money):
        money = str(money)
        moeny = money.strip()
        money = re.sub(f"[,]+", "", money)
        if money == '':
            money = "0.00"
        money = float(money)
        if self.showCents:
            money = "{:,.2f}".format(money)
        else:
            money = "{:,.0f}".format(money)
        if self.currencySignOnLeft:
            money = self.currencySign + money
        else:
            money = money + self.currencySign 
        super().setValue(money)
