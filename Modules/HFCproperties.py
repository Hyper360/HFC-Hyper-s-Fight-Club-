import pygame
import os
from Modules import text_reader, dialogue_and_timer, spritesheet, healthbar

pygame.font.init()
main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(main_dir)

DNT = dialogue_and_timer
SS = spritesheet
HB = healthbar
songfile = os.path.join(main_dir, "Sounds", "i-found-who-asked!.mp3")
white = 255
whitedecrease = False

songstart = False
ychange = -0.4

#Text
font = pygame.font.Font(os.path.join(main_dir, "Pictures", "PixeloidMono.ttf"), 30)
smallfont = pygame.font.Font(os.path.join(main_dir, "Pictures", "PixeloidMono.ttf"), 15)
mediumfont = pygame.font.Font(os.path.join(main_dir, "Pictures", "PixeloidMono.ttf"), 22)
presstartfont = pygame.font.Font(os.path.join(main_dir, "Pictures", "PixeloidMono.ttf"), 50)
fightfont = pygame.font.Font(os.path.join(main_dir, "Pictures", "BLKCHCRY.TTF"), 80)
versiontext = font.render('DEMONSTRATION VERSION 1', True, (255, 255, 255))
pressstart = presstartfont.render("Press space to start...", True, (250, 27, 6))
pressrect = pressstart.get_rect()
title = font.render("Hyper's Bootleg Trash Beginner Game", True, (250, 27, 6))
titlerect = title.get_rect()
background = pygame.image.load(os.path.join(main_dir, "Pictures", "City.png"))
background = pygame.transform.scale(background, (1000, 800))
base_font = pygame.font.Font(None, 32)
user_name = ''
name = None

#Namestart stuff
input_rect = pygame.Rect(450, 400, 140, 32)
color_active = pygame.Color("lightskyblue3")
color_passive = pygame.Color("gray50")
color = color_passive

enter_font = pygame.font.Font(os.path.join(main_dir, "Pictures", "PixeloidMono.ttf"), 32)
enter_text = "Enter"
enter_rect = pygame.Rect(430, 442, 140, 32)
enter_color = (255, 255, 255)

active = False
enter_active = False

welcomex = 50
welcomey = 100

readyx = 50
readyy = 500

#Setting up dialogue Characters and Healthbars
rock = DNT.DialogueCharacter(pygame.display.get_surface(), titlerect.left, 100, os.path.join(main_dir, "Pictures", "Sprite1.png"))
rock.change_image_size(360, 400)

cindy = DNT.DialogueCharacter(pygame.display.get_surface(), 0, 0, os.path.join(main_dir, "Pictures", "CindyNEUTRAL.png"))
cindy.change_image

noob_bot = DNT.DialogueCharacter(pygame.display.get_surface(), 0, 0, os.path.join(main_dir, "Pictures", "NoobBotANGRY.png"))
ridia_logo = DNT.DialogueCharacter(pygame.display.get_surface(), 0, 0, os.path.join(main_dir, "Pictures", "RIDIA_Logo.png"))
ridia_logo.change_image_size(500, 400)
dalia_logo = DNT.DialogueCharacter(pygame.display.get_surface(), 0, 0, os.path.join(main_dir, "Pictures", "DALIA_Logo.png"))
dalia_logo.change_image_size(500, 400)
HFClogo = DNT.DialogueCharacter(pygame.display.get_surface(), 0, 0, os.path.join(main_dir, "Pictures", "HFCLogo.png"))
HFClogo.change_image_size(400, 400)

rock_ani = SS.SpritesheetDraw(pygame.display.get_surface(), pygame.image.load(os.path.join(main_dir, "Pictures", "spritesheet.png")), 4, 150, x = 0, y=200)
bot_ani = SS.SpritesheetDraw(pygame.display.get_surface(), pygame.image.load(os.path.join(main_dir, "Pictures", "Noobspritesheet.png")), 4, 150, x = 800, y=400)


playerHB = HB.HealthBar(pygame.display.get_surface(), (rock_ani.x + rock_ani.frame_width, rock_ani.y + (rock_ani.frame_height/2)), 500, 400, 60, "Rock", True)
botHB = HB.HealthBar(pygame.display.get_surface(), (bot_ani.x - 400, bot_ani.y + (bot_ani.frame_height/2)), 250, 400, 60, "Bot", True)
testHB = HB.HealthBar(pygame.display.get_surface(), (500, 500), 300, 400, 50,'TEST', True, multiple_bars=3)

targets = []
sliderlist = []

#Misc.
center_rect = versiontext.get_rect(center=(1000 / 2, 800 / 2))
version_pos = versiontext.get_rect(center=(1000 / 2, 780))
normalfont = pygame.font.Font(os.path.join(main_dir, "Pictures", "PixeloidMono.ttf"), 30)
rockimg = pygame.image.load(os.path.join(main_dir, "Pictures", "Sprite1.png"))
rockimg = pygame.transform.scale(rockimg, (400, 400))
rockrect = rockimg.get_rect()


story_change = 1
storytext = ""
storysequence = 1

#Text reader for story
reader = text_reader.Text_Reader(os.path.join(main_dir, "Dialogue", "storyline.txt"))
story1reader = text_reader.Text_Reader(os.path.join(main_dir, "Dialogue", "storywbot.txt"))