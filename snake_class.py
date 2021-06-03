import os
import pickle
import random
from math import atan2, degrees

import numpy as np
import pygame
from pygame.locals import *


class Snake():

    def __init__(self, name):
        # self.model = tf.tf.keras.models.load_model('model/')
        pygame.init()
        self.name = name
        self.clock = pygame.time.Clock()
        self.height_width = 500
        self.screen = pygame.display.set_mode((self.height_width, self.height_width))
        #pygame.display.set_caption(name)
        self.snake = [[300, 360], (320, 360), (340, 360)]
        self.block = 20
        self.tam = [self.block, self.block]
        self.padding = 40
        self.UP = 0
        self.DOWN = 1
        self.RIGHT = 2
        self.LEFT = 3
        # pygame.mixer.music.load("resources/back_groud.mp3")
        # pygame.mixer.music.play(-1)
        # self.my_direction = random.randrange(0,4)
        self.num_clock = 10

        self.distance_wall_left = 0
        self.distance_wall_right = 0
        self.distance_wall_up = 0
        self.distance_wall_down = 0
        self.distance_diag_wall_right_down = 0
        self.distance_diag_wall_right_up = 0
        self.distance_diag_wall_left_down = 0
        self.distance_diag_wall_left_up = 0

        self.distance_rond_left = 0
        self.distance_rond_down = 0
        self.distance_rond_right = 0
        self.distance_rond_up = 0
        self.distance_diag_right_down = 0
        self.distance_diag_right_up = 0
        self.distance_diag_left_down = 0
        self.distance_diag_left_up = 0

        self.score = 0
        self.best_score = 0
        self.help = False
        self.len_sensors = 500

        self.myfont = pygame.font.SysFont("monospace", 20)

        self.rond = [220, 200]
        self.snake_skin = pygame.Surface(self.tam)
        self.snake_skin.fill((255, 255, 255))
        self.apple_skin = pygame.Surface((self.block, self.block))
        self.apple_skin.fill((255, 0, 0))
        self.left = (0, 255, 0)
        self.right = (0, 255, 0)
        self.up = (0, 255, 0)
        self.down = (0, 255, 0)
        self.diag_left_up = (0, 255, 0)
        self.diag_left_down = (0, 255, 0)
        self.diag_right_up = (0, 255, 0)
        self.diag_right_down = (0, 255, 0)
        self.death = False

    def verficia(self, c1):
        return c1[0] == self.block or c1[0] == self.height_width - self.padding or c1[1] == self.block or c1[1] == self.height_width - self.padding

    def sada(self):
        # effect = pygame.mixer.Sound('resources/acerto.wav')
        # effect.play()
        # for j in range(3000000):
        #     a = j
        self.snake.append((0, 0))
        self.rond = [random.randrange(self.padding * 2, self.height_width - self.padding * 2, self.padding),
                     random.randrange(self.padding * 2, self.height_width - self.padding * 2, self.padding)]

    def rabo(self):

        for i in range(1, len(self.snake)):
            if self.snake[0][0] == self.snake[i][0] and self.snake[0][1] == self.snake[i][1]:
                return True

    def reset(self):

        self.distance_wall_left = 0
        self.distance_wall_right = 0
        self.distance_wall_up = 0
        self.distance_wall_down = 0
        self.distance_diag_wall_right_down = 0
        self.distance_diag_wall_right_up = 0
        self.distance_diag_wall_left_down = 0
        self.distance_diag_wall_left_up = 0
        self.my_direction = 4
        self.distance_rond_left = 0
        self.distance_rond_down = 0
        self.distance_rond_right = 0
        self.distance_rond_up = 0
        self.distance_diag_right_down = 0
        self.distance_diag_right_up = 0
        self.distance_diag_left_down = 0
        self.distance_diag_left_up = 0

        self.score = 0

    def analyzer_position(self, snake):

        analyzer_left = snake[0] - self.rond[0]
        analyzer_right = self.rond[0] - snake[0]
        analyzer_up = snake[1] - self.rond[1]
        analyzer_down = self.rond[1] - snake[1]
        # print(analyzer_up)

        if analyzer_left >= 0 and analyzer_left <= self.len_sensors and snake[1] == self.rond[1]:

            if self.my_direction != 3 and self.my_direction != 2 and self.help:
                self.my_direction = 3

            self.left = (255, 0, 0)
            self.distance_rond_left = analyzer_left


        elif analyzer_right >= 0 and analyzer_right <= self.len_sensors and snake[1] == self.rond[1]:
            self.right = (255, 0, 0)
            self.distance_rond_right = analyzer_right

            if self.my_direction != 3 and self.my_direction != 2 and self.help:
                self.my_direction = 2


        elif analyzer_up >= 0 and analyzer_up <= self.len_sensors and snake[0] == self.rond[0]:
            self.up = (255, 0, 0)
            self.distance_rond_up = analyzer_up

            if self.my_direction != 0 and self.my_direction != 1 and self.help:
                self.my_direction = 0

        elif analyzer_down >= 0 and analyzer_down <= self.len_sensors and snake[0] == self.rond[0]:
            self.down = (255, 0, 0)
            self.distance_rond_down = analyzer_down

            if self.my_direction != 0 and self.my_direction != 1 and self.help:
                self.my_direction = 1


        elif analyzer_left == analyzer_up and analyzer_left >= 20 and analyzer_left <= self.len_sensors:

            self.distance_diag_left_up = analyzer_left
            self.diag_left_up = (255, 0, 0)
            self.score += 40

        elif analyzer_left == analyzer_down and analyzer_left >= 20 and analyzer_left <= self.len_sensors:

            self.distance_diag_left_down = analyzer_left
            self.diag_left_down = (255, 0, 0)
            self.score += 40

        elif analyzer_right == analyzer_up and analyzer_right >= 20 and analyzer_right <= self.len_sensors:

            self.distance_diag_right_up = analyzer_right
            self.diag_right_up = (255, 0, 0)
            self.score += 40

        elif analyzer_right == analyzer_down and analyzer_right >= 20 and analyzer_right <= self.len_sensors:

            self.distance_diag_right_down = analyzer_right
            self.diag_right_down = (255, 0, 0)
            self.score += 40

        else:

            self.left = (0, 255, 0)
            self.right = (0, 255, 0)
            self.up = (0, 255, 0)
            self.down = (0, 255, 0)
            self.diag_left_up = (0, 255, 0)
            self.diag_left_down = (0, 255, 0)
            self.diag_right_up = (0, 255, 0)
            self.diag_right_down = (0, 255, 0)
            self.distance_rond_up = 0
            self.distance_rond_down = 0
            self.distance_rond_left = 0
            self.distance_rond_right = 0
            self.distance_diag_right_up = 0
            self.distance_diag_left_up = 0
            self.distance_diag_left_down = 0
            self.distance_diag_right_down = 0

    def analyzer_position_wall(self, snake):

        #           EIXO X PARA DIREITA  + PARA ESQUERDA -
        #           EIXO Y PARA BAIXO + PARA CIMA -

        analyzer_left = snake[0] - self.padding
        analyzer_right = (self.height_width -(self.padding+20)) - snake[0]
        analyzer_up = snake[1] - self.padding
        analyzer_down = (self.height_width -(self.padding+20)) - snake[1]

        self.distance_wall_up = 0
        self.distance_wall_down = 0
        self.distance_wall_left = 0
        self.distance_wall_right = 0
        self.distance_diag_wall_right_down = 0
        self.distance_diag_wall_right_up = 0
        self.distance_diag_wall_left_down = 0
        self.distance_diag_wall_left_up = 0
        if analyzer_left >= 0 and analyzer_left <= self.len_sensors:
            # self.left = (255, 0, 0)

            self.distance_wall_left = analyzer_left
            # print(analyzer_left, analyzer_up)
            if self.help:
                if analyzer_left == 20 and analyzer_down > 20 and self.my_direction != 0:
                    self.my_direction = 1
                elif analyzer_left == 20 and analyzer_up > 20 and self.my_direction != 1:
                    self.my_direction = 0
                elif analyzer_left == 20:
                    self.my_direction = 2

        if analyzer_right >= 0 and analyzer_right <= self.len_sensors:
            # self.right = (255, 0, 0)
            self.distance_wall_right = analyzer_right

            if self.help:
                if analyzer_right == 20 and analyzer_down > 20 and self.my_direction != 0:
                    self.my_direction = 1
                elif analyzer_right == 20 and analyzer_up > 20 and self.my_direction != 1:
                    self.my_direction = 0
                elif analyzer_right == 20:
                    self.my_direction = 3

        if analyzer_up >= 0 and analyzer_up <= self.len_sensors:
            self.distance_wall_up = analyzer_up
            if self.help:
                if analyzer_up == 20 and analyzer_right > 20 and self.my_direction != 3:
                    self.my_direction = 2
                elif analyzer_up == 20 and analyzer_left > 20 and self.my_direction != 2:
                    self.my_direction = 3
                elif analyzer_up == 20:
                    self.my_direction = 1

        if analyzer_down >= 0 and analyzer_down <= self.len_sensors:
            self.distance_wall_down = analyzer_down
            if self.help:
                if analyzer_down == 20 and analyzer_right == 20 and self.my_direction != 3:
                    self.my_direction = 2
                elif analyzer_down == 20 and analyzer_left == 20 and self.my_direction != 2:
                    self.my_direction = 3
                elif analyzer_down == 20:
                    self.my_direction = 0

        if analyzer_left == analyzer_up and analyzer_left >= 20 and analyzer_left <= self.len_sensors:
            self.distance_diag_wall_left_up = analyzer_left

        if analyzer_left == analyzer_down and analyzer_left >= 20 and analyzer_left <= self.len_sensors:
            self.distance_diag_wall_left_down = analyzer_left

        if analyzer_right == analyzer_up and analyzer_right >= 20 and analyzer_right <= self.len_sensors:
            self.distance_diag_wall_right_up = analyzer_right

        if analyzer_right == analyzer_down and analyzer_right >= 20 and analyzer_right <= self.len_sensors:
            self.distance_diag_wall_right_down = analyzer_right

    def degree(self):

        for j in range(self.block, self.height_width, self.block):
            pygame.draw.line(self.screen, (100, 100, 100), (self.padding, j), (self.height_width - 40, j))
            pygame.draw.line(self.screen, (100, 100, 100), (j, self.padding), (j, self.height_width - 40))

    def pause(self):

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        return False

    def get_actions(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.death = True
                elif event.key == K_1:
                    self.num_clock = 10
                elif event.key == K_2:
                    self.num_clock = 30
                elif event.key == K_3:
                    self.num_clock = 50
                elif event.key == K_4:
                    self.num_clock = 80
                elif event.key == K_5:
                    self.num_clock = 100
                elif event.key == K_6:
                    self.num_clock = 500
                elif event.key == K_7:
                    self.num_clock = 1000
                elif event.key == K_8:
                    self.num_clock = 2000
                elif event.key == K_9:
                    self.num_clock = 3000

                elif event.key == K_UP and self.my_direction != self.DOWN:
                    self.my_direction = self.UP
                elif event.key == K_DOWN and self.my_direction != self.UP:
                    self.my_direction = self.DOWN
                elif event.key == K_RIGHT and self.my_direction != self.LEFT:
                    self.my_direction = self.RIGHT
                elif event.key == K_LEFT and self.my_direction != self.RIGHT:
                    self.my_direction = self.LEFT
                elif event.key == K_SPACE:
                    self.pause()
                elif event.key == K_RETURN:
                    if not self.help:
                        self.help = True
                    else:
                        self.help = False

        if self.my_direction == self.UP:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] - self.block)
        elif self.my_direction == self.DOWN:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] + self.block)
        elif self.my_direction == self.RIGHT:
            self.snake[0] = (self.snake[0][0] + self.block, self.snake[0][1])
        elif self.my_direction == self.LEFT:
            self.snake[0] = (self.snake[0][0] - self.block, self.snake[0][1])

    def sensors(self):

        # CIMA EM BAIXO

        pygame.draw.line(self.screen, self.up,
                         (self.snake[0][0] + (self.block / 2), self.snake[0][1] + (self.block / 2)),
                         (self.snake[0][0] + (self.block / 2), self.snake[0][1] - self.height_width - 20))

        pygame.draw.line(self.screen, self.down,
                         (self.snake[0][0] + (self.block / 2), self.snake[0][1] + (self.block / 2)),
                         (self.snake[0][0] + (self.block / 2), self.snake[0][1] + self.height_width + 20))

        #  LEFT
        pygame.draw.line(self.screen, self.left,
                         (self.snake[0][0] + (self.block / 2), self.snake[0][1] + (self.block / 2)),
                         (self.snake[0][0] - self.height_width, self.snake[0][1] + (self.block / 2)))

        # RIGHT
        pygame.draw.line(self.screen, self.right,
                         (self.snake[0][0] + (self.block / 2), self.snake[0][1] + (self.block / 2)),
                         (self.snake[0][0] + self.height_width, self.snake[0][1] + (self.block / 2)))

        # diagonal left
        pygame.draw.line(self.screen, self.diag_left_up,
                         (self.snake[0][0] + (self.block / 2), self.snake[0][1] + (self.block / 2)),
                         (self.snake[0][0] - self.height_width,
                          self.snake[0][1] + (self.block / 2) - (self.height_width)))

        pygame.draw.line(self.screen, self.diag_left_down,
                         (self.snake[0][0] + (self.block / 2), self.snake[0][1] + (self.block / 2)),
                         (self.snake[0][0] - self.height_width,
                          self.snake[0][1] + (self.block / 2) + (self.height_width)))

        # diagonal right

        pygame.draw.line(self.screen, self.diag_right_up,
                         (self.snake[0][0] + (self.block / 2), self.snake[0][1] + (self.block / 2)),
                         (self.snake[0][0] + self.height_width + 20,
                          self.snake[0][1] + (self.block / 2) - (self.height_width)))

        pygame.draw.line(self.screen, self.diag_right_down,
                         (self.snake[0][0] + (self.block / 2), self.snake[0][1] + (self.block / 2)),
                         (self.snake[0][0] + self.height_width + 20,
                          self.snake[0][1] + (self.block / 2) + (self.height_width)))

    def run(self, obj, epoch):

        self.reset()
        contador = 0

        file = 'resources/back_groud.mp3'
        #pygame.init()

        while True:
            self.aux = self.snake[0]
            self.get_actions()
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.apple_skin, self.rond)


            if self.verficia(self.snake[0]) or self.death:
                self.snake = [(200, 200), (210, 200), (220, 200)]
                self.death = False
                if self.score > self.best_score:
                    path = f'bests/{self.name}/{epoch}/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    self.best_score = self.score
                    pickle.dump(obj.get_weights(), open(f'bests/{self.name}/{epoch}/{self.best_score}.pkl', 'wb'))

                return self.score

            self.degree()
            for i in range(len(self.snake) - 1, 0, -1):
                self.snake[i] = (self.snake[i - 1][0], self.snake[i - 1][1])

            for pos in self.snake:
                self.screen.blit(self.snake_skin, pos)

            if self.snake[0][0] == self.rond[0] and self.snake[0][1] == self.rond[1]:
                self.score += 1000
                self.sada()
                contador = 0

            if contador == 90:
                self.death = True

            # // UNITEIS
            # self.analyzer_position_wall(self.snake[0])
            # self.sensors()
            # score_text = self.myfont.render(f"Score = {self.score}", 1, (255, 255, 255))
            # self.screen.blit(score_text, (40, 0))
            # epoch_text = self.myfont.render(f"Epoch = {epoch}", 1, (255, 255, 255))
            # self.screen.blit(epoch_text, (350, 0))
            # helper_text = self.myfont.render(f"Helper control Press Enter = {self.help}", 1, (255, 255, 255))
            # self.screen.blit(helper_text, (self.height_width / 2 - 220, self.height_width - 20))
            # best_score_text = self.myfont.render(f"Best Score = {self.best_score}", 1, (255, 255, 255))
            # self.screen.blit(best_score_text, (self.height_width - 350, 20))

            analyzer_x = self.rond[0] - self.snake[0][0]
            analyzer_y = self.snake[0][1] - self.rond[1]

            angle = degrees(atan2(analyzer_y, analyzer_x))
            analyzer_aux_x = self.rond[0] - self.aux[0]

            analyzer_aux_y = self.aux[1] - self.rond[1]

            analyzer_t_x = analyzer_x * -1 if analyzer_x < 0 else analyzer_x
            analyzer_t_y = analyzer_y * -1 if analyzer_y < 0 else analyzer_y

            analyzer_aux_x = analyzer_aux_x * -1 if analyzer_aux_x < 0 else analyzer_aux_x
            analyzer_aux_y = analyzer_aux_y * -1 if analyzer_aux_y < 0 else analyzer_aux_y

            if analyzer_t_x > analyzer_aux_x:
                self.score -= 40
            if analyzer_aux_x > analyzer_t_x:
                self.score += 30
            if 0 == analyzer_t_x:
                self.score += 30
            if analyzer_t_y > analyzer_aux_y:
                self.score -= 40
            if analyzer_aux_y > analyzer_t_y:
                self.score += 30
            if 0 == analyzer_t_y:
                self.score += 30

            #treinamento old
            # data = [analyzer_x, analyzer_y, angle, self.distance_rond_left, self.distance_rond_right,
            #         self.distance_rond_up, self.distance_rond_down,
            #         self.distance_diag_right_down, self.distance_diag_right_up, self.distance_diag_left_down,
            #         self.distance_diag_left_up,
            #         # self.distance_wall_left,
            #         # self.distance_wall_right,
            #         # self.distance_wall_up,
            #         # self.distance_wall_down
            #         ]
            # print(len(data))

            data = [angle]

            if obj is not None:
                predict = np.argmax(obj.predict(np.array([data])))
                if self.my_direction == 3 and predict == 2 or self.my_direction == 2 and predict == 3 or self.my_direction == 1 and predict == 0 or self.my_direction == 0 and predict == 1:
                    self.score -= 300
                else:
                    self.my_direction = predict
            contador += 1
            pygame.display.update()