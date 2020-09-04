#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import json
import os
import random


class SternBergGame(object):
    def __init__(self):
        self.screen_size = (800, 600)
        self.screen = None
        self.background = None
        self.running = True
        self.game_state = 0
        self.change_state = True
        self.language = None
        self.clock = pygame.time.Clock()
        self.timer = 0.0
        self.fps = 30
        self.loop_count = 1
        self.loop_max = 7

        self.btn_list = []
        self.chosen_images = []
        self.chosen_numbers = []
        self.correct_btn_id = 0
        self.memory_answer = True

        self.correct_math = 0
        self.correct_memory = 0
        self.math_answer_time = 0
        self.memory_answer_time = 0

        self.answer_data = {}

        f = os.path.join("images", "sternberg_images", "picture_test")
        self.total_images = len([name for name in os.listdir(f) if os.path.isfile(os.path.join(f, name))])

    def init(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Sternberg Memory Test")
        self.screen = pygame.display.set_mode(self.screen_size, pygame.HWSURFACE)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.convert()
        self.background = pygame.image.load(os.path.join("images", "sternberg_images", "bg.jpg"))
        self.screen.blit(self.background, (0, 0))
        self.running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            # USER CLICKED X BUTTON
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # USER CLICKED ESC KEY
                self.running = False

            if self.game_state == 6:
                if (event.key == pygame.K_f and self.memory_answer) or (
                        event.key == pygame.K_j and not self.memory_answer):
                    self.correct_memory += 1

                if event.key in (pygame.K_f, pygame.K_j):
                    self.memory_answer_time = 10 - self.timer
                    self.add_results()
                    if self.loop_count < self.loop_max:
                        self.change_state = True
                        self.on_change_state()
                        self.game_state = 2

                        self.correct_math = 0
                        self.correct_memory = 0
                        self.math_answer_time = 0
                        self.memory_answer_time = 0
                        self.loop_count += 1
                    else:
                        self.add_results()
                        self.on_change_state()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # LEFT CLICK
                print(event.pos)
                for btn in self.btn_list:
                    if btn.collidepoint(event.pos):
                        return self.on_left_click(btn)

    def on_loop(self):
        ms = self.clock.tick(self.fps)
        self.timer -= ms / 1000.0

        if self.game_state == 2:
            self.screen.fill(pygame.Color("black"), (620, 20, 165, 20))
            self.draw_text(self.get_translations("timeleft").format(self.timer), 620, 20, 15, (0, 100, 0))
            pygame.display.flip()

            if self.timer < 0.1:
                self.change_state = True
                self.on_change_state()

        elif self.game_state == 3:
            self.screen.fill(pygame.Color("black"), (620, 20, 165, 20))
            self.draw_text(self.get_translations("timeleft").format(self.timer), 620, 20, 15, (0, 100, 0))
            pygame.display.flip()

            if self.timer < 0.1:
                self.change_state = True
                self.on_change_state()

        elif self.game_state == 4:
            self.screen.fill(pygame.Color("black"), (620, 20, 165, 20))
            self.draw_text(self.get_translations("timeleft").format(self.timer), 620, 20, 15, (0, 100, 0))
            pygame.display.flip()

            if self.timer < 0.1:
                self.change_state = True
                self.on_change_state()

        elif self.game_state == 5:
            self.screen.fill(pygame.Color("black"), (620, 20, 165, 20))
            self.draw_text(self.get_translations("timeleft").format(self.timer), 620, 20, 15, (0, 100, 0))
            pygame.display.flip()

            if self.timer < 0.1:
                self.change_state = True
                self.on_change_state()

        elif self.game_state == 6:
            self.screen.fill(pygame.Color("black"), (620, 20, 165, 20))
            self.draw_text(self.get_translations("timeleft").format(self.timer), 620, 20, 15, (0, 100, 0))
            pygame.display.flip()

            if self.timer < 0.1:
                if self.loop_count < self.loop_max:
                    self.change_state = True
                    self.on_change_state()
                    self.game_state = 2

                    self.add_results()
                    self.correct_math = 0
                    self.correct_memory = 0
                    self.math_answer_time = 0
                    self.memory_answer_time = 0
                    self.loop_count += 1
                else:
                    self.add_results()
                    self.on_change_state()

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

        elif self.game_state == 5:
            if self.btn_list[self.correct_btn_id].center == btn.center:
                self.correct_math += 1
            self.math_answer_time = 5 - self.timer
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
                # PICTURES TEST
                self.timer = 10.0
                self.clock = pygame.time.Clock()
                lsnumbers = list(range(1, self.total_images + 1))

                for t in range(0, 6):
                    i = lsnumbers.pop(random.randint(0, len(lsnumbers) - 1))
                    img = pygame.image.load(os.path.join("images", "sternberg_images",
                                                         "picture_test", "image{0}.jpg".format(i))).convert()
                    pygame.transform.scale(img, (150, 150))
                    img_rect = img.get_rect()
                    img_rect.topleft = (40 + (250 * (t % 3)), 75 + (250 * (t % 2)))
                    self.screen.blit(img, img_rect)
                    self.chosen_images.append(i)

                pygame.display.flip()

            elif self.game_state == 3:
                # 2 SECOND BREAK
                self.timer = 2.0
                self.clock = pygame.time.Clock()

            elif self.game_state == 4:
                # ADDITION TEST
                self.timer = 15.0
                self.clock = pygame.time.Clock()
                self.add_addition()

            elif self.game_state == 5:
                # ADDITION ANSWER
                self.timer = 5.0
                self.clock = pygame.time.Clock()
                self.add_answers()

            elif self.game_state == 6:
                # MEMORY ANSWER
                self.timer = 10.0
                self.clock = pygame.time.Clock()
                self.add_memory_answer()
                pygame.display.flip()

            elif self.game_state == 7:
                # END GAME
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

    def add_addition(self):
        pygame.draw.rect(self.screen, (50, 50, 50), (45, 60, 710, 310))  # TEXT BORDER
        pygame.draw.rect(self.screen, (0, 0, 0), (50, 65, 700, 300))  # TEXT AREA

        number_one = random.randint(0, 50)
        number_two = random.randint(0, 51)
        self.chosen_numbers.extend([number_one, number_two])

        self.draw_text("{0} + {1} = ?".format(number_one, number_two), 100, 150, 92, (0, 100, 0))
        pygame.display.flip()

    def add_answers(self):

        pygame.draw.rect(self.screen, (50, 50, 50), (45, 60, 710, 310))  # TEXT BORDER
        pygame.draw.rect(self.screen, (0, 0, 0), (50, 65, 700, 300))  # TEXT AREA

        pygame.draw.rect(self.screen, (50, 50, 50), (155, 430, 110, 60))  # BTN 1 BORDER
        btn1 = pygame.draw.rect(self.screen, (0, 0, 0), (160, 435, 100, 50))  # BTN 1 AREA

        pygame.draw.rect(self.screen, (50, 50, 50), (500, 430, 110, 60))  # BTN 2 BORDER
        btn2 = pygame.draw.rect(self.screen, (0, 0, 0), (505, 435, 100, 50))  # BTN 2 AREA

        self.btn_list.extend([btn1, btn2])

        ans = sum(self.chosen_numbers)
        fake_ans = sum(self.chosen_numbers) + int(random.choice([-1, -2, 1, 2]))

        self.correct_btn_id = 0

        if random.randint(0, 1):
            ans, fake_ans = fake_ans, ans
            self.correct_btn_id = 1

        self.draw_text(ans, 185, 443, 36, (0, 100, 0))
        self.draw_text(fake_ans, 535, 443, 36, (0, 100, 0))

        self.chosen_numbers.clear()

    def add_memory_answer(self):
        i = random.randint(1, 7)
        img = pygame.image.load(os.path.join("images", "sternberg_images",
                                             "picture_test", "image{0}.jpg".format(i))).convert()

        pygame.transform.scale(img, (300, 300))
        img_rect = img.get_rect()
        img_rect.center = (self.screen_size[0] // 2, self.screen_size[1] // 2)
        self.screen.blit(img, img_rect)

        if i in self.chosen_images:
            self.memory_answer = True
        else:
            self.memory_answer = False

        self.chosen_images.clear()

    def add_results(self):
        res = {
            "img correct": self.correct_memory,
            "math correct": self.correct_math,
            "img answer time": self.memory_answer_time,
            "math answer time": self.math_answer_time
        }

        print(res)
        self.answer_data[self.loop_count] = res

    def end_game(self):
        img = pygame.image.load(os.path.join("images", "sternberg_images",
                                             "tick.png")).convert_alpha()
        img_rect = img.get_rect()
        img_rect.center = (self.screen_size[0] // 2, self.screen_size[1] // 2)
        self.screen.blit(img, img_rect)
        pygame.display.flip()

        print(self.correct_memory, self.correct_math)

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
        texts = self.get_translations("sternberg_intro")
        for i in texts:
            for line in i:
                self.draw_text(line, 60, 75 + offset_y, 16, (0, 100, 0))
                offset_y += 20

        pygame.display.flip()

    def save_data(self):
        total_files = len([name for name in os.listdir(os.path.join("test_results", "sternberg"))
                           if os.path.isfile(os.path.join("test_results", "sternberg", name))])

        print(self.answer_data)
        f = os.path.join("test_results", "sternberg", "sternberg_result{0}.json".format(total_files + 1))
        with open(f, "w") as f:
            json.dump(self.answer_data, f, indent=4)


SternBergGame().on_startup()
