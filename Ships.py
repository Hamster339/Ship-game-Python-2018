import pygame
import os
import math

class Enemy():
    def __init__(self,x,y):
        self.var = 0
        
        self.x = x
        self.y = y
        self.angle = 180
        
        self.calc_angle = 0
        self.target_angle = 0
        self.angle_from_target = 0
        self.relitive_angle = 0
        self.target_point = (0,0)
        self.relitave_position = (0,0)
        self.range = 0
        
        self.speed = 0
        self.rotate_speed = 0.05
        
        self.speed_change = "none"
        self.speed_added = 0
        self.sail_trimed = False
        self.full_speed = False
        self.stopped = True
        self.circleing = False
        
        self.HP = 100
        self.state = 0
        self.wrecked = False
        self.knocked = False
        
        self.ship = [pygame.image.load(os.path.join("sprites","french ship","french boat stoped.png")),pygame.image.load(os.path.join("sprites","french ship", "french boat half.png")),pygame.image.load(os.path.join("sprites","french ship", "french boat full.png")),pygame.image.load(os.path.join("sprites","wreck.png"))]
        
        self.sprite = self.ship[self.state]
        self.mask = pygame.mask.from_surface(self.ship[self.state])
        self.rect = self.ship[self.state].get_rect(left=self.x,top=self.y)
        
        self.left_fireing = 0
        self.right_fireing = 0
        self.reloadingL = False
        self.reloadingR = False
        self.reload_timerR = 0
        self.reload_timerL= 0
        
    
    def update(self):
        
        
        def Direction_calc():
            
            #finding dirction to travel
            self.target_point = (game.player.x,game.player.y)
            
            relitivex=self.target_point[0]-self.x
            relitivey=self.target_point[1]-self.y
            self.calc_angle = math.degrees(math.atan2(relitivex,relitivey))
            
            
            self.range = math.hypot(relitivex, relitivey)
            if self.range < 250:
                self.circleing = True
                self.target_angle = 270 + self.calc_angle
            else:
                self.circleing = False
                self.target_angle = 180 + self.calc_angle
            
            #Finding if need to change speed
            if self.stopped == True:
                if self.speed_change == "none":
                    self.speed_change = "up"
            elif not(self.relitive_angle > 350 or self.relitive_angle < 10):
                if self.full_speed == True:
                    if self.speed_change == "none":
                        self.speed_change = "down"
            elif self.full_speed == False:
                if self.speed_change == "none":
                    self.speed_change = "up"
        
        def Speed_change():
            #change speed
            if self.speed_change == "up":
                if self.sail_trimed == False:
                    self.state += 1
                    self.sail_trimed = True
                if self.speed_added < 20:
                    self.speed_added += 0.25
                    self.speed -= 0.25
                else:
                    self.speed_added = 0
                    self.sail_trimed = False
                    self.speed_change = "none"
                    
                    if self.state == 2:
                        self.full_speed = True
                        self.rotate_speed = 0.2
                    elif self.state == 1:
                        self.rotate_speed = 0.4
                        
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
            #turns ship
            if self.speed_change != "knocked":
                
                if self.angle_from_target > 0 and self.angle_from_target <= 180:
                    self.angle += self.rotate_speed
                elif self.angle_from_target > 180 and self.angle_from_target < 360:
                    self.angle -= self.rotate_speed
                
                self.angle %= 360
                
                self.sprite = game.rotate(self.ship[self.state],self.angle)
                self.mask = pygame.mask.from_surface(self.sprite)
                    
        def Move():
            self.x += math.sin(math.radians(self.angle)) * (self.speed * game.secounds)
            self.y += math.cos(math.radians(self.angle)) * (self.speed * game.secounds)
            
            self.rect = self.ship[self.state].get_rect(left=self.x,top=self.y)
        
        def Collitions():
            if not game.rect.colliderect(self.rect):
                self.x %= game.width
                self.y %= game.hight
            
            pixle_offset = (int(game.player.x-self.x),int(game.player.y-self.y))
            if self.mask.overlap(game.player.mask,pixle_offset):
                self.speed_change = "knocked"
                
        def Position():
            self.relitive_angle =  180 + self.calc_angle - self.angle
            self.relitive_angle %= 360
                
            self.angle_from_target = self.target_angle - self.angle
            self.angle_from_target %= 360
            
        def Fire():
            if self.range < 250 and self.circleing == True:
                if self.relitive_angle > 80 and self.relitive_angle < 100 and self.reloadingL == False:
                    self.left_fireing = 4
                    self.cannonl1 = Cannon(30,"l",(self.x,self.y),self.angle,self.rect)
                    self.cannonl2 = Cannon(16,"l",(self.x,self.y),self.angle,self.rect)
                    self.cannonl3 = Cannon(2,"l",(self.x,self.y),self.angle,self.rect)
                    self.cannonl4 = Cannon(-5,"l",(self.x,self.y),self.angle,self.rect)
                    self.reloadingL = True
                elif self.relitive_angle > 260 and self.relitive_angle < 280 and self.reloadingR == False:
                    self.right_fireing = 4
                    self.cannonr1 = Cannon(30,"r",(self.x,self.y),self.angle,self.rect)
                    self.cannonr2 = Cannon(16,"r",(self.x,self.y),self.angle,self.rect)
                    self.cannonr3 = Cannon(2,"r",(self.x,self.y),self.angle,self.rect)
                    self.cannonr4 = Cannon(-5,"r",(self.x,self.y),self.angle,self.rect)
                    self.reloadingR = True
            
            
            try:
                if self.cannonl1.stopped == False or self.cannonl2.stopped == False or self.cannonl3.stopped == False or self.cannonl4.stopped == False:
                    self.cannonl1.run()
                    self.cannonl2.run()
                    self.cannonl3.run()
                    self.cannonl4.run()
            except:
                pass
                
            try:
                if self.cannonr1.stopped == False or self.cannonr2.stopped == False or self.cannonr3.stopped == False or self.cannonr4.stopped == False:
                    self.cannonr1.run()
                    self.cannonr2.run()
                    self.cannonr3.run()
                    self.cannonr4.run()
            except:
                pass
                
            if self.reloadingL == True:
                self.reload_timerL += game.secounds
                if self.reload_timerL > 5:
                    self.reload_timerL = 0
                    self.reloadingL = False
                    
            if self.reloadingR == True:
                self.reload_timerR += game.secounds
                if self.reload_timerR > 5:
                    self.reload_timerR = 0
                    self.reloadingR = False
        def sunk():
            self.wrecked = True
            self.state = 3
            rotated = game.rotate(self.ship[self.state],self.angle)
            game.screen.blit(rotated,(self.x,self.y))
            
        
        if self.HP > 0:
            Direction_calc()
            Speed_change()
            Turn()
            Move()
            Collitions()
            Position()
            Fire()
            game.screen.blit(self.sprite,(self.x,self.y))
                
        else:
            sunk()
            

