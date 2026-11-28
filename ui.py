from settings import *

class Hp_line:
    def __init__(self, enemy = False):
        self.font = pg.font.Font('Pixsel_font.ttf', 20)
        self.rect = pg.rect.Rect(0,0,0,0)
        self.text = '100'
        self.enemy = enemy
        self.image = pg.Surface((0,0))

        padding = 5

        self.black_polygon = [[SCREEN_SIZE[0] // 20 - padding * 3, SCREEN_SIZE[1] // 10 + padding],
                            [SCREEN_SIZE[0] // 12 - padding, SCREEN_SIZE[1] // 20 - padding],
                            [SCREEN_SIZE[0] // 2.3 + padding * 3, SCREEN_SIZE[1] // 20 - padding],
                            [SCREEN_SIZE[0] // 2.5 + padding, SCREEN_SIZE[1] // 10 + padding],]

        self.red_polygon = [[SCREEN_SIZE[0]//20, SCREEN_SIZE[1]//10],
                            [SCREEN_SIZE[0]//12, SCREEN_SIZE[1]//20],
                            [SCREEN_SIZE[0]//2.3, SCREEN_SIZE[1]//20],
                            [SCREEN_SIZE[0] // 2.5, SCREEN_SIZE[1] // 10]]

        self.green_polygon = [[SCREEN_SIZE[0]//20, SCREEN_SIZE[1]//10],
                            [SCREEN_SIZE[0]//12, SCREEN_SIZE[1]//20],
                              [SCREEN_SIZE[0] // 2.3, SCREEN_SIZE[1] // 20],
                              [SCREEN_SIZE[0] // 2.5, SCREEN_SIZE[1] // 10]]

        self.green_polygon_hp = [[SCREEN_SIZE[0] // 20, SCREEN_SIZE[1] // 10],
                              [SCREEN_SIZE[0] // 12, SCREEN_SIZE[1] // 20],
                              [SCREEN_SIZE[0] // 2.3, SCREEN_SIZE[1] // 20],
                              [SCREEN_SIZE[0] // 2.5, SCREEN_SIZE[1] // 10]]

        for i in range(4):
            self.red_polygon[i][0] += SCREEN_SIZE[0]//15
            self.green_polygon[i][0] += SCREEN_SIZE[0] // 15
            self.green_polygon_hp[i][0] += SCREEN_SIZE[0] // 15
            self.black_polygon[i][0] += SCREEN_SIZE[0] // 15

        if self.enemy:
            for i in range(4):
                self.red_polygon[i][0] += SCREEN_SIZE[0] // 2.5
                self.green_polygon[i][0] += SCREEN_SIZE[0] // 2.5
                self.green_polygon_hp[i][0] += SCREEN_SIZE[0] // 2.5
                self.black_polygon[i][0] += SCREEN_SIZE[0] // 2.5

    def draw(self, screen):
        pg.draw.polygon(screen, 'black', self.black_polygon)
        pg.draw.polygon(screen, 'red', self.red_polygon)
        pg.draw.polygon(screen, 'green', self.green_polygon_hp)
        screen.blit(self.image, self.rect)

    def update(self, hp):
        if hp >= 0:
            self.text = str(int(hp)) + '%'
            self.image = self.font.render(self.text, True, (0,0,0))
            width = int((self.green_polygon[2][0] - self.green_polygon[1][0])/100 * hp)
            self.rect = self.image.get_rect()
            self.rect.midright = (0, (self.red_polygon[0][1] - self.red_polygon[1][1])// 2 + self.red_polygon[1][1])
            if self.enemy:
                self.green_polygon_hp[0][0] = self.green_polygon[3][0] - width
                self.green_polygon_hp[1][0] = self.green_polygon[2][0] - width
                self.rect.right = self.red_polygon[3][0]
            else:
                self.green_polygon_hp[3][0] = self.green_polygon[0][0] + width
                self.green_polygon_hp[2][0] = self.green_polygon[1][0] + width
                self.rect.left = self.red_polygon[1][0]

class VictoryAndDefeat:
    def __init__(self, image, text, level_event):
        self.image = load_image(image, (190,60))
        self.rect = self.image.get_rect()
        self.font = pg.font.Font('Pixsel_font.ttf', 45)
        self.text = self.font.render(text, True, (0,0,0))
        self.text_rect = self.text.get_rect()
        self.rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 150)
        self.text_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 150)
        self.button_retry = Button('Retry', (SCREEN_SIZE[0]//2 + 100, SCREEN_SIZE[1]//2 - 50),level_event)
        self.button_main_menu = Button('Menu', (SCREEN_SIZE[0]//2 - 100, SCREEN_SIZE[1]//2 - 50),  MAIN_MENU_EVENT)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        self.button_retry.draw(screen)
        self.button_main_menu.draw(screen)

    def event(self, event):
        self.button_main_menu.event(event)
        self.button_retry.event(event)