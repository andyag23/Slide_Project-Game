import pygame
import random
import os

WHITH = 500
HEIGHT = 600
FPS = 60

# 遊戲初始化 and 創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WHITH, HEIGHT))
# 改標題名字
pygame.display.set_caption("飛機打幽浮")
clock = pygame.time.Clock()

#載入圖片
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
boat_img = pygame.image.load(os.path.join("img","boat.png")).convert()
#rock_img = pygame.image.load(os.path.join("img","rock_new.png")).convert()
rock_imgs = []
for i in range(6):
    #字串裡面要變數，可以在前面加上f
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock_{i}.png")).convert())
#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("music","shoot1.mp3"))
rock_bomb = pygame.mixer.Sound(os.path.join("music","bomb.mp3"))
pygame.mixer.music.load(os.path.join("music","BGM.mp3"))
pygame.mixer.music.set_volume(0.8)

#遊戲字體
font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    #這邊的布林值是->是否要使用反鋸齒
    text_surface = font.render(text,True,(255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

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
        self.radius = 14.5
        #測試用
        #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
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
        shoot_sound.set_volume(0.4)
        shoot_sound.play()

#石頭物件
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((30, 40))
        #self.image.fill((255, 0, 0))
        #解決失針
        #self.image_ori = pygame.transform.scale(random.choice(rock_imgs),(60,40))
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey((255,255,255))
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.8 / 2)
        #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
        self.rect.x = random.randrange(0, WHITH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rote_degree = random.randrange(-3,3)

    def rotate(self):
        self.total_degree += self.rote_degree
        self.total_degree = self.total_degree % 360
        #單純這一行會有失針的問題
        self.image = pygame.transform.rotate(self.image_ori,self.total_degree)
        #解決抽動問題
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WHITH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WHITH - self.rect.width)
            self.rect.y = random.randrange(-240, -180)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)

#子彈物件
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img,(10,40))
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

#起始分數
Score = 0
#無限重複撥放背景音樂
pygame.mixer.music.play(-1)
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
        rock_bomb.set_volume(0.4)
        rock_bomb.play()
        Score += hit.radius
        rock = Rock()
        all_sprite.add(rock)
        rocks.add(rock)
    
    #pygame.sprite.collide_circle -> 圓形的精準判斷，原本為矩形
    crush = pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle)
    if crush:
        running = False

    #畫面顯示
    screen.fill((0,0,0))
    all_sprite.draw(screen)
    draw_text(screen,str(Score),18,WHITH/2,10)
    pygame.display.update()

pygame.quit()