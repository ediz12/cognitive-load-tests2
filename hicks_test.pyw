#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PATTERN CREDITS: http://thepatternlibrary.com/

import operator
import pygame
import json
import os
import random



class SternBergGame(object):
    def __init__(self):
        self.screen_size = (800, 600)
        self.screen = None
        self.background = None
        self.white_noise = None
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
        self.answer = 0
        self.question = ""

        self.correct_btn_id = 0
        self.is_correct = 0
        self.answer_time = 0

        self.answer_data = {}

        f = os.path.join("images", "hicks_images", "patterns")
        self.total_images = len([name for name in os.listdir(f) if os.path.isfile(os.path.join(f, name))])

    def init(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.display.set_caption("Hick's Law Test")
        self.screen = pygame.display.set_mode(self.screen_size, pygame.HWSURFACE)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.convert()
        self.background = pygame.image.load(os.path.join("images", "sternberg_images", "bg.jpg"))
        self.screen.blit(self.background, (0, 0))
        self.white_noise = pygame.mixer.Sound(os.path.join("images", "hicks_images", "whitenoise.ogg"))
        self.white_noise.play(loops=-1)
        self.white_noise.set_volume(0)
        self.running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            # USER CLICKED X BUTTON
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # USER CLICKED ESC KEY
                self.running = False

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
                if self.loop_count < self.loop_max:
                    self.change_state = True
                    self.on_change_state()
                    self.game_state = 2

                    self.add_results()
                    self.is_correct = 0
                    self.answer_time = 0
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

        elif self.game_state == 3:
            if self.btn_list[self.correct_btn_id].center == btn.center:
                self.is_correct = 1

            self.answer_time = 50 - self.timer

            if self.loop_count < self.loop_max:
                self.change_state = True
                self.on_change_state()
                self.game_state = 2

                self.add_results()
                self.is_correct = 0
                self.answer_time = 0
                self.loop_count += 1
            else:
                self.add_results()
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
                # NUMBER SHOW
                self.white_noise.set_volume(0.5)
                self.timer = 10.0
                self.clock = pygame.time.Clock()
                self.create_equation(True)
                self.draw_digits()

            elif self.game_state == 3:
                # QUESTION FINDER
                self.timer = 50.0
                self.clock = pygame.time.Clock()
                self.draw_questions()

            elif self.game_state == 4:
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

    def add_results(self):
        res = {
            "corrent answer": self.is_correct,
            "answer time": self.answer_time
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
        texts = self.get_translations("hicks_intro")
        for i in texts:
            for line in i:
                self.draw_text(line, 90, 110 + offset_y, 32, (0, 100, 0))
                offset_y += 32

        pygame.display.flip()

    def draw_digits(self):
        offset_x = 0

        for digit in str(self.answer):
            r = random.randint
            rgb = (r(0, 255), r(0, 255), r(0, 255))
            self.draw_text(digit, 186 + offset_x, (self.screen_size[1] // 2) - 128, 256, rgb)
            offset_x += 256

    def create_equation(self, get_correct_answer=False):
        ops = {'+': operator.add,
               '-': operator.sub}

        while True:

            op = random.choice(list(ops.keys()))
            num1 = random.randint(10, 49)
            num2 = random.randint(1, 50)

            ans = ops.get(op)(num1, num2)

            if get_correct_answer:
                if 10 <= ans < 100:
                    self.answer = ans
                    self.question = "{} {} {}".format(num1, op, num2)
                    return
            else:
                if self.answer - 30 <= ans < self.answer + 30:
                    s = "{} {} {}".format(num1, op, num2)
                    print(s, " = ", ans)
                    return s

    def draw_questions(self):
        # bg = pygame.image.load(os.path.join("images", "sternberg_images", "rainbow_bg.jpg"))
        # self.screen.blit(bg, (0, 0))

        lsnumbers = list(range(1, self.total_images + 1))

        self.correct_btn_id = random.randint(0, 8)

        for i in range(0, 3):
            for j in range(0, 3):

                if (3 * i + j) == self.correct_btn_id:
                    q = self.question
                else:
                    q = self.create_equation()

                k = lsnumbers.pop(random.randint(0, len(lsnumbers) - 1))
                img = pygame.image.load(os.path.join("images", "hicks_images",
                                                     "patterns", "pattern{0}.jpg".format(k))).convert()
                img_rect = img.get_rect()

                img_rect.topleft = (150 + (180 * (i % 3)), 60 + (180 * (j % 3)))

                self.btn_list.append(img_rect)
                self.screen.blit(img, img_rect)

                self.draw_text(q, 163 + (180 * (i % 3)), 123 + (180 * (j % 3)), 26, (255, 255, 255))
                self.draw_text(q, 165 + (180 * (i % 3)), 125 + (180 * (j % 3)), 26, (100, 100, 100))

        pygame.display.flip()

    def save_data(self):
        total_files = len([name for name in os.listdir(os.path.join("test_results", "hicks"))
                           if os.path.isfile(os.path.join("test_results", "hicks", name))])

        print(self.answer_data)
        f = os.path.join("test_results", "hicks", "hicks_result{0}.json".format(total_files + 1))
        with open(f, "w") as f:
            json.dump(self.answer_data, f, indent=4)


SternBergGame().on_startup()
