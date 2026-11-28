import pygame as pg
pg.init()


def load_image(image_path, size):
    image = pg.image.load(image_path)
    image = pg.transform.scale(image, size)
    return image

SCREEN_SIZE = (900, 575)
BEAM_SIZE = (900, 20)
LIGHTING_SIZE = (465, 465)
CLOUD_SIZE = (900, 900)
ICE_FLOOR_SIZE = (800, 450)
BG_Menu = load_image('images/Background_Menu.png', SCREEN_SIZE)
LEVEL_MENU_EVENT = pg.USEREVENT + 1
LEVEL1_EVENT = pg.USEREVENT + 2
MAIN_MENU_EVENT = pg.USEREVENT + 3
LEVEL2_EVENT = pg.USEREVENT + 4
LEVEL3_EVENT = pg.USEREVENT + 5
CREATORS_EVENT = pg.USEREVENT + 6
SETTINGS_EVENT = pg.USEREVENT + 7


class Button:
    def __init__(self, text, center, event = None):
        self.text = text
        self.font = pg.font.Font('Pixsel_font.ttf', 40)
        self.image_text = self.font.render(self.text, True, 'black')
        self.image_rect = self.image_text.get_rect(center=center)
        self.is_active = True
        self.button_event = event

        self.rect1 = pg.rect.Rect(0, 0, 190, 60)
        self.rect2 = pg.rect.Rect(0, 0, 180, 70)
        self.rect3 = pg.rect.Rect(0, 0, 170, 80)
        self.rect4 = pg.rect.Rect(0, 0, 175, 60)

        self.rect1.center = center
        self.rect2.center = center
        self.rect3.center = center
        self.rect4.center = center

    def draw(self, screen):
        if self.is_active:
            pg.draw.rect(screen, "black", self.rect1)
            pg.draw.rect(screen, "black", self.rect2)
            pg.draw.rect(screen, "black", self.rect3)
            pg.draw.rect(screen, pg.Color(39, 120, 10), self.rect4)
            screen.blit(self.image_text, self.image_rect)

    def click(self):
        if self.button_event:
            pg.event.post(pg.event.Event(self.button_event))

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect4.collidepoint(event.pos):
                self.click()

class Game_menu:
    def __init__(self):
        self.button_play = Button('Play', (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//3), LEVEL_MENU_EVENT)
        self.button_settings = Button('Settings', (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2), SETTINGS_EVENT)
        self.button_creators = Button('Creators', (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//1.5), CREATORS_EVENT)

    def event(self, event):
        self.button_play.event(event)
        self.button_settings.event(event)
        self.button_creators.event(event)

    def draw(self, screen):
        self.button_play.draw(screen)
        self.button_settings.draw(screen)
        self.button_creators.draw(screen)

    def update(self):
        pass

class Levels_menu:
    def __init__(self):
        self.button_level1 = Button('Level 1', (SCREEN_SIZE[0]//4, SCREEN_SIZE[1]//2), LEVEL1_EVENT)
        self.button_level2 = Button('Level 2', (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2), LEVEL2_EVENT)
        self.button_level3 = Button('Level 3', (SCREEN_SIZE[0]//4 * 3, SCREEN_SIZE[1]//2), LEVEL3_EVENT)
        self.button_return = Button('Return', (SCREEN_SIZE[0]//8.5, SCREEN_SIZE[1]//1.1),MAIN_MENU_EVENT)

    def draw(self, screen):
        self.button_level1.draw(screen)
        self.button_level2.draw(screen)
        self.button_level3.draw(screen)
        self.button_return.draw(screen)

    def event(self, event):
        self.button_level1.event(event)
        self.button_level2.event(event)
        self.button_level3.event(event)
        self.button_return.event(event)

    def update(self):
        pass
