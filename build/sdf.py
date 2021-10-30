import pygame #needed for all pygame tools
import math #needed for equations for movement
import os #For loading files

class player(): #player class
    def __init__(self,x,y): #initailisation methoid
        self.x = x #x postion
        self.y = y #y position
        self.angle = 0 #diection the ship is faceing
        self.HP = 100 #Heath points
        
        self.speed_change = "none" #stores if spped needs to be changes
        self.speed_added = 0 #stores the ammont that the ship has sped up by so far
        self.sail_trimed = False #stores is the spite has been changed or not
        self.full_speed = False #stores if the ship has reached full speed yet
        self.stopped = True #stores if the ship has stopped
        self.knocked = False #stores if the ship is currectly being knocked back
        player.wrecked = False #flag to show if ship has sunk
        
        self.ship = [pygame.image.load(os.path.join("data","sprites","brittish ship","brittish boat stoped.png")).convert_alpha(),pygame.image.load(os.path.join("data","sprites","brittish ship", "brittish boat half.png")).convert_alpha(),pygame.image.load(os.path.join("data","sprites","brittish ship", "brittish boat full.png")).convert_alpha(),pygame.image.load(os.path.join("data","sprites","wreck.png")).convert_alpha()] #loads in player sprite
        self.state = 0
        self.rect = self.ship[self.state].get_rect(left=self.x,top=self.y) #rect for ship
        self.mask = pygame.mask.from_surface(self.ship[self.state]) #mask for ship
        
        self.speed = 0 #speed of the ship (pixles moved per frame)
        self.rotate_speed = 0.05 #speed of turn (degrees per frame), set to 0.05 as that is the initial turning speed
        
        self.left_fireing = 0 #number of cannons on the left still fireing
        self.right_fireing = 0 #number of cannons on the right still fireing
        
        self.reloadingL = False #flag to show if left side is reloading
        self.reloadingR = False #same for right side
        self.reload_timerR = 0 #timer variable for right side
        self.reload_timerL= 0 #same for left side
        
        self.lose_timer = 0 #timer for lose screen
        
        
        
    def update(self): #update methoid
        
        def Speed_change(): #methoids for the player
            if self.speed_change == "up":    #if speed needs to be changed
                if self.sail_trimed == False:  #if the spitre has not already been changed it will do so
                    game.speed_change_sound.play() #plays sound effect for changeing speed
                    self.state += 1
                    self.sail_trimed = True
                if self.speed_added < 25:    #if the total ammount by which the ship will speed up has not been added
                    self.speed_added += 0.25 #more will be added
                    self.speed -= 0.25 #-ve as ship is moveing up the screen
                else:
                    self.speed_added = 0       #if ship has fully sped up, variables are reset
                    self.sail_trimed = False
                    self.speed_change = "none"
                    
                    if self.state == 2:          #changes rotate speed and variables for full speed and stoped
                        self.full_speed = True
                        self.rotate_speed = 0.3
                    elif self.state == 1:
                        self.rotate_speed = 0.5
                        self.stopped = False
                        
            
            elif self.speed_change == "down":
                if self.sail_trimed == False:
                    game.speed_change_sound.play() #plays sound effect for speed change
                    self.state -= 1
                    self.sail_trimed = True
                if self.speed_added < 25:
                    self.speed_added += 0.25
                    self.speed += 0.25
                else:
                    self.speed_added = 0
                    self.sail_trimed = False
                    self.speed_change = "none"
                    
                    if self.state == 0:
                        self.stopped = True
                        self.rotate_speed = 0.05
                    elif self.state == 1:
                        self.rotate_speed = 0.5
                        self.full_speed = False
                    
            
            elif self.speed_change == "knocked":
                if self.knocked == False:
                    self.state = 0
                    self.speed = 30
                    self.speed_added = 0
                    self.knocked = True
                if self.speed_added < 30:
                    self.speed_added += 0.25
                    self.speed -= 0.25
                else:
                    self.speed_added = 0
                    self.sail_trimed = False
                    self.speed_change = "none"
                    self.stopped = True
                    self.rotate_speed = 0.05
                    self.full_speed = False
                    self.knocked = False
        
        def Turn():
            if self.speed_change != "knocked":      #if ship has not been knocked back
                pressedkeys = pygame.key.get_pressed()   #gets keys currently being pressed
                if pressedkeys[pygame.K_a]:              # if a key is pressed, add rotate speed so it turns left
                    self.angle += self.rotate_speed
                elif pressedkeys[pygame.K_d]:            #same for d key
                    self.angle -= self.rotate_speed
                self.angle %= 360                        #angle is kept within correct rante
            
            self.sprite = game.rotate(self.ship[self.state],self.angle)  #sprte variable store the rotated sprite
        
        def Move():
            self.x += math.sin(math.radians(self.angle)) * (self.speed * game.secounds)#Adds x and y movement to x and y
            self.y += math.cos(math.radians(self.angle)) * (self.speed * game.secounds)#variables useing time-based movement
            
            self.rect.left = self.x #updates rect for the new position
            self.rect.top = self.y

            
        def Collitions(): #handles collitions
                    
            if not game.rect.colliderect(self.rect): #if player off screen
                self.x %= game.width #keep coordinates within screen range
                self.y %= game.hight
            
            self.mask = pygame.mask.from_surface(self.sprite) #update player mask
            pixle_offset = (int(game.enemy.x-self.x),int(game.enemy.y-self.y))  #update player offset from enemy
            if self.mask.overlap(game.enemy.mask,pixle_offset) and game.enemy.wrecked == False: #if player mask touching enemy mask
                self.speed_change = "knocked" #knocked back
                game.bump_sound.play() #play's bump sound
        
        def Fire():
            if self.left_fireing > 0: #if left cannons are still fireing
                self.cannonl1.run() #run each cannon ball
                self.cannonl2.run()
                self.cannonl3.run()
                self.cannonl4.run()
                
            if self.right_fireing > 0: #if right cannons are still fireing
                self.cannonr1.run() #run each cannon ball
                self.cannonr2.run()
                self.cannonr3.run()
                self.cannonr4.run()
            
            if self.reloadingL == True: #if left still realoading
                self.reload_timerL += game.secounds #increment timer
                if self.reload_timerL > 5: #if reloading for 5 secs
                    self.reload_timerL = 0 #reset timer
                    self.reloadingL = False #reset varible
                    
            if self.reloadingR == True: #same for right side
                self.reload_timerR += game.secounds
                if self.reload_timerR > 5:
                    self.reload_timerR = 0
                    self.reloadingR = False
        
        def Sunk():
            if self.wrecked == False: #if ship just been sunk
                self.wrecked = True #sets wrecked to true
                self.state = 3 #sets state so ship wreck is displayed
                game.sunk_sound.play() #plays sunk sound effect
                
            rotated = game.rotate(self.ship[self.state],self.angle) #rotates this sprite to corect poition
            game.screen.blit(rotated,(self.x,self.y)) #displays player on screen
            
            self.lose_timer += game.secounds #add seconds since last frame to timer
            if self.lose_timer > 5: # 5 secounds have passed
                self.lose_timer = 0 #reset timer
                game.gamemode = 3 #set game mode to 3 (lose)
            

        if self.HP > 0:     #calls modlues if ship is still alive
            Speed_change()
            Turn()
            Move()
            Collitions()
            Fire()
            game.screen.blit(self.sprite,(self.x,self.y)) #displays ship on screen
                
        else:              #if not still alive, only sunk methoid is needed
            Sunk()
 