class player():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angle = 0
        
        self.speed = 0
        self.rotate_speed = 0.05
        
        self.speed_change = "none"
        self.speed_added = 0
        self.sail_trimed = False
        self.full_speed = False
        self.stopped = True
        self.knocked = False
        self.wrecked = False
        
        self.state = 0
        self.HP = 100
        self.score = 0
        self.ship = [pygame.image.load(os.path.join("sprites","brittish ship","brittish boat stoped.png")),pygame.image.load(os.path.join("sprites","brittish ship", "brittish boat half.png")),pygame.image.load(os.path.join("sprites","brittish ship", "brittish boat full.png")),pygame.image.load(os.path.join("sprites","wreck.png"))]
        self.mask = pygame.mask.from_surface(self.ship[self.state])
        self.rect = self.ship[self.state].get_rect(left=self.x,top=self.y)
        
        self.left_fireing = 0
        self.right_fireing = 0
        
        self.reloadingL = False
        self.reloadingR = False
        self.reload_timerR = 0
        self.reload_timerL= 0
        
    
    def update(self):
        
        def Speed_change():
            if self.speed_change == "up":
                if self.sail_trimed == False:
                    self.state += 1
                    self.sail_trimed = True
                if self.speed_added < 20:
                    self.speed_added += 0.25
                    self.speed -= 0.25
                else:
                    self.speed_added = 0
                    self.sail_trimed = False
                    self.speed_change = "none"
                    
                    if self.state == 2:
                        self.full_speed = True
                        self.rotate_speed = 0.2
                    elif self.state == 1:
                        self.rotate_speed = 0.4
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
            if self.speed_change != "knocked":
                pressedkeys = pygame.key.get_pressed()
                if pressedkeys[pygame.K_a]:
                    self.angle += self.rotate_speed
                elif pressedkeys[pygame.K_d]:
                    self.angle -= self.rotate_speed
            self.angle %= 360
            
            self.sprite = game.rotate(self.ship[self.state],self.angle)
            self.mask = pygame.mask.from_surface(self.sprite)
                    
        def Move():
            self.x += math.sin(math.radians(self.angle)) * (self.speed * game.secounds)
            self.y += math.cos(math.radians(self.angle)) * (self.speed * game.secounds)
            
            self.rect = self.ship[self.state].get_rect(left=self.x,top=self.y)
        
        def Collitions():
            if game.enemy.wrecked == True:
                if not game.rect.colliderect(self.rect) and self.y <= 0:
                    print("win")
                    game.gamemode = 5
                    
                    self.score += (self.HP/game.timer) * 100
                    game.timer = 0
                    
                    print(self.score)
                    self.score = 0
    
                    
            if not game.rect.colliderect(self.rect):
                self.x %= game.width
                self.y %= game.hight
            
            #repeat for all enemies
            pixle_offset = (int(game.enemy.x-self.x),int(game.enemy.y-self.y))
            if self.mask.overlap(game.enemy.mask,pixle_offset) and game.enemy.wrecked == False:
                self.speed_change = "knocked"
        
        def Fire():
            if self.left_fireing > 0:
                self.cannonl1.run()
                self.cannonl2.run()
                self.cannonl3.run()
                self.cannonl4.run()
                
            if self.right_fireing > 0:
                self.cannonr1.run()
                self.cannonr2.run()
                self.cannonr3.run()
                self.cannonr4.run()
            
            if self.reloadingL == True:
                self.reload_timerL += game.secounds
                if self.reload_timerL > 5:
                    self.reload_timerL = 0
                    self.reloadingL = False
                    
            if self.reloadingR == True:
                self.reload_timerR += game.secounds
                if self.reload_timerR > 5:
                    self.reload_timerR = 0
                    self.reloadingR = False
        
        def Sunk():
            self.wrecked = True
            self.state = 3
            rotated = game.rotate(self.ship[self.state],self.angle)
            game.screen.blit(rotated,(self.x,self.y))
        
        if self.HP > 0:
            Speed_change()
            Turn()
            Move()
            Collitions()
            Fire()
            game.screen.blit(self.sprite,(self.x,self.y))
                
        else:
            Sunk()



