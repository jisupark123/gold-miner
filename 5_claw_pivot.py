# 집게 배치

import os
import pygame

# 집게 클래스
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

    def update(self):
        rect_center = self.position + self.offset
        self.rect = self.image.get_rect(center=rect_center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3)


# 보석 클래스
class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)


def setup_gemstone():
    gemstone_group.add(Gemstone(gemstone_images[0], (200, 380)))  # 그룸에 추가
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500)))
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380)))
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420)))


pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")

clock = pygame.time.Clock()

# Constant
RED = (255, 0, 0)
default_offset_x_claw = 40  # 기준점으로부터 집게의 x 간격

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)  # 현재 파일 위치
background = pygame.image.load(os.path.join(current_path, "images/background.png"))

# 4개 보석 이미지 불러오기 (작은 금, 큰 금, 돌, 다이아몬드)
gemstone_images = [
    pygame.image.load(os.path.join(current_path, "images/small_gold.png")),  # 작은 금
    pygame.image.load(os.path.join(current_path, "images/big_gold.png")),  # 큰 금
    pygame.image.load(os.path.join(current_path, "images/stone.png")),  # 돌
    pygame.image.load(os.path.join(current_path, "images/diamond.png")),  # 다이아몬드
]

# 보석 그룹
gemstone_group = pygame.sprite.Group()
setup_gemstone()  # 게임에 원하는 만큼의 보석을 정의

# 집게
claw_image = pygame.image.load(os.path.join(current_path, "images/claw.png"))
claw = Claw(claw_image, ((screen_width // 2, 110)))

running = True

while running:
    clock.tick(30)  # FPS 값이 30으로 고정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    gemstone_group.draw(screen)
    claw.update()  # 집게를 그리기 직전에 위치 조정
    claw.draw(screen)
    pygame.display.update()

pygame.quit()