class Enemy():
    def __init__(self,x,y):
        self.var = 0
        
        self.x = x #postion
        self.y = y
        self.angle = 180 #starting angle (down)
        
        self.calc_angle = 0 #angle for calculateing tatget angle
        self.target_angle = 0 #angle in which enemy needs to point
        self.angle_from_target = 0 #angle of enemy from player
        self.relitive_angle = 0 #angle if player from enemy
        self.target_point = (0,0) #point which enemy is aiming at
        self.relitave_position = (0,0) #the cordinate differences between the player and enemy
        self.range = 0 #distance to player
        
        self.speed = 0 #self explanitory
        self.rotate_speed = 0.05 #speed of rotation
        
        self.speed_change = "none" #explained in player speed change
        self.speed_added = 0
        self.sail_trimed = False
        self.full_speed = False
        self.stopped = True
        self.circleing = False #flag to show if enemy is circleing player
        
        self.HP = 100 #heath
        self.state = 0 #position if current sprite in list
        self.wrecked = False #flag to show if enemy is dead
        self.knocked = False #flag to show if enemy has been knocked back
        
        #sprite list
        self.ship = [pygame.image.load(os.path.join("data","sprites","french ship","french boat stoped.png")).convert_alpha(),pygame.image.load(os.path.join("data","sprites","french ship", "french boat half.png")).convert_alpha(),pygame.image.load(os.path.join("data","sprites","french ship", "french boat full.png")).convert_alpha(),pygame.image.load(os.path.join("data","sprites","wreck.png")).convert_alpha()]
        
        self.sprite = self.ship[self.state] #current sprite
        self.mask = pygame.mask.from_surface(self.ship[self.state]) #mask of enemy
        self.rect = self.ship[self.state].get_rect(left=self.x,top=self.y) #rect of enemy
        
        self.left_fireing = 0 #number of left cannons still fireing
        self.right_fireing = 0 #number of right cannons still fireing
        self.reloadingL = False #flag to show if left cannons are relaoding
        self.reloadingR = False #flag to show if right cannons are relaoding
        self.reload_timerR = 0 #right and left relaod timers
        self.reload_timerL= 0
        
        self.lose_timer = 0 #timer for player to win after enemy dies
        
    def update(self):
        
        
        def Direction_calc(): #Calculates which diretion enemy should go
                       
            #finding dirction to travel
            self.target_point = (game.player.x,game.player.y)
            
            relitivex=self.target_point[0]-self.x # difference in x coordinates of player and enemy
            relitivey=self.target_point[1]-self.y # difference in y
            self.calc_angle = math.degrees(math.atan2(relitivex,relitivey)) #angle used to calculate the target angle
            
            
            self.range = math.hypot(self.x - game.player.x, self.y - game.player.y) #calculates range
            if self.range < 275: #if range < 275
                self.circleing = True #set flag for cricleing
                self.target_angle = 270 + self.calc_angle #move at a right angle to player
            else:
                self.circleing = False #set flag for not circleing
                self.target_angle = 180 + self.calc_angle ##move towards player
            
            #Finding if need to change speed
            if self.stopped == True: #if stopped
                if self.speed_change == "none": #if not changeing speed
                    self.speed_change = "up"  #start moveing
            elif not(self.relitive_angle > 350 or self.relitive_angle < 10): #if not pointing at player
                if self.full_speed == True: #if not already at full speed
                    if self.speed_change == "none": #if not changeing speed
                        self.speed_change = "down" #slow down
            elif self.full_speed == False: #if pointing at player
                if self.speed_change == "none": #and not changeing speed
                    self.speed_change = "up" #speed up
        
        def Speed_change(): #same as player speed change
            
            if self.speed_change == "up":
                if self.sail_trimed == False:
                    self.state += 1
                    self.sail_trimed = True
                if self.speed_added < 25:
                    self.speed_added += 0.25
                    self.speed -= 0.25
                else:
                    self.speed_added = 0
                    self.sail_trimed = False
                    self.speed_change = "none"
                    
                    if self.state == 2:
                        self.full_speed = True
                        self.rotate_speed = 0.3
                    elif self.state == 1:
                        self.rotate_speed = 0.5
                        
                    self.stopped = False
            
            elif self.speed_change == "down":
                if self.sail_trimed == False:
                    self.state -= 1
                    self.sail_trimed = True
                if self.speed_added < 20:
                    self.speed_added += 0.25
                    self.speed += 0.25
                else:
                    self.speed_added = 0
                    self.sail_trimed = False
                    self.speed_change = "none"
                    
                    if self.state == 0:
                        self.stopped = True
                        self.rotate_speed = 0.05
                    elif self.state == 1:
                        self.rotate_speed = 0.4
                    
                    self.full_speed = False
            
            elif self.speed_change == "knocked":
                if self.knocked == False:
                    self.state = 0
                    print(self.state)
                    self.speed = 30
                    self.speed_added = 0
                    self.knocked = True
                if self.speed_added < 30:
                    self.speed_added += 0.25
                    self.speed -= 0.25
                else:
                    self.speed_added = 0
                    self.sail_trimed = False
                    self.speed_change = "none"
                    self.stopped = True
                    self.rotate_speed = 0.05
                    self.full_speed = False
                    self.knocked = False

        def Turn(): #handles turning
            if self.speed_change != "knocked": #if not knocked back
                
                if self.angle_from_target > 0 and self.angle_from_target <= 180: #if target angle to the right
                    self.angle += self.rotate_speed #turn right
                elif self.angle_from_target > 180 and self.angle_from_target < 360: #if to the left
                    self.angle -= self.rotate_speed #turn left
                
                self.angle %= 360 #keep angle in range
                
            self.sprite = game.rotate(self.ship[self.state],self.angle) #rotate the sprite so its faceing the new direction
                    
        def Move(): #handles homveing
            self.x += math.sin(math.radians(self.angle)) * (self.speed * game.secounds) #equations for working out
            self.y += math.cos(math.radians(self.angle)) * (self.speed * game.secounds) #movement
            
            self.rect = self.ship[self.state].get_rect(left=self.x,top=self.y) #undate the rect with the new position
            
        def collitions(): #handles collitions
            if not game.rect.colliderect(self.rect): #if off screen
                self.x %= game.width #keeps position in rnage of screen size
                self.y %= game.hight
            
            self.mask = pygame.mask.from_surface(self.sprite) #updates enemy mask
            pixle_offset = (int(game.player.x-self.x),int(game.player.y-self.y)) #calculates offset
            if self.mask.overlap(game.player.mask,pixle_offset): #if enemy touching player
                self.speed_change = "knocked" #enemy is knocked
        
        def Position(): #calculates position relitive to player
            self.relitive_angle =  180 + self.calc_angle - self.angle #calculates relitive angle
            self.relitive_angle %= 360 #keeps angle in range
                
            self.angle_from_target = self.target_angle - self.angle #calulates angle form target
            self.angle_from_target %= 360 #keeps angle in range
            

  
        def Fire(): #handles fireing
            if self.range < 250 and self.circleing == True: #if in range and is circleing player
                if self.relitive_angle > 80 and self.relitive_angle < 100 and self.reloadingL == False: #if player on left side
                    game.fire_sound.play() #plays fire sound effect
                    self.left_fireing = 4 #all cannons fireing
                    self.cannonl1 = Cannon(30,"l","e1") #left cannons are created
                    self.cannonl2 = Cannon(16,"l","e1")
                    self.cannonl3 = Cannon(2,"l","e1")
                    self.cannonl4 = Cannon(-5,"l","e1")
                    self.reloadingL = True #is currently reloading
                elif self.relitive_angle > 260 and self.relitive_angle < 280 and self.reloadingR == False: #same for right side
                    game.fire_sound.play() #plays fire sound effect
                    self.right_fireing = 4
                    self.cannonr1 = Cannon(30,"r","e1")
                    self.cannonr2 = Cannon(16,"r","e1")
                    self.cannonr3 = Cannon(2,"r","e1")
                    self.cannonr4 = Cannon(-5,"r","e1")
                    self.reloadingR = True
            
            if self.left_fireing > 0: #if cannons are still fireing
                self.cannonl1.run() #run cannons
                self.cannonl2.run()
                self.cannonl3.run()
                self.cannonl4.run()
                
            if self.right_fireing > 0: #same for other side
                self.cannonr1.run()
                self.cannonr2.run()
                self.cannonr3.run()
                self.cannonr4.run()
                
            if self.reloadingL == True: #if reloading
                self.reload_timerL += game.secounds #increment relode timer
                if self.reload_timerL > 5: #if 5 secs have passed
                    self.reload_timerL = 0 #reset timer
                    self.reloadingL = False #no longer reloadng
                    
            if self.reloadingR == True: #same for other side
                self.reload_timerR += game.secounds
                if self.reload_timerR > 5:
                    self.reload_timerR = 0
                    self.reloadingR = False
            

        def sunk(): #handles if enemy is sunk
            if self.wrecked == False: # if ship just been wrecked
                self.wrecked = True #flag to show if enemy has been sunk
                self.state = 3 #sets state to 3 so shipwreck sprite is displayed
                game.sunk_sound.play() #plays sunk sound
                
            rotated = game.rotate(self.ship[self.state],self.angle) #rotates shipwreck sprite to correct position
            game.screen.blit(rotated,(self.x,self.y)) #displays sprite
            
            self.lose_timer += game.secounds #add seconds since last frame to timer
            if self.lose_timer > 5: # 5 secounds have passed
                self.lose_timer = 0 #reset timer
                game.gamemode = 4 #set game mode to 4 (Player wins)
                game.score_calc() #calculates score
        
        if self.HP > 0: #same code from player class with the addition of direcction_calc
            Direction_calc()
            Speed_change()
            Turn()
            Move()
            collitions()
            Position()
            Fire()
            game.screen.blit(self.sprite,(self.x,self.y))
                
        else:
            sunk() 

