
'''
Round 3 timer
Default is 3 hours
Command line args can change total time and optional delay
Optional keys to add/subtract time
'''

import os
import threading
from timer_class import *


class Beta_Timer(Timer):
    def __init__(self, screen, seconds=10800):
        #~ super().__init__(screen, seconds)
        Timer.__init__(self, screen, seconds)
        
        self.heroButton_state = False
        self.undoButton_state = False
        self.endButton_state = False
        self.specialTimeAdjust_state = False
    
    def new(self):
        # Add delay option
        
        self.loadData()
        pg.mixer.init()
        
        if len(sys.argv) == 3:
            #~ pg.time.delay(int(sys.argv[2])*1000)
            #~ time.sleep(int(sys.argv[2]))
            self.delayStartTime = pg.time.get_ticks()
            self.delay(int(sys.argv[2]))
        
        self.intro()
        
        # Start ssh input thread after intro
        t2 = threading.Thread(target=self.key_input)
        t2.setDaemon(True)
        t2.start()
            
        self.startTime = pg.time.get_ticks()
        self.original_startTime = self.startTime
        
        self.run()       
    
    def draw(self):
        
         # Change background color
        if self.time_remaining <= 0:
            self.bg_color = COLORS['SCENIC_BLUE']
        else:
            self.bg_color = COLORS['BLACK']
            
        self.screen.fill(self.bg_color)
        
        self.drawText(self.timer(), FONTS['CLOCK_FONT'],\
            FONTS['CLOCK_SIZE'], COLORS['PINK'],\
            self.center.centerx, self.center.centery+75)
        
        self.drawText('ROUND 3',\
            FONTS['ROUND_FONT'], FONTS['ROUND_SIZE'], COLORS['WHITE'],\
            self.center.centerx, self.center.centery-150)
        
        pg.display.flip()

    def delay(self, seconds):
        while True:
            now = pg.time.get_ticks()
            pg.time.wait(100) # Save processor while waiting
            
            elapsed = (now - self.delayStartTime)
            if  elapsed >= int(seconds)*1000:
                break


def mainLoop():

    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = 'True'
    screen = pg.display.set_mode((0,0), pg.RESIZABLE)   #pg.FULLSCREEN/RESIZABLE
    pg.display.set_caption('Sugar Rush Clock')
    
    pg.mouse.set_visible(False)
    
    if len(sys.argv) >= 2:
        round3Timer = Beta_Timer(screen, int(sys.argv[1]))
    else:
        round3Timer = Beta_Timer(screen)
    
    round3Timer.showStartScreen(screen)
    while round3Timer.program_running:
        round3Timer.new()
    
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    try:
        mainLoop()
        
    except KeyboardInterrupt:
        sys.exit()       
        

