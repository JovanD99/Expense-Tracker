from os.path import exists
from spender_functions import *
import pygame
from ammount_check import *
from constants import *
from DisplayMoney_class import *
from InputNumberField_class import *
from main_scene import *
from next_scene import *
from monthly_expenditures_scene import *


"""Spender
A finanace program made to help the user keep track of their expenses.
Програм кој му овозможува на корисникот да ѓи следи своите трошоци."""

def main():
    #create the database if it doesnt exist
    if not exists("expenses.db"):
        create_database()

        
#--------------------------------------------------------------------------------
    #initialize the window
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Expense tracker")

    #create scenes and scene manager
    scenes = [MainScene(window),
              NextScene(window),
              MonthlyScene(window)]


    sceneManager = pyghelpers.SceneMgr(scenes, FRAMES_PER_SECOND)
#--------------------------------------------------------------------------------
    sceneManager.run()




#------------------------------------------------------------
if __name__ == "__main__":
    main()
