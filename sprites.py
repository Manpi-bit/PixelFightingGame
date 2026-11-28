

import pygame as pg
import pytmx as pt
import ui
import random as rd


from settings import SCREEN_SIZE, load_image, BEAM_SIZE, LIGHTING_SIZE, CLOUD_SIZE, ICE_FLOOR_SIZE


class Character(pg.sprite.Sprite):
    def __init__(self, file, enemy = False, attack_power = 5):
        pg.sprite.Sprite.__init__(self)
        self.char_number = int(file[-5])
        self.enemy = enemy
        self.images = self.get_animation(file)
        self.image = self.images['idle'][0]
        self.health = 100
        self.enemy_rect = None
        self.ice_floor = None
        self.super_damage = 0
        self.Jump_power = -16
        self.rect = self.image.get_rect()
        self.collider = pg.rect.Rect(0, 0, self.rect.width // 2, self.rect.height // 2)
        if enemy:
            self.rect.center = (SCREEN_SIZE[0] - 250, 418)
            self.collider.center = self.rect.center
        else:
            self.rect.center = (250, 418)
            self.collider.center = self.rect.center
        self.timer = pg.time.get_ticks()
        self.mode = 'idle'
        self.action = 0
        self.index_image = 0
        self.is_jump = False
        self.ui_hp = ui.Hp_line(enemy)
        self.is_flip = False
        self.revers = False
        self.prev_action = 'idle'
        self.attack_power = attack_power
        self.beam = None
        self.lighting = None
        self.cloud = None
        self.once_super = 1

    def get_animation(self, file):
        animation = {}
        images = pt.util_pygame.load_pygame(file)
        for layer in images.layers:
            animation[layer.name] = []
            for x, y, gid in layer:
                tile = images.get_tile_image_by_gid(gid)
                if tile:
                    tile = pg.transform.scale(tile,(150, 150))
                    if self.enemy:
                        tile = pg.transform.flip(tile, True, False)
                    animation[layer.name].append(tile)
        return animation


    def draw(self, screen):
        if self.beam:
            self.beam.draw(screen)
        if self.lighting:
            self.lighting.draw(screen)
        if self.cloud:
            self.cloud.draw(screen)
        screen.blit(self.image, self.rect)
        self.ui_hp.draw(screen)
        if self.ice_floor:
            self.ice_floor.draw(screen)

    def event(self, event):
        if self.mode != 'Victory pose' and self.mode != 'Defeat':
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f and self.mode == 'idle':
                    self.mode = 'Hands attack'
                if event.key == pg.K_a and self.mode == 'idle':
                    self.mode = 'Move_back'
                    if not self.mode == 'Super attack':
                        if not self.is_jump:
                            self.rect.centery = 410
                if event.key == pg.K_SPACE and self.Jump_power < -15:
                    if  not self.mode == 'Super attack':
                        self.Jump_power = -15
                        self.is_jump = True
                if event.key == pg.K_d and self.mode == 'idle':
                    if not self.mode == 'Super attack':
                        self.mode = 'Move_forward'
                        if not self.is_jump:
                            self.rect.centery = 410
                if event.key == pg.K_q and self.mode == 'idle':
                    self.mode = 'Block'
                if event.key == pg.K_e and self.mode == 'idle' and not self.is_jump:
                    self.mode = 'Super attack'
            if event.type == pg.KEYUP:
                if not self.mode == 'Super attack':
                    if event.key == pg.K_a:
                        self.mode = 'idle'
                        if not self.is_jump:
                            self.rect.centery = 418
                if event.key == pg.K_d:
                    if not self.mode == 'Super attack':
                        self.mode = 'idle'
                        if not self.is_jump:
                            self.rect.centery = 418
                if event.key == pg.K_q:
                    if not self.mode == 'Super attack':
                        self.mode = 'idle'



    def update(self, enemy_rect):
        self.enemy_rect = enemy_rect
        if self.health <= 0:
            self.mode = 'Defeat'
        self.ui_hp.update(self.health)
        self.collider.center = self.rect.center

        if self.ice_floor:
            if pg.time.get_ticks() - self.ice_floor.timer >= 15000:
                self.ice_floor = None

        if self.is_jump and self.mode not in ['Damage', 'Hands attack', 'Super attack']:
            self.image = self.images['Jump'][self.index_image]
            self.revers = False
            self.rect.y += self.Jump_power
            self.Jump_power += 1
            if self.Jump_power > 16:
                self.Jump_power = -16
                self.is_jump = False
                self.rect.centery = 418

        if self.mode == 'Hands attack':
            if pg.time.get_ticks() - self.timer >= 200:
                if self.index_image < len(self.images['Hands attack']):
                    self.timer = pg.time.get_ticks()
                    self.image = self.images['Hands attack'][self.index_image]
                    self.revers = False
                    self.index_image += 1
                else:
                    self.mode = 'idle'
                    self.index_image = 0
                    self.image = self.images['idle'][self.index_image]
                    self.revers = False
        elif self.mode == 'Move_forward':
            self.image = self.images['Move'][1]
            self.revers = False
            if self.rect.right <= SCREEN_SIZE[0]:
                self.rect.x += 10

        elif self.mode == 'Move_back':
            self.image = self.images['Move'][0]
            self.revers = False
            if self.rect.left >= 0:
                self.rect.x -= 10

        elif self.mode == 'Damage':
            self.prev_action = "Damage"
            self.action = 0
            if self.index_image not in [0, 1]:
                self.index_image = 0
            self.image = self.images['Damage'][self.index_image]
            self.revers = False
            if pg.time.get_ticks() - self.timer >= 10 and self.index_image == 0:
                self.timer = pg.time.get_ticks()
                if self.index_image == 0:
                    self.index_image = 1
            elif pg.time.get_ticks() - self.timer >= 400 and self.index_image == 1:
                self.mode = 'idle'
                self.prev_action = 'idle'
                self.index_image = 0

        elif self.mode == 'Block':
            self.index_image = 0
            self.image = self.images['Block'][self.index_image]
            self.revers = False

        elif self.mode == 'Stun':
            self.index_image = 0
            self.image = self.images['Stun'][self.index_image]
            self.revers = False
            if self.prev_action != 'Stun':
                self.prev_action = 'Stun'
                self.timer = pg.time.get_ticks()
            elif pg.time.get_ticks() - self.timer >= 4000:
                self.mode = 'idle'



        elif self.mode == 'Defeat':
            self.index_image = 0
            self.image = self.images['Defeat'][self.index_image]
            self.revers = False
            self.beam = None
            self.ice_floor = None
            self.lighting = None

        elif self.mode == 'Victory pose':
            if self.prev_action != 'Victory pose':
                self.beam = None
                self.ice_floor = None
                self.lighting = None
                self.is_jump = False
                self.index_image = 0
                self.image = self.images['Victory pose'][self.index_image]
                self.revers = False
                self.prev_action = 'Victory pose'
                self.timer = pg.time.get_ticks()
            if pg.time.get_ticks() - self.timer >= 200:

                self.image = self.images['Victory pose'][self.index_image]
                if self.index_image < 3:
                    self.index_image += 1
                    self.timer = pg.time.get_ticks()


        elif self.mode == 'Super attack' and not self.is_jump:
            if self.once_super == 1:
                self.super_attack()
            else:
                self.mode = "idle"


        elif not self.is_jump and self.mode != 'Defeat' and self.mode != 'Victory pose':
            self.index_image = 0
            self.image = self.images['idle'][self.index_image]
            self.revers = False

        if self.is_flip and not self.revers:
            self.image = pg.transform.flip(self.image, True, False)
            self.revers = True

    def damage(self, damage):
        if self.char_number == 4 and self.mode != 'Block' and self.mode != 'Super attack' and self.prev_action != 'Damage':
            self.prev_action = 'Damage'
            self.mode = 'Damage'
            self.health -= damage
            self.index_image = 0



        elif self.mode != 'Block' and self.mode != 'Super attack' and self.char_number != 4:
            self.prev_action = 'Damage'
            self.mode = 'Damage'
            self.health -= damage
            self.index_image = 0

    def bot(self):

        # if self.mode == 'idle' and self.prev_action != 'Super attack':
        #     self.prev_action = 'Super attack'
        #     self.mode = 'Super attack'
        # if pg.time.get_ticks() - self.timer >= 1000:
        #     self.mode = 'Move_back'
        # if pg.time.get_ticks() - self.timer >= 2000:
        #     self.mode = 'Hands attack'
        if self.mode == 'idle':
            self.action = rd.randint(0, 100)
        if self.mode != 'Victory pose':
            if self.health <= 75 and self.once_super == 1 and self.mode != 'Damage':
                self.mode = 'Super attack'

            elif self.action > 80 and self.prev_action != 'Hands attack':
                self.mode = 'Hands attack'
                self.prev_action = 'Hands attack'
                self.timer = pg.time.get_ticks()
                self.action = 0
            elif self.action > 60:
                self.mode = 'Move_forward'
                self.prev_action = 'Move_forward'
                self.timer = pg.time.get_ticks()
                self.action = 0
            elif self.action > 40 :
                self.mode = 'Move_back'
                self.prev_action = "Move_back"
                self.timer = pg.time.get_ticks()
                self.action = 0


        if pg.time.get_ticks() - self.timer >= 1000 and self.action == 0 and self.mode != 'Victory pose' and self.mode != 'Stun' and self.mode != 'Damage':
            self.mode = 'idle'

    def flip(self, is_flip):
        self.is_flip = is_flip

    def super_attack(self):
        if self.char_number == 5:
            if pg.time.get_ticks() - self.timer >= 1000:
                if self.index_image < len(self.images['Super attack']):
                    self.timer = pg.time.get_ticks()
                    self.image = self.images['Super attack'][self.index_image]
                    self.revers = False
                    self.index_image += 1
                    if self.index_image == 2:
                        self.beam = Beam(self.collider, self.is_flip, self.enemy)
                else:
                    self.mode = 'idle'
                    self.index_image = 0
                    self.beam = None
                    self.once_super = 0
                    self.image = self.images['idle'][self.index_image]
                    self.revers = False
        if self.char_number == 4:
            if pg.time.get_ticks() - self.timer >= 150:
                if self.index_image < len(self.images['Super attack']):
                    self.timer = pg.time.get_ticks()
                    self.image = self.images['Super attack'][self.index_image]
                    self.revers = False
                    self.index_image += 1
                    if self.index_image == 2:
                        self.lighting = Lighting(self.enemy_rect)
                        self.cloud = Cloud()
                else:
                    self.mode = 'idle'
                    self.index_image = 0
                    self.lighting = None
                    self.once_super = 0
                    self.cloud = None
                    self.image = self.images['idle'][self.index_image]
                    self.revers = False

        if self.char_number == 3:
            if not self.ice_floor:
                self.index_image = 0
                self.image = self.images['Super attack'][self.index_image]
                self.timer = pg.time.get_ticks()
                self.ice_floor = Ice_floor()
            elif pg.time.get_ticks() - self.timer >= 1000:
                self.mode = 'idle'
                self.once_super = 0

            # else:
            #     self.index_image = 0
            #     self.image = self.images['Super attack'][self.index_image]
            #     self.


    def super_attack_damage(self, damage):
        if self.mode == "Block":
            damage //= 2
        else:
            #self.index_image = 0
            self.mode = "Damage"
        if self.super_damage < 10 and pg.time.get_ticks() - self.timer >= 300:
            self.super_damage += 1
            self.health -= damage//10
            self.timer = pg.time.get_ticks()
        else:
            self.super_damage = 0

    def fix_damage(self, damage):



        if self.prev_action != "Damage" and self.prev_action != "Stun":
            self.prev_action = "Damage"
            self.health -= damage

    def ice_damage(self, damage):
        self.health -= damage




class Beam(pg.sprite.Sprite):
    def __init__(self, rect, is_flip, enemy):
        pg.sprite.Sprite.__init__(self)
        print(is_flip)
        self.image = load_image("images/Beam.svg", BEAM_SIZE )
        self.rect = self.image.get_rect()
        self.rect.centery = rect.centery + 10
        self.is_flip = is_flip
        if (self.is_flip and not enemy) or (not self.is_flip and enemy):
            self.image = pg.transform.flip(self.image, True, False)
            self.rect.right = rect.left
        else:
            self.rect.left = rect.right

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Lighting(pg.sprite.Sprite):
    def __init__(self, enemy_rect):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image("images/Lighting.png", LIGHTING_SIZE)
        self.rect = self.image.get_rect()
        self.rect.centerx = enemy_rect.centerx

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Cloud(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image("images/Cloud.png", CLOUD_SIZE)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Ice_floor(pg.sprite.Sprite):
    def __init__(self):
        self.timer = pg.time.get_ticks()
        self.image = load_image("images/Ice_floor.png", ICE_FLOOR_SIZE)
        self.rect = self.image.get_rect()
        self.rect.y = 63
        self.rect.centerx = 450

    def draw(self, screen):
        screen.blit(self.image, self.rect)