import pygame
from pygame.locals import *
import pygwidgets


CANCELLED_TAB = -1
KEY_REPEAT_DELAY = 500  # ms before starting to repeat
KEY_REPEAT_RATE = 50  # ms between repeating keys
BLACK = (0,0,0)
WHITE = (255,255,255)
LEGAL_KEYS = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_HOME, pygame.K_END, 
pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_KP_ENTER]

NUMBERS = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]


class InputNumber(pygwidgets.InputText):
    """A class that creates input text fields that 
    accept only numbers"""

    def __init__(self, window, loc, value='', fontName=None, fontSize=24, width=200, 
    textColor=BLACK, backgroundColor=WHITE, focusColor=BLACK, initialFocus=False, 
    nickname=None, callBack=None, mask=None, keepFocusOnSubmit=False, 
    allowFloatingNumber=True, allowNegativeNumber=True):

        super().__init__(window, loc, value, fontName, fontSize, width, textColor, 
        backgroundColor, focusColor, initialFocus, nickname, callBack, mask, 
        keepFocusOnSubmit)

        self.allowFloatingNumber = allowFloatingNumber
        self.allowNegativeNumber = allowNegativeNumber


    def handleEvent(self, event):
        """checks to see if the key pressed is a number and then passes 
        the result to the same method of the super class"""
        if event.type == pygame.K_DOWN:
            allowableKey = event.key in LEGAL_KEYS
            if not allowableKey:
               return False
            if event.unicode == '-':
                if not self.allowNegativeNumber:
                    return False
                if self.cursorPosition > 0:
                    return False
                if '-' in self.text:
                    return False
            if event.unicode == '.':
                if not self.allowFloatingNumber:
                    return False
                if '.' in self.text:
                    return False

        if not self.isEnabled:
            return False
        if not self.visible:
            return False

        if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):  # user clicked
            theX, theY = event.pos

            if self.imageRect.collidepoint(theX, theY):
                if not self.focus:
                    self.focus = True   # give this field focus
                    pygame.key.set_repeat(
                        KEY_REPEAT_DELAY, KEY_REPEAT_RATE)
                else:
                    # Field already has focus, must position the cursor where the user clicked
                    nPixelsFromLeft = theX - self.loc[0]
                    nChars = len(self.text)

                    lastCharOffset = self.font.size(self.text)[0]
                    if nPixelsFromLeft >= lastCharOffset:
                        self.cursorPosition = nChars
                    else:
                        for thisCharNum in range(0, nChars):
                            thisCharOffset = self.font.size(
                                self.text[:thisCharNum])[0]
                            if thisCharOffset >= nPixelsFromLeft:
                                self.cursorPosition = thisCharNum  # Found the proper position for the cursor
                                break
                    self.cursorVisible = True  # Show the cursor at the click point

            else:
                self.focus = False
            return False  # means:  handled click, nothing for client to do

        if not self.focus:  # if this field does not have focus, don't do anything
            return False

        if event.type == pygame.KEYDOWN:
            currentKey = event.key

            if currentKey in (pygame.K_RETURN, pygame.K_KP_ENTER):
                # defaults to False - lose focus with Enter/Return
                self.focus = self.keepFocusOnSubmit
                if not self.focus:
                    pygame.key.set_repeat(0)  # turn off repeating characters

                self._updateImage()

                if self.callBack is not None:
                    self.callBack(self.nickname)

                # User is done typing, return True to signal that text is available (via a call to getValue)
                return True

            elif currentKey == CANCELLED_TAB:
                # See code below setting up CANCELLED_TAB
                # If we get a CANCELLED_TAB as the current key, ignore it, already shifted focus
                pass

            elif currentKey == pygame.K_BACKSPACE:
                self.text = self.text[:max(self.cursorPosition - 1, 0)] + \
                    self.text[self.cursorPosition:]

                # Subtract one from cursor_pos, but do not go below zero:
                self.cursorPosition = max(self.cursorPosition - 1, 0)
                self._updateImage()

            elif currentKey == pygame.K_DELETE:  # forward delete key
                self.text = self.text[:self.cursorPosition] + \
                    self.text[self.cursorPosition + 1:]
                self._updateImage()

            elif currentKey == pygame.K_RIGHT:
                if self.cursorPosition < len(self.text):
                    self.cursorPosition = self.cursorPosition + 1

            elif currentKey == pygame.K_LEFT:
                if self.cursorPosition > 0:
                    self.cursorPosition = self.cursorPosition - 1

            elif currentKey == pygame.K_END:
                self.cursorPosition = len(self.text)

            elif currentKey == pygame.K_HOME:
                self.cursorPosition = 0

            elif currentKey in (pygame.K_UP, pygame.K_DOWN):
                pass

            elif currentKey == pygame.K_TAB:
                if self.oNextFieldOnTab is not None:  # Move focus to a different field
                    self.removeFocus()
                    self.oNextFieldOnTab.giveFocus()

                    # The TAB key is sent to all fields.  If this field is *before* the field
                    # gaining focus, we cannot send the TAB to that field
                    # So, we change the key to something that will be ignored when it is
                    # received in the target field
                    event.key = CANCELLED_TAB

            else:  # standard key
                # If no special key is pressed, add unicode of key to input_string
                if event.unicode not in "0123456789":
                    unicodeOfKey = ""
                else:
                    unicodeOfKey = event.unicode  # remember for potential repeating key

                self.text = self.text[:self.cursorPosition] + \
                    unicodeOfKey + self.text[self.cursorPosition:]
                self.cursorPosition = self.cursorPosition + len(unicodeOfKey)
                self._updateImage()

        return False  # means: handled key, nothing for client code to do


    def getValue(self):
        """returns an integer or a float value"""
        userString =  super().getValue()
        try:
            if userString == '':
                userString = "0"
            if self.allowFloatingNumber:
                returnValue = float(userString)
            else:
                returnValue = int(userString)
        except ValueError:
            raise ValueError("Entry is not a number")
        
        return returnValue
