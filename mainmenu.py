import pygame
import pygame_menu
from main import *


class MainMenu():
    def __init__(self, surface):
        self.menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

        self.textinpt = self.menu.add.text_input('Name :', default='John Doe')
        self.sizeSelecor = self.menu.add.selector('Size :', [('Large', 1), ('Medium', 2),('Small', 3)], onchange=set_size)
        self.playButton = self.menu.add.button('Select Difficulty', self.next_screen)
        self.quitButton = self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(surface)
    
    def next_screen(self):
        #also needs to update size of the screen

        self.menu.remove_widget(self.sizeSelecor)
        self.menu.remove_widget(self.textinpt)
        self.menu.remove_widget(self.playButton)
        self.menu.remove_widget(self.quitButton)
        self.easyButton = self.menu.add.button('Easy', select_difficulty, 'Easy')
        self.mediumButton = self.menu.add.button('Medium', select_difficulty, 'Medium')
        self.hardButton = self.menu.add.button('Hard', select_difficulty, 'Hard')

#need to add a map size menu

def select_difficulty(difficulty):
    game.run(difficulty)

def set_size(value, size):
    return value, size

if __name__ == "__main__":
    game = Game()   
    menu_1 = MainMenu(game.screen)

