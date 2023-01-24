import pygame

WHITH = 500
HEIGHT = 600

# 遊戲初始化 and 創建視窗
pygame.init()
screen = pygame.display.set_mode((WHITH,HEIGHT))
clock = pygame.time.Clock()
FPS = 60

running = True

#遊戲迴圈
while running:
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #更新遊戲

    #畫面顯示
    screen.fill((0,0,0))
    pygame.display.update()

pygame.quit()