import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image

class SpritesheetDraw():
    def __init__(self, screen, image, steps, cooldown, x = 0, y = 0, action = 0, frame_width = 256, frame_height = 256):
        self.x = x
        self.y = y
        self.animation_list = []
        self.screen = screen
        self.steps = [steps]
        self.action = action
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = cooldown
        self.frame = 0
        self.step_counter = 0
        self.sprite_sheet_image = image
        self.sprite_sheet = SpriteSheet(image)
        self.frame_width = frame_width
        self.frame_height = frame_height
        for animation in self.steps:
            self.temp_img_list = []
            for _ in range(animation):
                self.temp_img_list.append(self.sprite_sheet.get_image(self.step_counter, self.frame_width, self.frame_height, 1, (255, 255, 255)))
                self.step_counter += 1
            self.animation_list.append(self.temp_img_list)

    def draw(self, current_time):
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0
        try:
            self.screen.blit(self.animation_list[self.action][self.frame], (self.x, self.y))
        except:
            self.action = 1
            self.frame = 1
            self.screen.blit(self.animation_list[self.action][self.frame], (self.x, self.y))
        # self.screen.blit(self.sprite_sheet.get_image(self.step_counter, 256, 256, 1, (255, 255, 255)), (500, 0))