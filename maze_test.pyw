#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import json
import os
from maze import Maze
import time


class MazeGame(object):
    def __init__(self):
        self.screen_size = (800, 600)
        self.screen = None
        self.background = None
        self.surface = None
        self.running = True
        self.game_state = 0
        self.change_state = True
        self.language = None
        self.clock = pygame.time.Clock()
        self.timer = time.time()

        self.btn_list = []

        self.answer_data = {}

        # MAZE INIT
        self.game_size = (540, 360)
        self.game_screen = None
        self.dim = None
        self.path = None
        self.cell_width = None
        self.cell_height = None
        self.red_p = None
        self.green_p = None
        self.blue_p = None
        self.goldy = None
        self.curr_cell = None
        self.last_move = None
        self.maze_obj = None
        self.img_border = pygame.image.load(os.path.join("images", "maze_images", "red_border.png"))
        self.img_border2 = pygame.image.load(os.path.join("images", "maze_images", "redder_border.png"))
        pygame.transform.scale(self.img_border, (self.screen_size[0], self.screen_size[1]))
        self.show_border = False
        self.total_spaces = 0
        self.total_time = None

    def init(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Maze Test")
        self.screen = pygame.display.set_mode(self.screen_size, pygame.HWSURFACE)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface.convert()
        self.background = pygame.image.load(os.path.join("images", "sternberg_images", "bg.jpg"))
        self.screen.blit(self.background, (0, 0))

        self.img_border = pygame.transform.scale(self.img_border, (551, 371))
        self.img_border2 = pygame.transform.scale(self.img_border2, (551, 371))
        self.img_border.convert()
        transColor = self.img_border.get_at((250, 250))
        self.img_border.set_colorkey(transColor)
        self.img_border2.convert()
        self.img_border2.set_colorkey(transColor)
        self.running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            # USER CLICKED X BUTTON
            self.running = False

        elif event.type == pygame.KEYDOWN:
            moved = 0

            if event.key == pygame.K_ESCAPE:
                # USER CLICKED ESC KEY
                self.running = False

            if self.game_state == 2:
                if event.key == pygame.K_SPACE:
                    self.total_spaces += 1

                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.move_player('d')
                    moved = 1

                if event.key in (pygame.K_UP, pygame.K_w):
                    self.move_player('u')
                    moved = 1

                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.move_player('l')
                    moved = 1

                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.move_player('r')
                    moved = 1

                keys = pygame.key.get_pressed()
                if not moved:
                    if keys[pygame.K_DOWN]:
                        self.move_player('d')
                    if keys[pygame.K_UP]:
                        self.move_player('u')
                    if keys[pygame.K_LEFT]:
                        self.move_player('l')
                    if keys[pygame.K_RIGHT]:
                        self.move_player('r')

                self.draw_player()
                pygame.display.update()



        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # LEFT CLICK
                print(event.pos)
                for btn in self.btn_list:
                    if btn.collidepoint(event.pos):
                        return self.on_left_click(btn)

    def on_loop(self):
        if self.game_state == 2:
            self.clock.tick(10)
            if time.time() - self.timer > 1:
                if self.show_border:
                    self.screen.blit(self.img_border, (125, 115))
                else:
                    self.screen.blit(self.img_border2, (125, 115))
                pygame.display.flip()
                self.show_border = not self.show_border
                self.timer = time.time()

    def on_left_click(self, btn):
        if self.game_state == 0:
            if btn.center == (400, 200):
                self.language = "en"
                self.on_change_state()

            elif btn.center == (400, 450):
                self.language = "tr"
                self.on_change_state()

        elif self.game_state == 1:
            if btn.center == (400, 465):
                self.on_change_state()

    def on_render(self):
        if self.change_state:
            self.change_state = False

            if self.game_state == 0:
                # CHOOSE LANGUAGE
                self.load_flags()

            elif self.game_state == 1:
                # INSTRUCTIONS
                self.add_start_btn_and_textarea()

            elif self.game_state == 2:
                # MAZE TIME
                self.maze_init("15x25", 1)
                self.start()

            elif self.game_state == 3:
                # END GAME
                self.screen.blit(self.background, (0, 0))
                self.end_game()
                self.save_data()

    def on_startup(self):
        self.init()

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_render()
            self.on_loop()

        self.on_cleanup()

    def on_cleanup(self):
        pygame.quit()

    def on_change_state(self):
        self.change_state = True
        self.btn_list.clear()
        self.screen.blit(self.background, (0, 0))
        self.game_state += 1

    def load_flags(self):
        self.draw_text("English", 340, 90, 30, (0, 100, 0))
        us = pygame.image.load(os.path.join("images", "sternberg_images", "us_flag.jpg")).convert()
        us_rect = us.get_rect()
        us_rect.center = (self.screen_size[0] // 2, 200)
        self.screen.blit(us, us_rect)
        self.btn_list.append(us_rect)

        self.draw_text("Türkçe", 347, 340, 30, (0, 100, 0))
        tr = pygame.image.load(os.path.join("images", "sternberg_images", "tr_flag.jpg")).convert()
        tr_rect = tr.get_rect()
        tr_rect.center = (self.screen_size[0] // 2, 450)
        self.screen.blit(tr, tr_rect)
        self.btn_list.append(tr_rect)
        pygame.display.flip()

    def add_start_btn_and_textarea(self):
        pygame.draw.rect(self.screen, (50, 50, 50), (45, 20, 710, 310))  # TEXT BORDER
        pygame.draw.rect(self.screen, (0, 0, 0), (50, 25, 700, 300))  # TEXT AREA

        pygame.draw.rect(self.screen, (70, 70, 70), (275, 415, 250, 100))  # BTN BORDER
        start_btn = pygame.draw.rect(self.screen, (100, 100, 100), (280, 420, 240, 90))  # BTN AREA
        self.btn_list.append(start_btn)

        self.draw_instructions()

        if self.language == "tr":
            self.draw_text(self.get_translations("start"), start_btn.x + 10, start_btn.centery - 20, 30,
                           (119, 136, 153))
        else:
            self.draw_text(self.get_translations("start"), start_btn.x + 10, start_btn.centery - 20, 36,
                           (119, 136, 153))

        pygame.display.flip()

    def end_game(self):
        img = pygame.image.load(os.path.join("images", "sternberg_images",
                                             "tick.png")).convert_alpha()
        img_rect = img.get_rect()
        img_rect.center = (self.screen_size[0] // 2, self.screen_size[1] // 2)
        self.screen.blit(img, img_rect)
        pygame.display.flip()

    def get_translations(self, what):
        with open(os.path.join("config", "translations.json"), "r") as f:
            translations = json.load(f)

        texts = []

        if type(translations[self.language][what]) == list:
            texts.append(translations[self.language][what])
        else:
            return translations[self.language][what]

        return texts

    def draw_text(self, line, x, y, size, rgb):
        font = pygame.font.SysFont('mono', size, bold=True)
        r = font.render(str(line), True, rgb)
        self.screen.blit(r, (x, y))

    def draw_instructions(self):
        offset_y = 0
        texts = self.get_translations("maze_intro")
        for i in texts:
            for line in i:
                self.draw_text(line, 60, 75 + offset_y, 24, (0, 100, 0))
                offset_y += 24

        pygame.display.flip()

    def save_data(self):
        total_files = len([name for name in os.listdir(os.path.join("test_results", "maze"))
                           if os.path.isfile(os.path.join("test_results", "maze", name))])

        f = os.path.join("test_results", "maze", "maze_result{0}.json".format(total_files + 1))

        self.answer_data["total spaces"] = self.total_spaces
        self.answer_data["total time"] = time.time() - self.total_time

        with open(f, "w") as f:
            json.dump(self.answer_data, f, indent=4)

    # MAZE FUNCTIONS
    def maze_init(self, dim, path):
        self.game_screen = self.screen.subsurface(130, 120, self.game_size[0], self.game_size[1])
        font = pygame.font.SysFont(pygame.font.get_default_font(), 55)
        text = font.render("Loading...", 1, (255, 255, 255))
        rect = text.get_rect()
        rect.center = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.screen.blit(text, rect)
        pygame.display.update(rect)
        self.dim = map(int, dim.split('x'))
        self.path = path

    def start(self):
        self.maze_obj = Maze(*self.dim)  # pass args to change maze size: Maze(10, 10)
        self.maze_obj.generate()
        self.draw_maze()
        self.reset_player()
        self.total_time = time.time()

    def reset_player(self):
        # Make the sprites for the player.
        w, h = self.cell_width - 3, self.cell_height - 3
        rect = 0, 0, w, h
        base = pygame.Surface((w, h))
        base.fill((255, 255, 255))
        self.red_p = base.copy()
        self.green_p = base.copy()
        self.blue_p = base.copy()
        self.goldy = base.copy()
        if self.path == 1:
            r = (255, 0, 0)
            g = (0, 255, 0)
        else:
            r = g = (255, 255, 255)
        b = (0, 0, 255)
        gold = (0xc5, 0x93, 0x48)
        pygame.draw.ellipse(self.red_p, r, rect)
        pygame.draw.ellipse(self.green_p, g, rect)
        pygame.draw.ellipse(self.blue_p, b, rect)
        pygame.draw.ellipse(self.goldy, gold, rect)

        # Make a same-size matrix for the player.
        self.player_maze = {}
        for y in range(self.maze_obj.rows):
            for x in range(self.maze_obj.cols):
                cell = {'visited': 0}  # if 1, draws green. if >= 2, draws red.
                self.player_maze[(x, y)] = cell
                self.game_screen.blit(base, (x * self.cell_width + 2, y * self.cell_height + 2))

        self.game_screen.blit(self.goldy, (x * self.cell_width + 2, y * self.cell_height + 2))
        self.cx = self.cy = 0
        self.curr_cell = self.player_maze[(self.cx, self.cy)]  # starts at origin

        self.last_move = None  # For last move fun

    def draw_maze(self):
        self.game_screen.fill((255, 255, 255))
        self.cell_width = self.game_size[0] / self.maze_obj.cols
        self.cell_height = self.game_size[1] / self.maze_obj.rows

        for y in range(self.maze_obj.rows):
            for x in range(self.maze_obj.cols):
                if self.maze_obj.maze[(x, y)]['south']:  # draw south wall
                    pygame.draw.line(self.game_screen, (0, 0, 0),
                                     (x * self.cell_width, y * self.cell_height + self.cell_height),
                                     (x * self.cell_width + self.cell_width,
                                      y * self.cell_height + self.cell_height))
                if self.maze_obj.maze[(x, y)]['east']:  # draw east wall
                    pygame.draw.line(self.game_screen, (0, 0, 0),
                                     (x * self.cell_width + self.cell_width, y * self.cell_height),
                                     (x * self.cell_width + self.cell_width, y * self.cell_height +
                                      self.cell_height))
        # Screen border
        pygame.draw.rect(self.game_screen, (0, 0, 0), (0, 0, self.game_size[0], self.game_size[1]), 1)
        pygame.display.update()

    def move_player(self, direction):
        no_move = 0
        try:
            if direction == 'u':
                if not self.maze_obj.maze[(self.cx, self.cy - 1)]['south']:
                    self.cy -= 1
                    self.curr_cell['visited'] += 1
                else:
                    no_move = 1
            elif direction == 'd':
                if not self.maze_obj.maze[(self.cx, self.cy)]['south']:
                    self.cy += 1
                    self.curr_cell['visited'] += 1
                else:
                    no_move = 1
            elif direction == 'l':
                if not self.maze_obj.maze[(self.cx - 1, self.cy)]['east']:
                    self.cx -= 1
                    self.curr_cell['visited'] += 1
                else:
                    no_move = 1
            elif direction == 'r':
                if not self.maze_obj.maze[(self.cx, self.cy)]['east']:
                    self.cx += 1
                    self.curr_cell['visited'] += 1
                else:
                    no_move = 1
            else:
                no_move = 1
        except KeyError:  # Tried to move outside screen
            no_move = 1

        # Handle last move...
        if ((direction == 'u' and self.last_move == 'd') or
                (direction == 'd' and self.last_move == 'u') or
                (direction == 'l' and self.last_move == 'r') or
                (direction == 'r' and self.last_move == 'l')) and not no_move:
            self.curr_cell['visited'] += 1

        if not no_move:
            self.last_move = direction
            self.curr_cell = self.player_maze[(self.cx, self.cy)]

        # Check for victory.
        if self.cx + 1 == self.maze_obj.cols and self.cy + 1 == self.maze_obj.rows:
            self.on_change_state()

    def draw_player(self):
        for y in range(self.maze_obj.rows):
            for x in range(self.maze_obj.cols):
                if self.player_maze[(x, y)]['visited'] > 0:
                    if self.player_maze[(x, y)]['visited'] == 1:
                        circ = self.green_p
                    else:
                        circ = self.red_p
                    # draw green circles
                    self.game_screen.blit(circ, (x * self.cell_width + 2, y * self.cell_height + 2))
        self.game_screen.blit(self.blue_p, (self.cx * self.cell_width + 2, self.cy * self.cell_height + 2))


MazeGame().on_startup()
