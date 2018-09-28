
'''
Scroll from $0 to $10000
Used when winner is announced
'''

import os
from timer_class import *

class MoneyScroll(Timer):
    
    def __init__(self, screen):
        Timer.__init__(self, screen)
        
        self.count = 1
                  
    def update(self):
        # If clock stopped, pause program to save processor
        if self.count >= 10000:
            pg.time.wait(50)
    
    def intro(self):
        pass
        
    def draw(self):
        self.screen.fill(self.bg_color)
        
        self.drawText(self.moneyTimer(), FONTS['ROUND_FONT'],\
            FONTS['ROUND_SIZE'], COLORS['WHITE'],\
            self.center.centerx, self.center.centery)
        
        pg.display.flip()
    
    def moneyTimer(self):
        if self.count == 0:
            pg.time.delay(3000)
        if self.count < 10000:
            self.count += 123.43
        else:
            self.count = 10000
            pg.time.delay(3000)
            self.count = 0
            
        if self.count >= 10000:
            return '${:09,.2f}'.format(10000)
        elif self.count == 0:
            return '${:09,.2f}'.format(self.count)
        else:
            return '${:08,.2f}'.format(self.count)


def mainLoop():

    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = 'True'
    screen = pg.display.set_mode((0,0), pg.RESIZABLE)   #pg.FULLSCREEN/RESIZABLE
    pg.display.set_caption('Sugar Rush Clock')
    
    pg.mouse.set_visible(False)
    
    if len(sys.argv) == 2:
        moneyTimer = MoneyScroll(screen, int(sys.argv[1]))
    else:
        moneyTimer = MoneyScroll(screen)
    
    moneyTimer.showStartScreen(screen)
    while moneyTimer.program_running:
        moneyTimer.new()
    
    pg.quit()
    sys.exit()

if __name__ == '__main__':
    try:
        mainLoop()
    except KeyboardInterrupt:
        sys.exit()       
        

