
import pygame as pg
import threading
import time
import sys

COLORS = {'WHITE' : (255,255,255),
          'BLACK' : (0,0,0),
          'RED' : (255,0,0),
          'GREEN' : (0,255,0),
          'BLUE'  : (0,0,255),
          'GREY' : (150, 150, 150),
          'PURPLE' : (102,0, 204),
          'PINK' : (204,0, 204),
          'SCENIC_BLUE' : (0, 153, 153)}

FONTS = {'TEXT_FONT' : 'RursusCompactMono.ttf',
         'CLOCK_FONT' : 'd7.ttf',
         'CLOCK_SIZE' : 200,
         'ROUND_FONT' : 'Eurostile.ttf',
         'ROUND_SIZE' : 200}

KEYS = {'START' : ['start', pg.K_s],
        'HERO' : ['h', pg.K_h],
        'UNDO' : ['u', pg.K_u],
        'END' : ['g', pg.K_g],
        'ESCAPE' : ['esc', pg.K_ESCAPE],
        'ADD' : ['z', pg.K_z],
        'SUBTRACT' : ['x', pg.K_x],
        'SPEED' : ['k', pg.K_k],
        'SLOW' : ['l', pg.K_l],
        'RESET' : ['p', pg.K_p]}

FPS = 30


class Timer():
    def __init__(self, screen, seconds=10800):       
        self.clock = pg.time.Clock()
        self.screen = screen
        self.center = self.screen.get_rect()
        self.bg_color = COLORS['BLACK']
        
        self.program_running = True
        self.waiting = True
        
        self.countdownTime = int(seconds)
        self.original_countdownTime = int(seconds)
        self.time_remaining = 0
        self.frozen_time = 0
        self.heroButton = 0
        
        self.frozen_flag = False
        self.heroButton_state = True
        self.undoButton_state = False
        self.endButton_state = True
        self.changeTime_state = True
        self.specialTimeAdjust_state = False
        
        self.multiplier = 1000
        self.end_counter = 0
        
        self.beep = ''
        self.long_beep = ''
        
    def new(self):
        self.loadData()
        pg.mixer.init()

        self.intro()
        
        # Start ssh input thread after intro
        keyThread = threading.Thread(target=self.key_input)
        keyThread.setDaemon(True)
        keyThread.start()
        
        self.startTime = pg.time.get_ticks()
        self.original_startTime = self.startTime
        
        self.run()       
        
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            pg.time.wait(15)    # Save processor
        
    def events(self):

        for event in pg.event.get():
            
            if event.type == pg.VIDEORESIZE:
                self.screen = (pg.display.set_mode((event.dict['size']), pg.RESIZABLE))
                self.center = self.screen.get_rect()

            
            if event.type == pg.QUIT:
                self.playing = False
                self.program_running = False
                
            if event.type == pg.KEYDOWN:
                
                if event.key == KEYS['ESCAPE'][1]:
                    # Quit
                    print('Exiting...')
                    self.playing = False
                    self.program_running = False
                    
                if event.key == KEYS['HERO'][1] or event.key == pg.K_KP2:
                    # Hero button key
                    # Changes round 1 - round 2 - frozen time
                    if self.heroButton_state == True:
                        self.undoButton_state = True
                        self.heroButton += 1
                        if self.heroButton >= 2:
                            self.heroButton = 2
                            self.frozen_flag = True
                            self.frozen_time = self.time_remaining
                            self.heroButton_state = False
                            print('Time is frozen')
                        print('Button is now at: ', self.heroButton)

                if event.key == KEYS['UNDO'][1]:
                    # Undo hero push
                    if self.undoButton_state == True:
                        self.heroButton -= 1
                        if self.heroButton <= 1:
                            self.heroButton_state = True
                            self.frozen_flag = False
                        if self.heroButton <= 0:
                            self.heroButton = 0
                            self.undoButton_state = False
                            
                        print('Undo, Button is now at: ', self.heroButton)
                
                if event.key == KEYS['ADD'][1]:
                    # Add 10 minutes to remaining time
                    if self.changeTime_state == True:
                        self.countdownTime += 600
                
                if event.key == KEYS['SUBTRACT'][1]:
                    # Remove 10 minutes from remaining time
                    if self.changeTime_state == True:
                        self.countdownTime -= 600
                
                if event.key == KEYS['END'][1]:
                    # 'self-destruct' key
                    # Run down the time quickly
                    if self.endButton_state == True:
                        if self.frozen_flag == True:
                            self.startTime = pg.time.get_ticks()
                            self.countdownTime = self.frozen_time
                            self.time_remaining = self.frozen_time
                            self.frozen_flag = False
                        else:
                            self.countdownTime = self.time_remaining
                            self.startTime = pg.time.get_ticks()
    
                        self.end_counter += 1
                        if self.end_counter == 1:
                            self.multiplier = 25
                        elif self.end_counter == 2:
                            self.multiplier = 5
                        else:
                            self.multiplier = 3
                            self.endButton_state = False
                        print('End key, multiplier is now at: ', self.multiplier)
                        
                        # Disable buttons after self-destruct
                        self.heroButton_state = False
                        self.undoButton_state = False
                        self.changeTime_state = False
                    
                if event.key == KEYS['SPEED'][1]:
                    # Speed up timer
                    
                    if self.specialTimeAdjust_state == True:
                        self.countdownTime = self.time_remaining
                        self.startTime = pg.time.get_ticks()
                        
                        self.multiplier = 10
                    
                if event.key == KEYS['SLOW'][1]:
                    # Slow timer to normal speed
                    
                    if self.specialTimeAdjust_state == True:
                        self.countdownTime = self.time_remaining
                        self.startTime = pg.time.get_ticks()
                        
                        self.multiplier = 1000
                    
                if event.key == KEYS['RESET'][1]:
                    # Reset timer to where it would be
                    # without changes
                    if self.specialTimeAdjust_state == True:
                        self.countdownTime = self.original_countdownTime
                        self.startTime = self.original_startTime
    
    def key_input(self):
    # Accept keypresses from terminal/ssh
        while True:
            #~ key = str(input('enter a key>> '))
            key = str(input('enter a key>> '))
            
            if key:
                for i in KEYS.values():
                    for j in i:
                        if key == j:
                            my_event = pg.event.Event(pg.KEYDOWN, {'key': i[1]})
                            pg.event.post(my_event)
                
                if key == 'size':
                    print(pg.display.get_surface().get_size())
            
            time.sleep(.25)
            print('\n')
                  
    def update(self):
        # If clock stopped, pause program to save processor
        if self.time_remaining == 0 or self.frozen_flag == True:
            pg.time.wait(50)
        
    def draw(self):
        # Draw stuff to the screen
        pass
        
    def drawText(self, text, fontName, size, color, x, y):
        # Draw some text to the screen
        font = pg.font.Font(fontName, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surface, text_rect)

    def drawText_topleft(self, text, fontName, size, color, x, y):
        # Draw some text to the screen at fixed location
        font = pg.font.Font(fontName, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def loadData(self):
        pass
    
    def waitForEsc(self):
        pressed = pg.key.get_pressed()
        if pressed[pg.K_ESCAPE]:
            self.playing = False
            self.program_running = False
            self.waiting = False
    
    def intro(self):

        self.screen.fill(self.bg_color)
        center_point = self.center
        
        # Countdown with beep sounds
        j = 3
        pg.mixer.music.load('beep-short.wav')
        for i in range(3):
            self.screen.fill(self.bg_color)
            self.drawText('{}'.format(j), FONTS['CLOCK_FONT'], 600,\
                COLORS['WHITE'], center_point.centerx, center_point.centery)
                
            pg.display.flip()
            pg.mixer.music.play()
            j -= 1
            time.sleep(1)
        
        pg.mixer.music.load('beep-long.wav')    
        pg.mixer.music.play()
        
    def showStartScreen(self, surface):
        
        self.screen.fill(self.bg_color)
        
        try:
            # Try loading first logo
            frame = pg.image.load('sr_logo.jpg').convert_alpha()
            frame = pg.transform.scale(frame, (1280, 800))
            frame_rect = frame.get_rect()
            frame_rect.center = (self.center.centerx, self.center.centery)
            self.screen.blit(frame, (frame_rect))
            
        except Exception:
            # If first logo fails try second logo
            try:
                frame = pg.image.load('logo.jpg').convert_alpha()
                frame = pg.transform.scale(frame, (1400, 1100))
                frame_rect = frame.get_rect()
                frame_rect.center = (self.center.centerx, self.center.centery)
                self.screen.blit(frame, (frame_rect))
            except Exception:
                pass
            
        pg.display.flip()
        
        self.waitForStart()        
    
    def showEndScreen(self, surface):
        pass
        
    def waitForStart(self):
        while self.waiting:
            #~ # Use for in-window starting
            for event in pg.event.get():                
                if event.type == pg.KEYUP:
                    if event.key == KEYS['START'][1]:
                        self.waiting = False
            
            # Use for terminal/ssh starting
            #~ thing = input('Waiting for key to start (esc):    ')
            
            thing = input('Waiting for key to start (esc):    ')
            if thing == KEYS['START'][0]:
                self.waiting = False
            elif thing == KEYS['ESCAPE'][0]:
                print('Exiting...')
                pg.quit()
                sys.exit()
    
    def timer(self):
        now = pg.time.get_ticks()
        
        # self.multiplier=1000 are seconds
        elapsed_time = int((now - self.startTime)/self.multiplier)
        self.time_remaining = int(self.countdownTime - elapsed_time)
        
        minutes, seconds = divmod(self.time_remaining, 60)
        hours, minutes = divmod(minutes, 60)
        
        f_minutes, f_seconds = divmod(self.frozen_time, 60)
        f_hours, f_minutes = divmod(f_minutes, 60)
        
        if self.frozen_flag == False:
            if self.time_remaining >= 0:
                return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
            else:
                self.changeTime_state = False
                return '{:02d}:{:02d}:{:02d}'.format(0, 0, 0)
                
        else:
            self.time_remaining = 60000
            return '{:02d}:{:02d}:{:02d}'.format(f_hours, f_minutes, f_seconds)

        

