# 게임 오버 처리

import math
import os
import pygame

# 집게 클래스
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.original_image = image
        self.position = position
        self.rect = image.get_rect(center=position)
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.direction = LEFT  # 집게의 이동 방향
        self.angle = 10  # 최초 각도 정의 (오른쪽 끝)
        self.angle_speed = 3.5  # 집게의 스피드

    def update(self, to_x):
        self.angle += self.direction * self.angle_speed
        if self.angle > 170:
            self.angle = 170
            self.set_direction(RIGHT)
        elif self.angle < 10:
            self.angle = 10
            self.set_direction(LEFT)

        self.offset.x += to_x
        self.rotate()

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.position + offset_rotated)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5)

    def set_direction(self, direction):
        self.direction = direction

    def set_init_state(self):
        self.offset.x = default_offset_x_claw
        self.angle = 10
        self.direction = LEFT


# 보석 클래스
class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position, price, speed):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.price = price
        self.speed = speed

    def set_position(self, position, angle):
        r = self.rect.size[0] // 2  # 반지름
        rad_angle = math.radians(angle)  # 각도
        to_x = r * math.cos(rad_angle)  # 삼각형의 밑변
        to_y = r * math.sin(rad_angle)  # 삼각형의 높이
        self.rect.center = (position[0] + to_x, position[1] + to_y)


def setup_gemstone():
    small_gold_price, small_gold_speed = 100, 10
    big_gold_price, big_gold_speed = 300, 5
    stone_price, stone_speed = 10, 5
    diamond_price, diamond_speed = 600, 13

    # 그룹에 추가
    gemstone_group.add(
        Gemstone(gemstone_images[0], (200, 380), small_gold_price, small_gold_speed)
    )
    gemstone_group.add(
        Gemstone(gemstone_images[1], (300, 500), big_gold_price, big_gold_speed)
    )
    gemstone_group.add(
        Gemstone(gemstone_images[2], (300, 380), stone_price, stone_speed)
    )
    gemstone_group.add(
        Gemstone(gemstone_images[3], (900, 420), diamond_price, diamond_speed)
    )


def update_score(score):
    global curr_score
    curr_score += score


def display_score():
    txt_curr_score = game_font.render(f"Curr Score: {curr_score:,}", True, BLACK)
    txt_goal_score = game_font.render(f"Goal Score: {goal_score:,}", True, BLACK)
    screen.blit(txt_curr_score, (50, 20))
    screen.blit(txt_goal_score, (50, 80))


def display_time(time):
    txt_timer = game_font.render(f"Time: {time}", True, BLACK)
    screen.blit(txt_timer, (1100, 50))


def display_mission_complete():
    game_font = pygame.font.SysFont("arialrounded", 60)  # 큰 폰트 적용
    txt_game_over = game_font.render("Mission Complete", True, BLACK)
    rect_game_over = txt_game_over.get_rect(
        center=(int(screen_width / 2), int(screen_height / 2))  # 화면 중앙에 표시
    )
    screen.blit(txt_game_over, rect_game_over)


def display_game_over():
    game_font = pygame.font.SysFont("arialrounded", 60)  # 큰 폰트 적용
    txt_game_over = game_font.render("Game Over", True, BLACK)
    rect_game_over = txt_game_over.get_rect(
        center=(int(screen_width / 2), int(screen_height / 2))  # 화면 중앙에 표시
    )
    screen.blit(txt_game_over, rect_game_over)


pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")

clock = pygame.time.Clock()
game_font = pygame.font.SysFont("arialrounded", 30)


# 게임 관련 변수
default_offset_x_claw = 40  # 기준점으로부터 집게의 x 간격
to_x = 0  # x 좌표 기준으로 집게 이미지를 이동시킬 값 저장
caught_gemstone = None  # 집게를 뻗어서 잡은 보석 정보

# 속도 변수
move_speed = 17  # 발사할 때 이동 스피드 (x 좌표 기준으로 증가되는 값)
return_speed = 20  # 아무것도 없이 돌아올 때 스피드

# 색깔 변수
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 방향 변수
LEFT = 1
STOP = 0  # 집게를 뻗음
RIGHT = -1

# 점수 관련 변수
goal_score = 10  # 목표 점수
curr_score = 0  # 현재 점수

# 게임 오버 관련 변수
total_time = 10  # 제한 시간
start_ticks = pygame.time.get_ticks()  # 현재 시간을 받아옴

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)  # 현재 파일 위치
background = pygame.image.load(os.path.join(current_path, "images/background.png"))

# 4개 보석 이미지 불러오기 (작은 금, 큰 금, 돌, 다이아몬드)
gemstone_images = [
    pygame.image.load(
        os.path.join(current_path, "images/small_gold.png")
    ).convert_alpha(),  # 작은 금
    pygame.image.load(
        os.path.join(current_path, "images/big_gold.png")
    ).convert_alpha(),  # 큰 금
    pygame.image.load(
        os.path.join(current_path, "images/stone.png")
    ).convert_alpha(),  # 돌
    pygame.image.load(
        os.path.join(current_path, "images/diamond.png")
    ).convert_alpha(),  # 다이아몬드
]

# 보석 그룹
gemstone_group = pygame.sprite.Group()
setup_gemstone()  # 게임에 원하는 만큼의 보석을 정의

# 집게
claw_image = pygame.image.load(
    os.path.join(current_path, "images/claw.png")
).convert_alpha()
claw = Claw(claw_image, ((screen_width // 2, 110)))

running = True

while running:
    clock.tick(30)  # FPS 값이 30으로 고정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            claw.set_direction(STOP)  # 좌우 멈춤
            to_x = move_speed  # move_speed 만큼 빠르게 쭉 뻗음

    if (
        claw.rect.left < 0  # 화면 밖으로 나가면
        or claw.rect.right > screen_width
        or claw.rect.bottom > screen_height
    ):
        to_x = -return_speed

    if claw.offset.x < default_offset_x_claw:  # 원위치에 오면
        to_x = 0
        claw.set_init_state()  # 처음 상태로 되돌림

        if caught_gemstone:  # 잡힌 보석이 있다면
            update_score(caught_gemstone.price)
            gemstone_group.remove(caught_gemstone)
            caught_gemstone = None

    if not caught_gemstone:  # 잡힌 보석이 없다면 충돌체크
        for gemstone in gemstone_group:
            # if claw.rect.colliderect(gemstone.rect): # 직사각형 기준으로 충돌처리
            # 투명 영역 제외하고 실제 이미지 영역이 존재하는 부분에 대해 충돌 처리
            if pygame.sprite.collide_mask(claw, gemstone):
                caught_gemstone = gemstone  # 잡힌 보석
                to_x = -gemstone.speed  # 잡힌 보석의 속도에 - 한 값을 이동 속도로 설정
                break
    if caught_gemstone:
        caught_gemstone.set_position(claw.rect.center, claw.angle)

    screen.blit(background, (0, 0))
    gemstone_group.draw(screen)
    claw.update(to_x)  # 집게를 그리기 직전에 위치 조정
    claw.draw(screen)
    display_score()

    # 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # ms -> s
    display_time(total_time - int(elapsed_time))

    if curr_score >= goal_score:
        running = False
        display_mission_complete()

    elif total_time - elapsed_time <= 0:
        running = False
        display_game_over()

    pygame.display.update()

pygame.time.delay(2000)  # 2초 정도 delay
pygame.quit()
