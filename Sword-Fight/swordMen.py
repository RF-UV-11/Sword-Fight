import pygame
from pygame import mixer

class swordMen():
    def __init__(self, x, y, details, ss, animations, sM):
        self.sm = sM
        #defining sclaes for players
        self.image_sc = details[1]
        #declaring frame index
        self.f_i = 0
        #defining attack trigger to control attack frequency
        self.atk_trig = False
        #fro creating rectangle space for players
        self.rect = pygame.Rect((x,y,60,210))
        #defining horizontal distance for moving actions
        self.hor_dist = 0
        #defining attack types
        self.atk_tp = 0
        #defining blood to display the health measure of the individual players on the screen
        self.blood = 100
        #defining action : JUMP
        self.jump = False
        #defining face of the player that if player crossed each other and try to attack then player must turned around to attack
        self.reve = details[3]
        #defining variable size for frame of an animation
        #used in extration of frames from spritesheet
        self.size = details[0]
        #defining positions / offsets
        self.oFSet = details[2]
        #creatinf default animation state
        self.deflt = details[4]
        #creating  actions for controls : syeady,running,atks,death,jump
        self.act = self.deflt
        #creating list to store animations
        self.anm_l = self.frame_img(ss, animations)
        #create an imagery graphic for characters
        self.img = self.anm_l[self.act][self.f_i]
        #defining time from when image has been created
        self.time = pygame.time.get_ticks()
        #defining triggerfor running animaion
        self.run = False
        #for death
        self.death = False

    #constructing method to sketch player
    def sketch(self, surface):
        flipped_img = pygame.transform.flip(self.img, self.reve, False)
        #pygame.draw.rect(surface, (200, 55, 170), self.rect)
        #putting graphics
        surface.blit(flipped_img, (self.rect.x - (self.oFSet[0] * self.image_sc) , self.rect.y - (self.oFSet[1] * self.image_sc)))


    #consrtucting method to handle all the controls for diff movements of the players
    def actions(self, sc_width, sc_height, surface, opponent):
        self.run = False
        self.atk_tp = 0
        #speed variable is used to control the distance moved by player when moves are left or right
        #its for the total displacement
        speed = 7
        dx = 0
        dy = 0
        #gravity
        G = 2

        # keyboard presses
        #controls different actions on diff key-presses
        key = pygame.key.get_pressed()

        #-----controls-----
        if self.atk_trig == False and self.death == False:

            #identifying the player:::
            if self.sm == 1:

                #left-right
                if key[pygame.K_a]:
                    dx = -speed
                    self.run =True
                if key[pygame.K_d]:
                    dx = speed
                    self.run =True
                
                
                #jump

                if key[pygame.K_w] and self.jump == False:
                    self.hor_dist = -23
                    self.jump = True

                #without gravity player will just go upwards
                #now we must define gravity
                #applying gravity
                self.hor_dist += G
                dy += self.hor_dist

            
                #attacks
                if key[pygame.K_i] or key[pygame.K_j] or key[pygame.K_l]:
                    self.atk(surface, opponent)
                    # attack type:

                    if key[pygame.K_i]:
                        self.atk_trig = True
                        self.atk_tp = 1
                    if key[pygame.K_j]:
                        self.atk_trig = True
                        self.atk_tp = 2
                    if key[pygame.K_l]:
                        self.atk_trig = True
                        self.atk_tp = 3
            
            
            if self.sm == 2:

                #left-right
                if key[pygame.K_LEFT]:
                    dx = -speed
                    self.run =True
                if key[pygame.K_RIGHT]:
                    dx = speed
                    self.run =True
                
                
                #jump

                if key[pygame.K_UP] and self.jump == False:
                    self.hor_dist = -23
                    self.jump = True

                #without gravity player will just go upwards
                #now we must define gravity
                #applying gravity
                self.hor_dist += G
                dy += self.hor_dist

            
                #attacks
                if key[pygame.K_n] or key[pygame.K_b] or key[pygame.K_m]:
                    self.atk(surface, opponent)
                    # attack type:

                    if key[pygame.K_n]:
                        self.atk_trig = True
                        self.atk_tp = 1
                    if key[pygame.K_b]:
                        self.atk_trig = True
                        self.atk_tp = 2
                    if key[pygame.K_m]:
                        self.atk_trig = True
                        self.atk_tp = 3

    #putting limit to ensure that players must stay only in the screen

        #if player is at the end of left side of the screen then player can not move further in the left direction
        if self.rect.left + dx < 0:
            dx = -self.rect.left
            

        #if player is at the end of the right side of the screen then player can not move further in the right direction
        if self.rect.right + dx > sc_width:
            dx = sc_width - self.rect.right

        #we must define ground surface for players otherwise the will fall down due to gravity
        #so basically her we are defining bottom limit
        if self.rect.bottom + dy > sc_height - 35:
            self.hor_dist = 0
            self.jump = False
            dy = sc_height - 35 - self.rect.bottom


        # new positions of players
        self.rect.x += dx
        self.rect.y += dy

        #checking if opponents facing each other 
        # if so then when player attack he must change his face to the opponent so attack can affect
        if opponent.rect.centerx > self.rect.centerx:
            self.reve = False
        else:
            self.reve = True

        #to check if attack has reached to the opponent
        #we must define region or range of an attack

    
    #defining method to identifying and creating animation
    def make_anim(self):

        #checking health::::
        if self.blood <= 0:
            self.death = 0
            self.death = True
            self.chk_clm(5)

        #identifying atks:
        elif self.atk_trig == True:
            
            if self.atk_tp == 1:
                
                pygame.mixer.music.load("ASSETS/AUDIO/atk1.mp3")
                pygame.mixer.music.play()
                self.chk_clm(4)
            elif self.atk_tp == 2:
                pygame.mixer.music.load("ASSETS/AUDIO/atk2.mp3")
                pygame.mixer.music.play()
                self.chk_clm(6)
            elif self.atk_tp == 3:
                pygame.mixer.music.load("ASSETS/AUDIO/atk3.mp3")
                pygame.mixer.music.play()
                self.chk_clm(0)
            

        #identifying jumping animation
        elif self.jump == True:
            self.chk_clm(3)
        #identifying animations
        elif self.run == True:
            self.chk_clm(2)
        else:
            self.chk_clm(self.deflt)
        #defining cool down var to cntrol rate of animation
        anm_cd = 100
        #updating image for animation
        self.img = self.anm_l[self.act][self.f_i]
        if (pygame.time.get_ticks() - self.time) > anm_cd:
            self.f_i += 1
            self.time = pygame.time.get_ticks()
        #finishing animation
        if self.f_i >= len(self.anm_l[self.act]):
            #end animation when player is dead :::
            if self.death == True:
                self.f_i = len(self.anm_l[self.act]) - 1
            else:
                self.f_i = 0
                #to finish atks
                if self.act == 4 or self.act == 6 or self.act == 0:
                    self.atk_trig = False

    def atk(self, surface, opponent):
        self.atk_trig = True 
        atk_range = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.reve), self.rect.y, 2*self.rect.width, self.rect.height)
        if atk_range.colliderect(opponent):
            opponent.blood -= 10
            print("shine")
        #this is temp to check the range of an attack
        #pygame.draw.rect(surface, (255,0,0), atk_range)
    

    #defining method for checking frames ::: comparing frame size of columns
    def chk_clm(self, n_act):
        if n_act != self.act:
            self.act = n_act
            #updating frame_index
            self.f_i = 0
            self.time = pygame.time.get_ticks()

    def frame_img(self, sprites, animations):

        #same steps can be done using the below method too :
        #------------------------------------------------------------
        
        # #we are creating outer loop to proceed the animation
        # vrt_d = 0
        # for anm in enumerate(animations):
              #creating list to store extracted frame_imges
        #`````tmp_list = []
        #     #extract frame from the image of each row for a specific action
        #     for h_d in range(anm):
        #         tmp = sprites.subsrface(h_d*self.size, vrt_d*self.size, self.size, self.size) #creating square frame to extract frames of rows to create animation from spritesheets
        #         tmp_list.append(tmp)
        #     vrt_d += 1


        #we are using this method instead using above method beacuase it is way better and neat
        
        #creating list to store animation of whole action
        anm_l = []
        #we are creating outer loop to proceed the animation
        for vrt_d, anm in enumerate(animations):
            #creating list to store extracted frame_imges
            tmp_list = []
            #extract frame from the image of each row for a specific action
            for h_d in range(anm):
                tmp = sprites.subsurface(h_d*self.size, vrt_d*self.size, self.size, self.size) #creating square frame to extract frames of rows to create animation from spritesheets
                tmp_list.append(pygame.transform.scale(tmp, (self.size * self.image_sc, self.size * self.image_sc)))
            anm_l.append(tmp_list)
        return anm_l
