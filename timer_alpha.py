
'''
 Rounds 1 & 2 timer
 Hero button changes round and freezes time
 Change start time with command line arg
 Optional keys for hero button, undo, and fast scroll to zero
'''

import os
from timer_class import *


class Alpha_Timer(Timer):
    def __init__(self, screen, seconds=10800):
        Timer.__init__(self, screen, seconds)
        
        self.specialTimeAdjust_state = False
    
    def draw(self):
        
         # Change background color
        if self.time_remaining <= 0:
            self.bg_color = COLORS['SCENIC_BLUE']
        else:
            self.bg_color = COLORS['BLACK']
        
        text_colors = [COLORS['WHITE'], COLORS['PURPLE'], COLORS['PINK']]
            
        self.screen.fill(self.bg_color)
        
        self.drawText(self.timer(), FONTS['CLOCK_FONT'],\
            FONTS['CLOCK_SIZE'], text_colors[self.heroButton],\
            self.center.centerx, self.center.centery+75)
        
        self.drawText('ROUND {}'.format(self.heroButton+1 if self.heroButton <=1 else 2),\
            FONTS['ROUND_FONT'], FONTS['ROUND_SIZE'], COLORS['WHITE'],\
            self.center.centerx, self.center.centery-150)
        
        pg.display.flip()


def mainLoop():

    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = 'True'
    screen = pg.display.set_mode((0,0), pg.RESIZABLE)   #pg.FULLSCREEN/RESIZABLE
    pg.display.set_caption('Sugar Rush Clock')
    
    pg.mouse.set_visible(False)
    
    if len(sys.argv) == 2:
        round1Timer = Alpha_Timer(screen, sys.argv[1])
    else:
        round1Timer = Alpha_Timer(screen)
    
    round1Timer.showStartScreen(screen)
    while round1Timer.program_running:
        round1Timer.new()
    
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    try:
        mainLoop()
    except KeyboardInterrupt:
        sys.exit()       
        

