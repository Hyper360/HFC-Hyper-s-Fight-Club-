# Importing Modules
import pygame
from pygame import mixer
import random
import sys
import os
# import cProfile

main_dir = os.path.dirname(__file__)

# Initializing pygame, mixer and starting the clock
pygame.init()
mixer.init()
clock = pygame.time.Clock()

# Setup
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags= pygame.DOUBLEBUF | pygame.HWSURFACE)
from Modules import spritesheet, HFCproperties, particles, fade, hitbar, healthbar, button, upgrade_items, upgrade_gui, draw_text, dialogue_and_timer
SS = spritesheet
HFC = HFCproperties
PAT = particles
FADE = fade
HB = healthbar
HITB = hitbar
BTN = button
UPGUI = upgrade_gui
UPGI = upgrade_items
DT = draw_text
DNT = dialogue_and_timer

screen_color = 150, 60, 60
icon = pygame.image.load(os.path.join(main_dir, "Pictures", "fightclubicon.jpg"))
pygame.display.set_caption("Hyper's Bootleg Trash Beginner Game RESMASTERED")
pygame.display.set_icon(icon)

# Setting up title placement
HFC.titlerect.y = 200

# Setting up the hitbar for fights
def final_hitbar():
    return_string = ''
    for target in HFC.targets:
        target.draw()
    for slider in HFC.sliderlist:
        slider.draw()
        if slider.space:
            return_string = slider.return_collision()
    
    return return_string