class Cannon():
    def __init__(self,offset,direction,ship_position,ship_angle,ship_rect):
        
        if direction == "l":
            self.angle = ship_angle - 90
        elif direction == "r":
            self.angle = ship_angle + 90

        self.angle %= 360
            
        self.x = int(ship_position[0] - ship_rect.centerx) #error is here
        self.y = int(ship_position[1] - ship_rect.centerx) #error is here
        
        if offset < 0:
            self.offset_angle = -90
        elif offset > 0:
            self.offset_angle = 90
        self.offset_distance = abs(offset)
    
        self.set_up = True
        self.go = False
        
        self.speed = 200
        
        self.distance = 0
        self.range = 250
        
        self.pos = 0
        self.cycle_time = 0
        self.stopped = False
        self.splashing = False
        
        self.ball = pygame.image.load(os.path.join("sprites","ball.png"))
        self.mask = pygame.mask.from_surface(self.ball)
        
        self.splash = [pygame.image.load(os.path.join("sprites","splash","splash1.png")),pygame.image.load(os.path.join("sprites","splash","splash2.png")),pygame.image.load(os.path.join("sprites","splash","splash3.png")),pygame.image.load(os.path.join("sprites","splash","splash4.png")),pygame.image.load(os.path.join("sprites","splash","splash5.png")),pygame.image.load(os.path.join("sprites","splash","splash6.png")),pygame.image.load(os.path.join("sprites","splash","splash7.png"))]
        
    def move(self):
        
        if self.go == False:
            self.cycle_time += game.secounds
        
        if self.cycle_time >= 0.25:
            self.cycle_time = 0
            self.go = True
                
        if self.distance >= self.offset_distance and self.set_up == True:
            self.speed = 100
            self.offset_angle = 0
            self.distance = 0
            self.set_up = False
        
        if self.set_up == True or self.go == True:
            self.x += int(round(math.sin(math.radians(self.angle - self.offset_angle)) * (self.speed * game.secounds)))
            self.y += int(round(math.cos(math.radians(self.angle - self.offset_angle)) * (self.speed * game.secounds)))
             
            print(self.x,self.y) 
            self.distance += self.speed * game.secounds
            game.screen.blit(self.ball,(self.x,self.y))
    
    def collitions(self):
        #repeat for all enemies
        pixle_offset = (int(game.enemy.x-self.x),int(game.enemy.y-self.y))
        if self.mask.overlap(game.enemy.mask,pixle_offset) and game.enemy.wrecked == False and self.distance > 75 :
            game.enemy.HP -= 10
            self.hit()
                
        pixle_offset = (int(game.player.x-self.x),int(game.player.y-self.y))
        if self.mask.overlap(game.player.mask,pixle_offset) and game.player.wrecked == False and self.distance > 75:
            game.player.HP -= 10
            self.hit()
            
        if self.distance >= self.range:
            self.miss()
    
    
    def miss(self):
        self.splashing = True
        if self.pos < 7:
            game.screen.blit(self.splash[self.pos],(self.x,self.y))
            self.cycle_time += game.secounds
            
            if self.cycle_time > 0.1:
                self.pos += 1
                self.cycle_time = 0
        else:
            self.stopped = True
            self.splashing = False
    
    def hit(self):
        if self.source == "p":
            if self.direction == "l":
                game.player.left_fireing -= 1
            elif self.direction == "r":
                game.player.right_fireing -= 1

        elif self.source == "e":
            if self.direction == "l":
                game.enemy.left_fireing -= 1
            elif self.direction == "r":
                game.enemy.right_fireing -= 1
        self.stopped = True
   
    def run(self):
       if self.stopped == False:
           if self.splashing == False:
               self.move()
           self.collitions()
            
