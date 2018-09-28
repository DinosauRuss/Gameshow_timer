
'''
Master timer
Optional keys to add/subtract time
Can temporarily speed up time and return to normal speed,
    followed by reset to original countdown
Command line arg can change total time
'''

import os
import threading
from timer_class import *


class Master_Timer(Timer):
    def __init__(self, screen, seconds=10800):
        Timer.__init__(self, screen, seconds)
        
        self.heroButton_state = False
        self.undoButton_state = False
        self.endButton_state = False
        self.specialTimeAdjust_state = True
    
    def draw(self):
        
         # Change background color
        if self.time_remaining <= 0:
            self.bg_color = COLORS['SCENIC_BLUE']
        else:
            self.bg_color = COLORS['BLACK']
            
        self.screen.fill(self.bg_color)
        
        self.drawText(self.timer(), FONTS['CLOCK_FONT'],\
            FONTS['CLOCK_SIZE'], COLORS['WHITE'],\
            self.center.centerx, self.center.centery)
        
        pg.display.flip()


def mainLoop():

    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = 'True'
    screen = pg.display.set_mode((0,0), pg.RESIZABLE)   #pg.FULLSCREEN/RESIZABLE
    pg.display.set_caption('Sugar Rush Clock')
    
    pg.mouse.set_visible(False)
    
    if len(sys.argv) == 2:
        masterTimer = Master_Timer(screen, int(sys.argv[1]))
    else:
        sugarTimer = Master_Timer(screen)
    
    masterTimer.showStartScreen(screen)
    while masterTimer.program_running:
        masterTimer.new()
    
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    try:
        mainLoop()
    except KeyboardInterrupt:
        sys.exit()       
        

