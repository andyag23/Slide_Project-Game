import pygame

W = 500
H = 600
FPS = 60
P_W,P_H = 50,40
P_X,P_Y = W/2,H/2
pygame.init()
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("我的遊戲")
clock = pygame.time.Clock()

#遊戲函式
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((P_W,P_H))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = W/2
        self.rect.y = H/2
        self.speedx = 8
    
    def update(self): #update的函式
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speedx
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speedx
        # 不超過視窗
        if self.rect.right > W:
            self.rect.right = W
        if self.rect.left < 0:
            self.rect.left =0
        if self.rect.bottom > H:
            self.rect.bottom = H
        if self.rect.top < 0:
            self.rect.top = 0
All_sprites = pygame.sprite.Group()
player = Player()
All_sprites.add(player)

running = True

#遊戲迴圈
while running:
    clock.tick(FPS) #一秒鐘只能執行N次
    # 取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新遊戲
    All_sprites.update() #動圖片動起來

    # 畫面顯示
    screen.fill((0,0,0))
    All_sprites.draw(screen)
    pygame.display.update()

pygame.QUIT