class Main():
    def __init__(self):
        pygame.init()
        
        self.finished = False
        
        self.hight = 700
        self.width = 1024
        self.screen = pygame.display.set_mode((self.width,self.hight))
        self.rect = self.screen.get_rect()
        
        self.clock = pygame.time.Clock()
        self.secounds = 0
        self.timer = 0
        
        self.mouse = (0,0)
        self.ESC = False
        
        self.start = pygame.image.load(os.path.join("sprites", "start.png"))
        self.instruction_pic = pygame.image.load(os.path.join("sprites", "Instructions.png"))
        self.instruction = False
        
        self.start_play_rect = pygame.Rect((39,466),(300,100))
        self.start_instructions_rect = pygame.Rect((493,460),(300,100))
        self.start_exit_rect = pygame.Rect((282,592),(300,100))
        
        self.Pause_pic = pygame.image.load(os.path.join("sprites", "Paused.png"))
        self.Pause_resume_rect = pygame.Rect((336,231),(300,100))
        self.Puase_instruction_rect = pygame.Rect((337,337),(300,100))
        self.Pause_exit_rect = pygame.Rect((337,465),(300,100))
        
        self.background = pygame.image.load(os.path.join("sprites", "background.png"))
        
        self.player = player(self.width/2-55,500)
        self.enemy = Enemy(self.width/2-55,200)
        self.enemy2 = Enemy(self.width/2-155,200)
        self.enemy3 = Enemy(self.width/2+45,200)
        
        self.gamemode = 0
    
    def Start_update(self):
        
        if self.instruction == True:
            self.screen.blit(self.instruction_pic,(0,0))
            
            if self.ESC == True:
                self.instruction = False
                self.ESC = False
        
        elif self.start_play_rect.collidepoint(self.mouse):
            self.gamemode = 1
            self.mouse = (0,0)
            
        elif self.start_instructions_rect.collidepoint(self.mouse):
            self.instruction = True
            self.mouse = (0,0)
            
        elif self.start_exit_rect.collidepoint(self.mouse):
            self.finished = True
        
        else:
            self.screen.blit(self.start,(0,0))
        
        
    def Game_update(self):
        self.timer += self.secounds
        self.screen.blit(self.background,(0,0))
        self.enemy.update()
        self.player.update()
    
    def Pause_update(self):
        if self.instruction == True:
            self.screen.blit(self.instruction_pic,(0,0))
            
            if self.ESC == True:
                self.instruction = False
                self.ESC = False
        
        elif self.Pause_resume_rect.collidepoint(self.mouse):
            self.gamemode = 1
            self.mouse = (0,0)
            
        elif self.Puase_instruction_rect.collidepoint(self.mouse):
            self.instruction = True
            self.mouse = (0,0)
            
        elif self.Pause_exit_rect.collidepoint(self.mouse):
            self.gamemode = 0
            self.Reset()
            self.mouse = (0,0)

        else:
            self.screen.blit(self.Pause_pic,(0,0))
            
        
    
    def Win_update(self):
        pass
    
    def fail_update(self):
        pass
    
    def Reset(self):
        self.player = player(self.width/2-55,500)
        self.enemy = Enemy(self.width/2-55,200)
        self.enemy2 = Enemy(self.width/2-155,200)
        self.enemy3 = Enemy(self.width/2+45,200)
    
    def rotate(self,image, angle):
        rect = image.get_rect()
        new_image = pygame.transform.rotate(image, angle)
        rect.center = new_image.get_rect().center
        new_image = new_image.subsurface(rect)
        return new_image
    
    def run(self):
        while not self.finished:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_ESCAPE:
                        if self.gamemode in range(1,3):
                            self.gamemode = 4
                        elif self.instruction == True:
                            self.ESC = True
                    
                    elif event.key == pygame.K_w:
                        if self.player.speed_change == "none" and self.player.full_speed == False:
                            self.player.speed_change = "up"
                    elif event.key == pygame.K_s:
                        if self.player.speed_change == "none" and self.player.stopped == False:
                            self.player.speed_change = "down"
                    elif event.key == pygame.K_LCTRL:
                        if self.player.reloadingL == False and self.player.speed_change != "knocked":
                            self.player.left_fireing = 4
                            self.player.cannonl1 = Cannon(30,"l",(game.player.x,game.player.y),game.player.angle,game.player.rect)
                            self.player.cannonl2 = Cannon(16,"l",(game.player.x,game.player.y),game.player.angle,game.player.rect)
                            self.player.cannonl3 = Cannon(2,"l",(game.player.x,game.player.y),game.player.angle,game.player.rect)
                            self.player.cannonl4 = Cannon(-5,"l",(game.player.x,game.player.y),game.player.angle,game.player.rect)
                            self.player.reloadingL = True
                    elif event.key == pygame.K_SPACE:
                        if self.player.reloadingR == False and self.player.speed_change != "knocked":
                            self.player.right_fireing = 4
                            self.player.cannonr1 = Cannon(-30,"r",(game.player.x,game.player.y),game.player.angle,game.player.rect)
                            self.player.cannonr2 = Cannon(-16,"r",(game.player.x,game.player.y),game.player.angle,game.player.rect)
                            self.player.cannonr3 = Cannon(-2,"r",(game.player.x,game.player.y),game.player.angle,game.player.rect)
                            self.player.cannonr4 = Cannon(5,"r",(game.player.x,game.player.y),game.player.angle,game.player.rect)
                            self.player.reloadingR = True

                elif event.type == pygame.MOUSEBUTTONUP:
                  self.mouse = pygame.mouse.get_pos()
                        
                    
            if self.gamemode == 0:
                self.Start_update()
                 
            elif self.gamemode == 1:
                self.Game_update()
            
            elif self.gamemode == 2:
                self.Game_update()
           
            elif self.gamemode == 3:
                self.Game_update()
            
            elif self.gamemode == 4:
                self.Pause_update()
                
            elif self.gamemode == 5:
                self.Win_update()
                    
            self.mouse = (0,0)   
            pygame.display.update()
            self.secounds = self.clock.tick(60)/1000.0
        pygame.quit()
    


game = Main()
game.run()