class Cannon():
    def __init__(self,offset,direction,source):
        
        if source == "p": #if comming from player
            if direction == "l": #if going left
                self.angle = game.player.angle - 90 #make angle at a right angle to the ship on left side
            elif direction == "r": #if going right
                self.angle = game.player.angle + 90 #make angle at a right angle to the ship on right side
        
        elif source == "e1": #same for is coming from enemy
            if direction == "l":
                self.angle = game.enemy.angle - 90
            elif direction == "r":
                self.angle = game.enemy.angle + 90
        
        if self.angle < 0:
            self.angle += 360
            
            
        if source == "p": #if coming from plauer
            self.x = int(game.player.x + game.player.ship[0].get_rect().centerx) #x and y coordinates is x or y position of
            self.y = int(game.player.y + game.player.ship[0].get_rect().centery) # player + halfof the player hight or width 
                                                                                 #so Ball is placed in the center of the player
        elif source == "e1":
            self.x = int(game.enemy.x + game.enemy.ship[0].get_rect().centerx) #same for enemy
            self.y = int(game.enemy.y + game.enemy.ship[0].get_rect().centery)
        
        if offset < 0:   #if offset less than 0
            self.offset_angle = -90 #cannonball travels down before going out
        elif offset > 0: #if more
            self.offset_angle = 90 # cannonball travels up before going out
        self.offset_distance = abs(offset) #distance it travels up or down must be positive
        
        self.source = source #sets source and direction as attributes of cannon class
        self.direction = direction
    
        self.set_up = True #flag for if this ball is in position
        self.go = False #flag for if all balls are in position
        self.cycle_time = 0 #timer for getting into position
        
        self.speed = 200 #variable for speed
        
        self.distance = 0 #distance traveled
        self.range = 250 #max range
        
        self.pos = 0 
        self.stopped = False
        self.splashing = False
        
        self.ball = pygame.image.load(os.path.join("data","sprites","ball.png")).convert_alpha() # loads ball sprite
        
        self.mask = pygame.mask.from_surface(self.ball)
        
        self.splash = [pygame.image.load(os.path.join("data","sprites","splash","splash1.png")),pygame.image.load(os.path.join("data","sprites","splash","splash2.png")),pygame.image.load(os.path.join("data","sprites","splash","splash3.png")),pygame.image.load(os.path.join("data","sprites","splash","splash4.png")),pygame.image.load(os.path.join("data","sprites","splash","splash5.png")),pygame.image.load(os.path.join("data","sprites","splash","splash6.png")),pygame.image.load(os.path.join("data","sprites","splash","splash7.png"))]
        #loads in splash sprite
         
         
    
    def move(self):# handles move
     
        if self.go == False: #if cannon balls still setting up
            self.cycle_time += game.secounds #Increment timer
            
        if self.cycle_time >= 0.25: #if cannon balls have been moveing for 0.25s (time for all to be in position)
            self.cycle_time = 0 #reset timer
            self.go = True #ball is in correct position and can fire
            
        if self.distance >= self.offset_distance and self.set_up == True: #if traveled correct distance to start point
            self.speed = 100 #speed set to normal value
            self.offset_angle = 0 #makes ball travel out instead of up
            self.distance = 0 #resets deistance travled
            self.set_up = False #flag to show tthis ball is in position and is waiting for others
        
        if self.set_up == True or self.go == True: #if moveing into position or fireing
            #equations for movement
            self.x += int(round(math.sin(math.radians(self.angle - self.offset_angle)) * (self.speed * game.secounds)))
            self.y += int(round(math.cos(math.radians(self.angle - self.offset_angle)) * (self.speed * game.secounds)))

            self.distance += self.speed * game.secounds #adds distance traveld this frame to total distance
            game.screen.blit(self.ball,(self.x,self.y)) #display ball on screen
    
    def collitions(self): #handles collitions
        
        if self.distance >= self.range: #if cannon ball gose past max range
                self.miss() #Call miss function
                
        pixle_offset = (int(game.enemy.x-self.x),int(game.enemy.y-self.y)) #calculates pixel offset for cannon ball and enemy
        if self.mask.overlap(game.enemy.mask,pixle_offset) and game.enemy.wrecked == False and self.distance > 75 : #if cannon ball mask touching player mask
            game.enemy.HP -= 10 #subtract form enemy hp
            self.hit() #call hit methiod
                
        pixle_offset = (int(game.player.x-self.x),int(game.player.y-self.y)) #calculates pixel offset for cannon ball and player
        if self.mask.overlap(game.player.mask,pixle_offset) and game.player.wrecked == False and self.distance > 75: #if cannon ball mask touching enemy mask
            game.player.HP -= 10 #subtract form player hp
            self.hit() #call hit methoid
        
    
    def miss(self): #handles if the ball misses
        game.miss_sound.play() #plays splash sound
        
        self.splashing = True #flag to show splash animation is going
        if self.pos < 7: #if miss annomation not compleated
            game.screen.blit(self.splash[self.pos],(self.x,self.y)) #display splash on screen
            self.cycle_time += game.secounds #increment timer
            
            if self.cycle_time > 0.1: #if 0.1 secounds pass
                self.pos += 1 #move onto next frame of annimation
                self.cycle_time = 0 #reset timer
        else: #if finnished animation
            
            if self.source == "p": #if ball fired from player
                if self.direction == "l": #if fired from left side
                    game.player.left_fireing -= 1 #decrease number of cannons fireing on left side by 1
                elif self.direction == "r": #same for right side
                    game.player.right_fireing -= 1

            elif self.source == "e": #same for enemy
                if self.direction == "l":
                    game.enemy.left_fireing -= 1
                elif self.direction == "r":
                    game.enemy.right_fireing -= 1

            self.stopped = True #cannon ball has stopped
            self.splashing = False #splash annimation is no longer going
    
    def hit(self): #handles if the ball hits
        game.hit_sound.play() #plays hit sound
        
        if self.source == "p": #if ball fired form player
            if self.direction == "l": #if fired from left side
                game.player.left_fireing -= 1 # -1 form number of canon balls still fireing
            elif self.direction == "r": #same for if fired from left  side
                game.player.right_fireing -= 1

        elif self.source == "e": #same for if fired from enemy
            if self.direction == "l":
                game.enemy.left_fireing -= 1
            elif self.direction == "r":
                game.enemy.right_fireing -= 1
        self.stopped = True #flag to show cannon ball has stopped
    
    def run(self): #runs all the previous methoids
        if self.stopped == False: #if cannon still going
           if self.splashing == False: #if not doing splash annimation (stops moveing when it hits the water)
               self.move() #move
           self.collitions() #Check for collitions        
        
        

