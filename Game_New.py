import pygame
import random
import os

WHITH = 500
HEIGHT = 600
FPS = 60

# 遊戲初始化 and 創建視窗
pygame.init()
screen = pygame.display.set_mode((WHITH, HEIGHT))
# 改標題名字
pygame.display.set_caption("飛機打幽浮")
clock = pygame.time.Clock()

#載入圖片
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
boat_img = pygame.image.load(os.path.join("img","boat.png")).convert()
rock_img = pygame.image.load(os.path.join("img","rock_new.png")).convert()

# 玩家物件
class Player(pygame.sprite.Sprite):
    # 初始函數固定寫法
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((50, 40))
        #self.image.fill((0, 255, 0))
        self.image = pygame.transform.scale(boat_img,(60,20))
        self.image.set_colorkey((0,0,0))
        # 把物件框起來
        self.rect = self.image.get_rect()
        self.rect.centerx = WHITH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        #if key_pressed[pygame.K_w]:
        #    self.rect.y -= self.speedx
        #if key_pressed[pygame.K_s]:
        #    self.rect.y += self.speedx
        # 不超過視窗
        if self.rect.right > WHITH:
            self.rect.right = WHITH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprite.add(bullet)
        bullets.add(bullet)

#石頭物件
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((30, 40))
        #self.image.fill((255, 0, 0))
        self.image = pygame.transform.scale(rock_img,(60,40))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WHITH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WHITH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WHITH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)

#子彈物件
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img,(20,40))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#設定群組
all_sprite = pygame.sprite.Group()
#多兩個群組是因為要判斷子彈跟石頭移動時接觸的判斷
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprite.add(player)
#迴圈降下石頭物件
for i in range(8):
    rock = Rock()
    all_sprite.add(rock)
    rocks.add(rock)
 
running = True

#遊戲迴圈
while running:
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #更新遊戲
    all_sprite.update()
    #groupcollide 布林值意義為物件碰撞後是否要消失
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        rock = Rock()
        all_sprite.add(rock)
        rocks.add(rock)
    
    crush = pygame.sprite.spritecollide(player,rocks,False)
    if crush:
        running = False

    #畫面顯示
    screen.fill((0,0,0))
    all_sprite.draw(screen)
    pygame.display.update()

pygame.quit()