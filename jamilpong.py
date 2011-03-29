import pygame
from pygame.locals import *
pygame.init()

WIDTH = 640
HEIGHT = 480
BALL_W = 16
BALL_H = 16
BALL_CLR = (255, 255, 255)
PADDLE_W = 16
PADDLE_H = 96
PADDLE_CLR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Label(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, text=""):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 30)
        self.text = text
        self.center = (x_pos, y_pos)

    def update(self):
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.center

class Ball(pygame.sprite.Sprite):
    def __init__(self, x_pos=320, y_pos=240):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BALL_W, BALL_H))
        self.image = self.image.convert()
        self.image.fill(BALL_CLR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
        self.speed = 8
        self.dx = -self.speed
        self.dy = 0

    def reset(self):
        self.rect.centerx = 320
        self.rect.centery = 240
        self.speed = 8
        self.dx = -self.speed
        self.dy = 0

    def update(self, other_sprites):
        # update the ball's speed, in the appropriate direction
        if self.dx < 0:
            self.dx = -self.speed
        else:
            self.dx = self.speed

        # update the ball's position
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        
        # if the ball hits the top of the screen, bounce it
        if self.rect.top < 0:
            self.rect.top = 0
            self.dy = self.dy * -1
        # if the ball hits the bottom of the screen, bounce it
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
            self.dy = self.dy * -1
        
        # if the ball collides with a paddle, bounce it back
        collide_li = pygame.sprite.spritecollide(self, other_sprites, False)
        if collide_li:
            self.dx = self.dx * -1
            if collide_li[0].dir == "up":
                self.dy = -self.speed
            elif collide_li[0].dir == "down":
                self.dy = self.speed
            if self.speed < 24:
                self.speed += 1

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x_pos=64, y_pos=280):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PADDLE_W, PADDLE_H))
        self.image = self.image.convert()
        self.image.fill(PADDLE_CLR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
        self.dy = 0
        self.dir = "none"
        self.score = 0

    def reset(self):
        self.rect.centerx = 64
        self.rect.centery = 280
        self.dx = 0
        self.dy = 0
        self.dir = "none"

    def move_keydown(self, key):
        """update the paddle while the key is held down"""
        if key == K_UP:
            self.dy = -16
            self.dir = "up"
        elif key == K_DOWN:
            self.dy = 16
            self.dir = "down"

    def move_keyup(self):
        """once the key is release stop the paddle"""
        self.dy = 0
        self.dir = "none"

    def update(self, ball_sprite):
        self.rect.centery += self.dy
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()

class AI_Paddle(Paddle):
    def __init__(self, x_pos=(640 - 64), y_pos=280, difficulty="easy"):
        Paddle.__init__(self, x_pos, y_pos)
        self.difficulty = difficulty

    def reset(self):
        self.rect.centerx = 640 - 64
        self.rect.centery = 280
        self.dy = 0
        self.dir = "none"

    def update(self, ball_sprite):
        if self.difficulty == "easy":
            if ball_sprite.dx > 0 and ball_sprite.rect.centery < self.rect.centery - 8 \
                    and ball_sprite.rect.centerx > screen.get_width() // 2:
                self.dy = -8
                self.dir = "up"
            elif ball_sprite.dx > 0 and ball_sprite.rect.centery > self.rect.centery - 8 \
                    and ball_sprite.rect.centerx > screen.get_width() // 2:
                self.dy = 8
                self.dir = "down"
            else:
                self.dy = 0
                self.dir = "none"
        elif self.difficulty == "medium":
            if ball_sprite.dx > 0 and ball_sprite.rect.centery < self.rect.centery - 8 \
                    and ball_sprite.rect.centerx > screen.get_width() // 2 \
                    and ball_sprite.rect.centerx < 3 * screen.get_width() // 4:
                self.dy = -8
                self.dir = "up"
            elif ball_sprite.dx > 0 and ball_sprite.rect.centery < self.rect.centery - 8 \
                    and ball_sprite.rect.centerx > screen.get_width() // 2 \
                    and ball_sprite.rect.centerx >= (3 * screen.get_width() // 4):
                self.dy = -16
                self.dir = "up"
            elif ball_sprite.dx > 0 and ball_sprite.rect.centery > self.rect.centery - 8 \
                    and ball_sprite.rect.centerx > screen.get_width() // 2 \
                    and ball_sprite.rect.centerx < 3 * (screen.get_width() // 4):
                self.dy = 8
                self.dir = "down"
            elif ball_sprite.dx > 0 and ball_sprite.rect.centery > self.rect.centery - 8 \
                    and ball_sprite.rect.centerx > screen.get_width() // 2 \
                    and ball_sprite.rect.centerx >= 3 * (screen.get_width() // 4):
                self.dy = 16
                self.dir = "down"
            else:
                self.dy = 0
                self.dir = "none"
        if self.difficulty == "hard":
            if ball_sprite.dx > 0 and ball_sprite.rect.centery < self.rect.centery - 8 \
                    and ball_sprite.rect.centerx > screen.get_width() // 2:
                self.dy = -16
                self.dir = "up"
            elif ball_sprite.dx > 0 and ball_sprite.rect.centery > self.rect.centery - 8 \
                    and ball_sprite.rect.centerx > screen.get_width() // 2:
                self.dy = 16
                self.dir = "down"
            else:
                self.dy = 0
                self.dir = "none"
            
        self.rect.centery += self.dy
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
    
def main():
    # initialize pygame and the surfaces
    pygame.display.set_caption("Pypong - A pong remake in pygame")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # assign neccessary variables for play
    player = Paddle()
    ball = Ball()
    villian = AI_Paddle()
    score_label = Label(screen.get_width() // 2, 32, "")
    player_label = Label(6, 12, "0")
    enemy_label = Label(screen.get_width() - 6 , 12, "0")

    # group the appropriate sprites
    labelsprites = pygame.sprite.Group(score_label, player_label, enemy_label)    
    paddlesprites = pygame.sprite.Group(player, villian)
    ballsprites = pygame.sprite.Group(ball)
    enemysprites = pygame.sprite.Group(villian)

    clock = pygame.time.Clock()
    playing = True

    # main loop
    while playing:
        scored = False
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    playing = False
                elif event.key == K_UP or event.key == K_DOWN:
                    player.move_keydown(event.key)
                elif event.key == K_p:
                    score_label.text = "Paused, press P to unpause"
            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    player.move_keyup()

        # check for score
        # do this bit more gracefully
        if ball.rect.centerx < 0:
            score_label.text = "Computer Score!"
            villian.score += 1
            enemy_label.text = str(villian.score)
            if player.score >= 5:
                score_label.text = "Computer wins!"
        elif ball.rect.centerx > screen.get_width():
            score_label.text = "Player Score!"
            player.score += 1
            player_label.text = str(player.score)
            if player.score >= 5:
                score_label.text = "Player wins!"

        # clear the sprites
        paddlesprites.clear(screen, background)
        ballsprites.clear(screen, background)
        labelsprites.clear(screen, background)

        # update all sprites
        paddlesprites.update(ball)
        ballsprites.update(paddlesprites)
        labelsprites.update()

        # draw all sprites
        paddlesprites.draw(screen)
        ballsprites.draw(screen)
        labelsprites.draw(screen)

        pygame.display.flip()
        
        if score_label.text != "":
            if score_label.text != "Paused, press P to unpause":
                pygame.time.delay(640)
                score_label.text = ""
                ball.reset()
                player.reset()
                villian.reset()
            else:
                while score_label.text == "Paused, press P to unpause":
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            playing = False
                            score_label.text = ""
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                playing = False
                                score_label.text = ""
                            elif event.key == K_p:
                                score_label.text = ""
if __name__ == '__main__':
    main()
