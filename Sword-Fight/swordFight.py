import pygame
from pygame import mixer
from swordMen import swordMen

mixer.init()

pygame.init()


#importing music:::

pygame.mixer.music.load("ASSETS/AUDIO/intro.mp3")
pygame.mixer.music.play()
#atk_sndInt = pygame.mixer.music.load("ASSETS/AUDIO/intro.mp3")
#defining colors
Green = (0,255,0)
Red = (255,0,0)
White = (255,255,255)
light_blue = (102, 255, 255)

#timer :::
count = 6
count_m = 7
last_cnt = pygame.time.get_ticks()


#condition for player if it's flipped or not !!!!
S1_F = False
S2_F = True

#creating frame size to extract each frame from the sprites
#s-1:\
S1_S = 250
#s-2:\
S2_S = 126

#defining size of players
#size/scale of player-1
S1_SC = 2
#size/scale of player-2
S2_SC = 3.5

#defining offsets / positions for players
#player - 1
S1_OS = [125,96]
#player - 2
S2_OS = [50,35]

#defining default idle frame for each players
DEF_ANM_S1 = 1
DEF_ANM_S2 = 1

#creating list to contain frames to make an animation
L_S1 = [S1_S, S1_SC, S1_OS, S1_F, DEF_ANM_S1]
L_S2 = [S2_S, S2_SC, S2_OS, S2_F, DEF_ANM_S2]

#create a window where game will be run

SCREEN_WIDTH = 1460
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#setting an icon for our game
icon_img = pygame.image.load("Images/icon.png")
pygame.display.set_icon(icon_img)
pygame.display.set_caption("ONI-GIRI")

# without frame rate movements will be very fast
#so to control movement speed we must declare framerate
clock = pygame.time.Clock()
FPS = 60

#creating timer :::
c_f = pygame.font.Font("ASSETS/FONTS/kashima demo (1).otf", 80)
game_over = False

#creating msg:::
def msg(mssg, font, color, x, y):
    image = font.render(mssg, True, color)
    screen.blit(image, (x,y))


#creating background
bg_img = pygame.image.load("Images/bg7.jpg").convert_alpha()

#creating function to call background we have crwated earlier
def create_bg():
    scaled_bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

#creating display area of blood for each player
def create_blood_dis(blood,color, x, y):
    dec = blood / 100
    pygame.draw.rect(screen, light_blue, (x, y ,400,30))
    pygame.draw.rect(screen, color, (x, y, 400 * dec, 30))

#create players' graphic by importing spritesheets of characters
sM1_sheet = pygame.image.load("ASSETS/SWORD_MEN_1/S_M_1.png").convert_alpha()
sM2_sheet = pygame.image.load("ASSETS/SWORD_MEN_2/S_M_2_N.png").convert_alpha()
# scaled1 = pygame.transform.scale(sM1_sheet_img, (200,200))
# scaled2 = pygame.transform.scale(sM2_sheet_img, (100, 100))
# sM1_sheet = scaled1.convert_alpha()
# sM2_sheet = scaled2.convert_alpha()
#mixing sprites to make whole animation
#creating list of frames for each action
SM1_animation = [13,2,8,3,16,7,15]
SM2_animation = [10,6,7,6,9,8,3,11]

#creating sword-Men
s_men1 = swordMen(200,600,L_S1,sM1_sheet,SM1_animation, 1)
s_men2 = swordMen(1200,600,L_S2,sM2_sheet,SM2_animation, 2)


# to run game continuosly we are making loop
Flag = True
while Flag:
    
    #setting framerate
    #we must define the frame rate to choose how smooth we want our movements
    clock.tick(FPS)

    #create bg
    create_bg()

    #display status of players
        #our player's blood will be green and on the left side of the screen on the top
    create_blood_dis(s_men1.blood,Green, 20, 20)
        #opponents' blood will be red and on the right side of the screen on the top
    create_blood_dis(s_men2.blood,Red, 1040,20)

    #start timer :::

    if count_m <= 0:

        # control sword-men

        s_men1.actions(SCREEN_WIDTH,SCREEN_HEIGHT,screen, s_men2)
        s_men2.actions(SCREEN_WIDTH,SCREEN_HEIGHT,screen, s_men1)
        #s_men2.actions(SCREEN_WIDTH,SCREEN_HEIGHT)

    else:
        if count > 0:
            msg(str(count), c_f, White, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        else:
            if count_m > 0:
                msg("Fight",c_f,White, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_cnt) >= 1000:
            count -= 1
            count_m -= 1
            last_cnt = pygame.time.get_ticks()

    #for animation we need to take upadated image
    s_men1.make_anim()
    s_men2.make_anim()

    #create sword-Men
    s_men1.sketch(screen)
    s_men2.sketch(screen)


    #making sure that game is over and game cool down :::
    if game_over == False:
        if s_men1.death == True:
            game_over = True
            game_over_time = pygame.time.get_ticks()
        elif s_men2.death == True:
            game_over = True
            game_over_time = pygame.time.get_ticks()
    else:
        msg("VICTORY",c_f,White,360,360)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Flag=False

    
    #updates
    pygame.display.update()

pygame.quit()