class Main(): #Main class
    def __init__(self): #initalisadtion function, the self identifys which variables are attributes to the class
        pygame.init() #Set up pygame so it can be used
        pygame.font.init() #inicalise font pakage to display text
        pygame.mixer.pre_init(44100, 16, 2, 4096) #inicalise mixer
        
        self.font = pygame.font.SysFont('Edwardian Script ITC', 100) #defines font
        
        self.finished = False #This flag controls when the game exits
        
        self.hight = 700 #hight and width are defined for use in positioning things on the screen
        self.width = 1024
        self.screen = pygame.display.set_mode((self.width,self.hight)) #screen is deinfeied
        pygame.display.set_caption("Ships") #sets window caption
        icon = pygame.image.load(os.path.join("data","sprites","icon.png")) #loads in icon
        pygame.display.set_icon(icon) #sets icon
        self.rect = self.screen.get_rect() #rect of screen
                                                                                        
        self.background = pygame.image.load(os.path.join("data","sprites", "background.png")) #loads in background
        self.player = player(self.width/2-55,500) #creates player
        self.enemy = Enemy(self.width/2-55,200) #creates enemy starting in middlw top od screen
        
        self.gamemode = 0 #gamemode variable contols which screen is displayed
        self.score = 0 #player's score
        self.mouse = (0,0) #contins position of last mouse click
        
        self.start = pygame.image.load(os.path.join("data","sprites", "start.png")).convert_alpha() #loads in start screen
        self.start_play_rect = pygame.Rect((39,466),(300,100)) #defines rect for play button
        self.start_instructions_rect = pygame.Rect((493,460),(300,100)) #defines rect for instructions button
        self.start_exit_rect = pygame.Rect((282,592),(300,100)) #definces rect for menu buttons
        
        self.Pause_pic = pygame.image.load(os.path.join("data","sprites", "Paused.png")).convert_alpha() #loads in pause screen
        self.Pause_resume_rect = pygame.Rect((336,231),(300,100)) #defines rect for resume button
        self.Pause_instruction_rect = pygame.Rect((337,337),(300,100)) #defines rect forinstruction button
        self.Pause_menu_rect = pygame.Rect((337,465),(300,100)) #defines rect for menu button
        
        self.lose_pic = pygame.image.load(os.path.join("data","sprites", "lose.png")).convert_alpha() #loads in lose screen
        self.lose_again_rect = pygame.Rect((62,437),(300,100)) #defines rect for try again button
        self.lose_menu_rect = pygame.Rect((616,437),(300,100)) #defines rect for menu button
        
        self.win_pic = pygame.image.load(os.path.join("data","sprites", "Win.png")).convert_alpha() #loads in lose screen
        self.win_again_rect = pygame.Rect((36,531),(300,100)) #defines rect for try again button
        self.win_menu_rect = pygame.Rect((682,529),(300,100)) #defines rect for menu button
        self.textsurface = self.font.render(" ", False, (0, 0, 0)) #defines font
        
        self.instruction_pic = pygame.image.load(os.path.join("data","sprites", "Instructions.png")).convert_alpha() # load in instruction pic
        self.instruction = False #flag to show if instructions should be shown
        self.ESC = False #flag to show escape key has been pressed
        
        self.secounds = 0 #time since last frame
        self.timer = 0 #time game has been played for this round
        self.clock = pygame.time.Clock() #sets up the clock in order to give the game the desired framerate
        
        self.fire_sound = pygame.mixer.Sound(os.path.join("data","sound", "cannon.wav")) #loads in sound effects
        self.bump_sound = pygame.mixer.Sound(os.path.join("data","sound", "collide.wav"))
        self.hit_sound = pygame.mixer.Sound(os.path.join("data","sound", "hit.wav"))
        self.miss_sound = pygame.mixer.Sound(os.path.join("data","sound", "splash.wav"))
        self.speed_change_sound = pygame.mixer.Sound(os.path.join("data","sound", "Sail fold.wav"))
        self.click_sound = pygame.mixer.Sound(os.path.join("data","sound", "click.wav"))
        self.sunk_sound = pygame.mixer.Sound(os.path.join("data","sound", "sunk.wav"))
        
        pygame.mixer.music.load(os.path.join("data","sound","Corner.wav")) #loads music for title screen
        pygame.mixer.music.play(-1) #plays music for title screen
        
    def Start_update(self): #methoid for start screen
        
        if self.instruction == True: #if instructions should be displayed
            self.screen.blit(self.instruction_pic,(0,0)) # display instruction
            
            if self.ESC == True: #if esc key pressed
                self.instruction = False #instructions should no longer be shown
                self.ESC = False #reset esc key
        
        elif self.start_play_rect.collidepoint(self.mouse): #if play button pressed
            self.click_sound.play() #plays click sound
            pygame.mixer.music.load(os.path.join("data","sound","Corner2.wav")) #loads music for game
            pygame.mixer.music.play(-1) #plays music for game
            self.gamemode = 1 #change game mode so game starts

            
        elif self.start_exit_rect.collidepoint(self.mouse):  #if exit button pressed
            self.click_sound.play() #plays click sound
            self.finished = True #stops main game loop to exit game
        
        elif self.start_instructions_rect.collidepoint(self.mouse): # if instruction button clicked
            self.click_sound.play() #plays click sound
            self.instruction = True # set flag to show instructions should be displayed
            
        else:
            self.screen.blit(self.start,(0,0)) #otherwise display start screen
    
    def Game_update(self): #methoid for game                 
        self.screen.blit(self.background,(0,0)) #displays background on screen
        self.enemy.update() #Run the enemy's update methoid
        self.player.update() #Runs the player's update methoid to display the player on top of the background
        self.timer += game.secounds #incrments game timer
    
    def Pause_update(self): #method for pause screen
        if self.instruction == True: # if instructions should be displayed
            self.screen.blit(self.instruction_pic,(0,0)) #display instructions
            
            if self.ESC == True: #if Esc key has been pressed
                self.instruction = False #instructions should no longer be displayed
                self.ESC = False #Esc key press has been delt with
        
        elif self.Pause_resume_rect.collidepoint(self.mouse): # if resume button clicked
            self.click_sound.play() #plays click sound
            self.gamemode = 1 #game mode is set to play game
            
        elif self.Pause_instruction_rect.collidepoint(self.mouse): #if instruction button pressed
            self.click_sound.play() #plays click sound
            self.instruction = True #instructions should be displayed
            
        elif self.Pause_menu_rect.collidepoint(self.mouse): #if exit button pressed
            self.click_sound.play() #plays click sound
            pygame.mixer.music.load(os.path.join("data","sound","Corner.wav")) #loads music for title screen
            pygame.mixer.music.play(-1) #plays music for title screen
            self.gamemode = 0 #game mode set to menu
            self.Reset() #reset game

        else:
            self.screen.blit(self.Pause_pic,(0,0)) #display puase screen if no buttons pressed
    
    def lose_update(self): #method for lose screen
        self.Reset() #reset game
        if self.lose_again_rect.collidepoint(self.mouse): # if try again button clicked
            self.click_sound.play() #plays click sound
            self.gamemode = 1 #game mode is set to play game
        elif self.lose_menu_rect.collidepoint(self.mouse): # if menu button clicked
            self.click_sound.play() #plays click sound
            pygame.mixer.music.load(os.path.join("data","sound","Corner.wav")) #loads music for title screen
            pygame.mixer.music.play(-1) #plays music for title screen
            self.gamemode = 0 #game mode is set to start screen
        else:
            self.screen.blit(self.lose_pic,(0,0)) #display lose screen if no buttons pressed
    
    def win_update(self): #method for win screen
        self.Reset() #reset game
        if self.win_again_rect.collidepoint(self.mouse): # if try again button clicked
            self.click_sound.play() #plays click sound
            self.gamemode = 1 #game mode is set to play game
        elif self.win_menu_rect.collidepoint(self.mouse): # if menu button clicked
            self.click_sound.play() #plays click sound
            pygame.mixer.music.load(os.path.join("data","sound","Corner.wav")) #loads music for title screen
            pygame.mixer.music.play(-1) #plays music for title screen
            self.gamemode = 0 #game mode is set to start screen
        else:
            self.screen.blit(self.win_pic,(0,0)) #display win screen if no buttons pressed
            self.screen.blit(self.textsurface,(530,395)) #display text on win screen
    
    def score_calc(self): #calculates score
        self.score = round((self.player.HP/self.timer) * 100) #score calculated and stored in variable
        self.textsurface = self.font.render(str(self.score), False, (255, 165, 0)) #creates text surface
        
    
    def run(self): #this is where the main game loop will be
        while not self.finished: #Main game loop
            
            for event in pygame.event.get(): #loop reapeays for every event since last frame
                if event.type == pygame.QUIT: #if exit button pressed
                    self.finished = True #game loop ends
                
                elif event.type == pygame.KEYDOWN:    #if the event is a keypress (this makes the handler more effient)
                    if event.key == pygame.K_ESCAPE: #if escape key pressed
                        if self.gamemode == 1: #if game being played
                            self.gamemode = 2 #game mode for pause screen
                        elif self.instruction == True: #if not and instuctions should be displayed
                            self.ESC = True #Esc flag set to true
                    
                    if event.key == pygame.K_w:  #if w pressed
                        if self.player.speed_change == "none" and self.player.full_speed == False: #if not changeing speed 
                            self.player.speed_change = "up" #speed up                               and not at full speed
                    
                    elif event.key == pygame.K_s: #if s pressed
                        if self.player.speed_change == "none" and self.player.stopped == False: #if not changeing speed 
                            self.player.speed_change = "down" #speed down                          and not stoped
                    
                    
                    elif event.key == pygame.K_LCTRL:# if control key pressed
                        if self.player.reloadingL == False and self.player.speed_change != "knocked": #if not reloading and not knocked
                            self.fire_sound.play() #plays fire sound effect
                            self.player.left_fireing = 4 #all cannons are fireing
                            self.player.cannonl1 = Cannon(30,"l","p") #calls cannon balls with different offsets 
                            self.player.cannonl2 = Cannon(16,"l","p") #that i have been guessed for now
                            self.player.cannonl3 = Cannon(2,"l","p")
                            self.player.cannonl4 = Cannon(-5,"l","p")
                            self.player.reloadingL = True #flag shows cannons are reloading and cant fire
                    
                    elif event.key == pygame.K_SPACE: #if space key pressed, same as above for right side
                        if self.player.reloadingR == False and self.player.speed_change != "knocked":
                            self.fire_sound.play() #plays fire sound effect
                            self.player.right_fireing = 4
                            self.player.cannonr1 = Cannon(-30,"r","p")
                            self.player.cannonr2 = Cannon(-16,"r","p")
                            self.player.cannonr3 = Cannon(-2,"r","p")
                            self.player.cannonr4 = Cannon(5,"r","p")
                            self.player.reloadingR = True
                            
                elif event.type == pygame.MOUSEBUTTONUP: #if mouse clicked
                  self.mouse = pygame.mouse.get_pos() # records mouse position
            
            if self.gamemode == 0: #if game mode = 0 (start)
                self.Start_update() #display start screen
                 
            elif self.gamemode == 1: #if = 1 (game)
                self.Game_update() #display game
                
            elif self.gamemode == 2: #if = 2 (pause screen)
                self.Pause_update() #display pause screen
            
            elif self.gamemode == 3: #if = 3 (lose screen)
                self.lose_update() #display lose screen
            
            elif self.gamemode == 4: #if = 4 (win screen
                self.win_update() #display win screen
                
            self.mouse = (0,0)  #resets postion of mouse click
            pygame.display.update() #updates the screen with any changes
            self.secounds = self.clock.tick(60) / 1000.0 #keeps the framerate at 60fps and
                                                        #records the time in secouds since last frame
            
        pygame.quit()
    
    def rotate(self,image, angle):    
            rect = image.get_rect()   #gets rect from origonal image
            new_image = pygame.transform.rotate(image, angle)  #rotate the image
            rect.center = new_image.get_rect().center  #recenters the new image
            new_image = new_image.subsurface(rect)
            return new_image #retuens rotated image
    
    def Reset(self): #resets game
        self.player = player(self.width/2-55,500) #redefines player object so variables returnd to starting state
        self.enemy = Enemy(self.width/2-55,200)#redefines enemy object
        self.timer = 0 #timer reset


game = Main() #creats instance of main class
game.run() #runs program
