import pygame as pg

from levels import *
from settings import *
from sprites import *
from ui import VictoryAndDefeat

screen = pg.display.set_mode(SCREEN_SIZE)
running = True
game_menu = Game_menu()
player =  None
enemy = None
foreground = None
victory_and_defeat = None
level_event = None


while running:
    for event in pg.event.get():
        game_menu.event(event)
        if event.type == MAIN_MENU_EVENT:
            game_menu = Game_menu()
            player = None
            enemy = None
            victory_and_defeat = None
        if event.type == pg.QUIT:
            running = False
        if event.type == LEVEL_MENU_EVENT:
            game_menu = Levels_menu()
        if event.type == LEVEL1_EVENT:
            game_menu = Level('maps/Level_1.tmx')
            player = Character('images/characters/Char5.tmx', False, 5)
            enemy = Character('images/characters/Char3.tmx', True, 7.5)
            foreground = Foreground()
            level_event = LEVEL1_EVENT

            victory_and_defeat = None
        if event.type == LEVEL2_EVENT:
            game_menu = Level_2('maps/Level_2.tmx')
            player = Character('images/characters/Char3.tmx', False, 7.5)
            enemy = Character('images/characters/Char4.tmx', True, 7.5)
            level_event = LEVEL2_EVENT
            foreground = None

            victory_and_defeat = None

        if event.type == LEVEL3_EVENT:
            game_menu = Level_3('maps/Level_3.tmx')
            player = Character('images/characters/Char4.tmx', False, 7.5)
            enemy = Character('images/characters/Char5.tmx', True, 5)
            level_event = LEVEL3_EVENT
            foreground = None

            victory_and_defeat = None
        if event.type == CREATORS_EVENT:
            game_menu = Slide_show()

        if event.type == SETTINGS_EVENT:
            game_menu = Settings_LOL()

        if player:
            player.event(event)
            if player.rect.centerx > enemy.rect.centerx:
                player.flip(True)
                enemy.flip(True)
            else:
                player.flip(False)
                enemy.flip(False)
        if victory_and_defeat:
            victory_and_defeat.event(event)

    if player:
        enemy.bot()
        player.update(enemy.rect)
        enemy.update(player.rect)
        if enemy.health <= 0 and not victory_and_defeat:
            victory_and_defeat = VictoryAndDefeat('images/Victory.svg', 'Victory', level_event)
            player.mode = 'Victory pose'
        if player.health <= 0 and not victory_and_defeat:
            victory_and_defeat = VictoryAndDefeat('images/Defeat.svg', 'Defeat', level_event)
            enemy.mode = 'Victory pose'



        if player.mode == 'Hands attack' and enemy.mode != 'Damage':
            if player.collider.colliderect(enemy.collider):
                enemy.damage(player.attack_power)

        if enemy.mode == 'Hands attack' and player.mode != 'Damage':
            if enemy.collider.colliderect(player.collider):
                player.damage(enemy.attack_power)

        if player.mode == 'Super attack':
            if player.beam:
                enemy.super_attack_damage(40)
            if player.lighting:
                enemy.fix_damage(25)
                enemy.mode = 'Stun'
        if player.ice_floor:
            enemy.ice_damage(0.0465)

        if enemy.mode == 'Super attack':
            if enemy.beam:
                player.super_attack_damage(40)
            if enemy.lighting:
                player.fix_damage(25)
                player.mode = 'Stun'
        if enemy.ice_floor:
            player.ice_damage(0.0465)

    game_menu.update()
    screen.blit(BG_Menu,(0,0))
    game_menu.draw(screen)
    if player:

        player.draw(screen)
        enemy.draw(screen)
        if foreground:
            foreground.draw(screen)


    if victory_and_defeat:
        victory_and_defeat.draw(screen)

    pg.display.flip()