# Making a class that contains the entire game
class MainGame:
    def __init__(self):
        # Initializing important assets for the class
        self.state = 'intro'
        self.current_time = pygame.time.get_ticks()
        self.player_turn = True
        self.timer = DNT.Timer(1500)
        self.went = False
        self.rain = True
        self.weather_button = BTN.Button(screen, 950, 0, 50, 50, (150, 0, 0), os.path.join(main_dir, "Pictures", "Tree.png"))
        self.rain_noise = mixer.Sound(os.path.join(main_dir, "Sounds", "Rain_Sounds.mp3"))
        self.coins = 0
        self.font = HFC.font
        self.placeholder_image = pygame.image.load(os.path.join(main_dir, "Pictures", "None.png"))
        self.tutorial_prompt = pygame.image.load(os.path.join(main_dir, "Pictures", "TutorialPrompt.png"))
        self.tutorial_prompt = pygame.transform.scale(self.tutorial_prompt, (self.tutorial_prompt.get_width()/2, self.tutorial_prompt.get_height()/2) )

        self.categories_upg = UPGUI.Upgrade(UPGI.categories)
        self.weapons_upg = UPGUI.Upgrade(UPGI.categories, UPGI.weapons)
        self.armor_upg = UPGUI.Upgrade(UPGI.categories, UPGI.armor)

        self.catlist = self.categories_upg.return_categories()
        self.weapons_list = self.weapons_upg.return_items()
        self.armor_list = self.armor_upg.return_items()

        self.main_gui = UPGUI.UpgradeGUI(screen, self.catlist, 0, 100, 400, 100)
        self.weapons_gui = UPGUI.UpgradeGUI(screen, self.weapons_list, 500, 100, 400, 100)
        self.armor_gui = UPGUI.UpgradeGUI(screen, self.armor_list, 500, 100, 400, 100)

        self.b = BTN.Button(screen, 700, 0, 50, 50, (100, 200, 100), None)

    def intro(self):
        # Setting up the current time (used for timed events)
        self.current_time = pygame.time.get_ticks()
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # When space is pressed, the screen faded to black
                    FADE.fadetoblack(WIDTH, HEIGHT, 100)
        # Handling background music
        if HFC.songstart == False:
            mixer.music.load(HFC.songfile)
            mixer.music.play(-1)
            HFC.songstart = True
        if HFC.songstart == True:
            pass

        # Filling the screen black, and positioning the title, presstart text, version text
        screen.fill((0,0,0))
        screen.blit(HFC.title, (270, HFC.titlerect.y))
        screen.blit(HFC.pressstart, (HFC.pressrect.x, 650))
        screen.blit(HFC.versiontext, (HFC.version_pos))
        HFC.pressrect.centerx = WIDTH/2
        HFC.titlerect.y += HFC.ychange
        HFC.HFClogo.change_pos(HFC.HFClogo.x, HFC.HFClogo.y + HFC.ychange) 
        
        # If the y-axis of the title's rectangle is below 200 pixels, the title will start moving down
        if HFC.titlerect.y <= 200:
            HFC.ychange = 1
        # If the y-axis of the title's rectangle is above 300 pixels, the title will start moving up
        elif HFC.titlerect.y >= 300:
            HFC.ychange = -1
    
        HFC.HFClogo.draw()
        #When the screen finished fading, the game state changes
        if FADE.fadeend == True:
            self.state = 'namestart'
            HFC.songfile = os.path.join(main_dir, "Sounds", "whatsyourname.mp3")
            HFC.songstart = False
        
    def namestart(self):
        # Setting up the current time (used for timed events)
        self.current_time = pygame.time.get_ticks()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # If you click the input rectangle, it will become active and availabe to type in
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HFC.input_rect.collidepoint(event.pos):
                    HFC.active = True
                else:
                    HFC.active = False

            # If the input rectangle is active, you can edit the contents by typing
            if event.type == pygame.KEYDOWN:
                if HFC.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        HFC.user_name = HFC.user_name[:-1]
                    else:
                        HFC.user_name += event.unicode

            # Color of the rectangle changes based on activity
            if HFC.active == True:
                HFC.color = HFC.color_active
            else:
                HFC.color = HFC.color_passive

            # If enter is pressed, enter active is true
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HFC.enter_rect.collidepoint(event.pos):
                    HFC.enter_active = True

            # If enter active is true, the game prepares to switch states
            if HFC.enter_active == True:
                self.state = 'main_storyline'
                self.rain = False
                self.rain_noise.stop()
                PAT.rainparticles.clear()
                PAT.snowparticles.clear()
                HFC.songfile = os.path.join(main_dir, "Sounds", "Orgins.mp3")
                HFC.songstart = False

        # Filling the bacground with the bacground image as stated in the HFCproperties module
        screen.blit(HFC.background, (0,0))

        # If it is raining, the bacground will be a forest, otherwise the baground will be a snowy forest
        if self.rain == True:
            HFC.background = pygame.image.load(os.path.join(main_dir, "Pictures", "Forest.png"))
            HFC.background = pygame.transform.scale(HFC.background, (1000, 800))
        elif self.rain == False:
            HFC.background = pygame.image.load(os.path.join(main_dir, "Pictures", "Forest_Snow.png"))
            HFC.background = pygame.transform.scale(HFC.background, (1000, 800))
        
        # Music, and sound handling
        if HFC.songstart == False:
            mixer.music.load(HFC.songfile)
            mixer.music.play(-1)
            if self.rain == True:
                self.rain_noise.play(-1)
            else:
                self.rain_noise.stop()
            HFC.songstart = True
        if HFC.songstart == True:
            pass
        
        # Drawing the weather button
        self.weather_button.draw()

        # If the weather button is pressed, all particles on the screen, rain or snow will be deleted
        if self.weather_button.pressed:
            self.rain = not self.rain
            PAT.rainparticles.clear()
            PAT.snowparticles.clear()
        if self.rain == True:
            # Rain will start falling
            PAT.DrawRainParticles(screen)
        elif self.rain == False:
            # Snow will start falling
            PAT.DrawSnowParticles(screen)

        DT.blit_text(screen, "This is the beginning of your adventure What will be your username? (Canon name will always be Rock)", (55, 50), HFC.font)

        # Input rectangle that grows depending on how many characters are inside the rectangle
        pygame.draw.rect(screen, HFC.color, HFC.input_rect, 2)
        text_surface = HFC.base_font.render(HFC.user_name, True, (255, 255, 255))
        screen.blit(text_surface, (HFC.input_rect.x + 5, HFC.input_rect.y + 5))
        HFC.input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.draw.rect(screen, HFC.enter_color, HFC.enter_rect, 0)
        enter_surface = HFC.enter_font.render(HFC.enter_text, True, (0, 0, 0))
        screen.blit(enter_surface, (440, 440))

        HFC.input_rect.centerx = WIDTH/2
        # Snow or rain?
        if self.rain == True:
            # The numbers in randint set the density of the rain. 15 and 15 is the best most optimal choice
            for x in range(random.randint(15, 15)):
                # For each particle created, it will add the particle to a list
                particle = PAT.RainParticle(random.randint(0, 1000), -100, random.randint(-10, 10)/10, random.randint(-3, -1), random.randint(3, 5), (192,225,228), 0.5)
                PAT.rainparticles.append(particle)
            # Same thing happens with snow
        elif self.rain == False:
            for x in range(random.randint(1, 3)):
                particle = PAT.SnowParticle(random.randint(0, 1000), -20, random.randint(-20, 20)/10, random.randint(-3, -1), random.randint(3, 8), (192,225,228), 0.05)
                PAT.snowparticles.append(particle) 

    def main_storyline(self):
        if HFC.songstart == False:
            mixer.music.load(HFC.songfile)
            mixer.music.play(-1)
            HFC.songstart = True
        if HFC.songstart == True:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    HFC.reader.next_line()
                    pygame.mixer.Sound(os.path.join(main_dir, "Sounds", "Skip.mp3")).play(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    HFC.reader.last_line()
                if event.key == pygame.K_c:
                    if HFC.reader.final_line == True:
                        HFC.rock.change_pos(100, 100)
                        HFC.rock.change_image(os.path.join(main_dir, "Pictures", "RockNEUTRAL.png"))
                        HFC.cindy.change_image(os.path.join(main_dir, "Pictures", "None.png"))
                        HFC.cindy.change_pos(600, 100)
                        self.state = 'storyline1'
                        self.rain_noise.stop()
                        HFC.songfile = os.path.join(main_dir, "Sounds", "obnoxious.mp3")
                        HFC.songstart = False
                        HFC.background = pygame.image.load(os.path.join(main_dir, "Pictures", "Office.png"))
                        HFC.background = pygame.transform.scale(HFC.background, pygame.display.get_window_size())
        screen.fill((0, 0, 0))
        DT.blit_text(screen, HFC.reader.read_cur_text(), (0, 400), pygame.font.Font(os.path.join(main_dir, "Pictures", "PixeloidMono.ttf"), 25))

        if HFC.reader.final_line != True:
            DT.blit_text(screen, "Click to continue...", (5, 780), HFC.smallfont)
        elif HFC.reader.final_line == True:
            DT.blit_text(screen, "Press 'c' to continue...", (5, 780), HFC.smallfont)

        if HFC.reader.ind == 12:
            HFC.ridia_logo.draw()
        elif HFC.reader.ind == 21:
            HFC.dalia_logo.draw()
        
    def storyline1(self):
        self.current_time = pygame.time.get_ticks()
        if HFC.songstart == False:
            mixer.music.load(HFC.songfile)
            mixer.music.play(-1)
            HFC.songstart = True
        if HFC.songstart == True:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    HFC.story1reader.next_line()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if HFC.story1reader.final_line == True:
                        HFC.songstart = False
                        HFC.songfile = os.path.join(main_dir, "Sounds", "FightingAFrigginBot.mp3")
                        HFC.background = pygame.image.load(os.path.join(main_dir, "Pictures", "Forest.png"))
                        HFC.background = pygame.transform.scale(HFC.background, pygame.display.get_window_size())
                        self.state = 'fight'
                if event.key == pygame.K_x:
                    HFC.story1reader.last_line()
        
        screen.fill((0, 0, 0))
        screen.blit(HFC.background, (0,0))
        DT.blit_text(screen, "Welcome " + HFC.user_name + " to Hyper's Fight Club", (HFC.welcomex, HFC.welcomey), HFC.font)

        if HFC.story1reader.final_line != True:
            DT.blit_text(screen, "Click to continue...", (5, 780), HFC.smallfont)
        elif HFC.story1reader.final_line == True:
            DT.blit_text(screen, "Press 'c' to continue...", (5, 780), HFC.smallfont)
            
        HFC.rock.draw()
        HFC.cindy.draw()
        with open(os.path.join(main_dir, "Dialogue", "storywbotcode.txt"), 'r') as f:
            story_code = f.read()
            exec(story_code)
        
        PAT.DrawRainParticles(screen)
          
        DT.blit_text(screen, HFC.story1reader.read_cur_text(), (0, 550), pygame.font.Font(os.path.join(main_dir, "Pictures", "PixeloidMono.ttf"), 30))

    def fight(self):
        self.timer.update(self.current_time)
        self.current_time = pygame.time.get_ticks()
        screen.fill((200,200,200))
        screen.blit(HFC.background, (0,0))
        if HFC.songstart == False:
            mixer.music.load(HFC.songfile)
            mixer.music.play(-1)
            self.rain_noise.play(-1)
            HFC.songstart = True
        if HFC.songstart == True:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    if self.player_turn:
                        if len(HFC.targets) < 1 and len(HFC.sliderlist) < 1:
                            self.went = True
                            HFC.targets.append(HITB.Target(screen, WIDTH/2, HEIGHT/2, WIDTH, HEIGHT))
                            HFC.sliderlist.append(HITB.Slider(screen, 5, HFC.targets[0], HEIGHT))
                        
        if self.player_turn == False:
            if self.timer.signal:
                HFC.playerHB.deduct_health(random.randint(20, 35))
                self.timer.reset(self.current_time)
                self.player_turn = True

        with open(os.path.join(main_dir, "text_code", "fight1.txt"), 'r') as f:
            code = f.read()
            exec(code)
        
        DT.blit_text(screen, "ROCK \n vs \n BOT", (WIDTH/2 - HFC.fightfont.get_linesize(), 0), HFC.fightfont, (255, 0, 0))
        HFC.rock_ani.draw(self.current_time)
        HFC.bot_ani.draw(self.current_time)
        HFC.playerHB.draw()
        HFC.botHB.draw()

        # RAIN!!!
        for x in range(random.randint(15, 15)):
                # For each particle created, it will add the particle to a list
                particle = PAT.RainParticle(random.randint(0, 1000), -100, random.randint(-10, 10)/10, random.randint(-3, -1), random.randint(3, 5), (192,225,228), 0.5)
                PAT.rainparticles.append(particle)
        PAT.DrawRainParticles(screen)
        screen.blit(self.tutorial_prompt, (0, 500))

        if HFC.botHB.health <= 0:
            self.state = 'upgrade'
            HFC.songfile = os.path.join(main_dir, "Sounds", "Lift_(To_Improve_Oneself).mp3")
            HFC.songstart = False
            self.rain_noise.stop()
            PAT.rainparticles.clear()
            HFC.background = pygame.image.load(os.path.join(main_dir, "Pictures", "Upgrade_Bck.png"))
            HFC.background = pygame.transform.scale(HFC.background, pygame.display.get_window_size())

    def upgrade_shop(self):
        screen.fill((0,0,0))
        screen.blit(HFC.background, (0,0))
        if HFC.songstart == False:
            mixer.music.load(HFC.songfile)
            mixer.music.play(-1)
            HFC.songstart = True
        if HFC.songstart == True:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.main_gui.event_handling(event)
            self.armor_gui.event_handling(event)
            self.weapons_gui.event_handling(event)
        
        self.main_gui.update()
        if self.main_gui.return_selection() == "Armor":
            self.armor_gui.update()
            armor_descr = self.font.render(self.armor_upg.target(self.main_gui.return_selection(), self.armor_gui.return_selection(), 1), True, (0,0,0), (200, 200, 200))
            screen.blit(armor_descr, (0, 500))
        elif self.main_gui.return_selection() == "Weapons":
            self.weapons_gui.update()
            weapons_descr = self.font.render(self.weapons_upg.target(self.main_gui.return_selection(), self.weapons_gui.return_selection(), 1), True, (0,0,0), (200, 200, 200))
            screen.blit(weapons_descr, (0, 500))

        self.b.draw()
        if self.b.pressed == True:
            if self.main_gui.return_selection() == "Armor":
                var = self.armor_gui.return_selection()
                HFC.playerHB.change_armor(var, self.armor_upg.target(self.main_gui.return_selection(), self.armor_gui.return_selection(), 2))
            elif self.main_gui.return_selection() == "Weapons":
                var = self.weapons_gui.return_selection()
                HFC.playerHB.change_weapons(var, self.weapons_upg.target(self.main_gui.return_selection(), self.weapons_gui.return_selection(), 2))
            HFC.rock.change_pos(100, 100)
            HFC.rock.change_image(os.path.join(main_dir, "Pictures", "RockNEUTRAL.png"))
            HFC.noob_bot.change_pos(600, 100)
            # self.state = 'storyline1'
            self.rain_noise.stop()
            HFC.songfile = os.path.join(main_dir, "Pictures", "obnoxious.mp3")
            HFC.songstart = False
            pygame.quit()

    def state_manager(self):
        # profile = cProfile.Profile()
        # profile.enable()
        if self.state == 'intro':
            self.intro()
        if self.state == 'namestart':
            self.namestart()
        if self.state == 'main_storyline':
            self.main_storyline()
        if self.state == 'storyline1':
            self.storyline1()
        if self.state == 'fight':
            self.fight()
        if self.state == 'upgrade':
            self.upgrade_shop()
        # profile.disable()
        # profile.dump_stats('HFCProfiler.prof')

game_state = MainGame()
if __name__ == '__main__':
    
    while True:
        game_state.state_manager()
        DT.blit_text(screen, str(round(clock.get_fps())) + " fps", (0,0), HFC.smallfont, (255, 0, 0))
        clock.tick(60)
        pygame.display.update()