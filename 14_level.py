# 레벨 시스템

import math
import os
import pygame
import random

# 보석 정보

gemstone_init = {
    "small_gold": {  # 작은 금
        "count_range": (4, 7),  # 개수 범위
        "x_pos_range": (200, 1150),  # 위치 범위 (x,y)
        "y_pos_range": (330, 600),
    },
    "big_gold": {  # 큰 금
        "count_range": (1, 4),
        "x_pos_range": (200, 1150),
        "y_pos_range": (400, 600),
    },
    "stone": {  # 돌
        "count_range": (3, 5),
        "x_pos_range": (300, 950),
        "y_pos_range": (330, 560),
    },
    "diamond": {  # 다이아몬드
        "count_range": (1, 3),
        "x_pos_range": (200, 1150),
        "y_pos_range": (500, 600),
    },
}

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
        self.angle = 15  # 최초 각도 정의 (오른쪽 끝)
        self.angle_speed = 3.5  # 집게의 스피드
        self.next_angle_speed = +0.05
        self.pick_speed = 10  # 발사할 때 이동 스피드 (x 좌표 기준으로 증가되는 값)
        self.return_speed = 1.3  # 아무것도 없이 돌아올 때 스피드 (pick_speed의 몇 배)
        self.next_pick_speed = +0.5  # 다음 레벨에서 증가할 집게의 속도

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

    def upgrade_speed(self):
        self.angle_speed += self.next_angle_speed
        self.pick_speed += self.next_pick_speed


# 보석 클래스
class Gemstone(pygame.sprite.Sprite):
    def set_position(self, position, angle):
        r = self.rect.size[0] // 2  # 반지름
        rad_angle = math.radians(angle)  # 각도
        to_x = r * math.cos(rad_angle)  # 삼각형의 밑변
        to_y = r * math.sin(rad_angle)  # 삼각형의 높이
        self.rect.center = (position[0] + to_x, position[1] + to_y)


class SmallGold(Gemstone):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(current_path, "images/small_gold2.png")
        ).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.price = 150
        self.speed = 0.8


class BigGold(Gemstone):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(current_path, "images/big_gold2.png")
        ).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.price = 300
        self.speed = 0.4


class Stone(Gemstone):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(current_path, "images/stone2.png")
        ).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.price = 50
        self.speed = 0.5


class Diamond(Gemstone):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(current_path, "images/diamond2.png")
        ).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.price = 600
        self.speed = 1


def create_gemstone(stone_name, x_range, y_range):
    x = random.randint(x_range[0], x_range[1])
    y = random.randint(y_range[0], y_range[1])

    if stone_name == "small_gold":
        return SmallGold((x, y))
    elif stone_name == "big_gold":
        return BigGold((x, y))
    elif stone_name == "stone":
        return Stone((x, y))
    elif stone_name == "diamond":
        return Diamond((x, y))
    else:
        raise NameError


def create_random_gemstone():
    new_stone = random.choice(["small_gold", "big_gold", "stone", "diamond"])
    return create_gemstone(
        new_stone,
        gemstone_init[new_stone]["x_pos_range"],
        gemstone_init[new_stone]["y_pos_range"],
    )


def setup():
    def is_overlaped(new_stone):
        for stone in gemstone_group:
            if pygame.sprite.collide_mask(new_stone, stone):
                return True
        return False

    global gemstone_group
    gemstone_group.empty()
    total_score = 0

    for stone_name in ["small_gold", "big_gold", "stone", "diamond"]:
        a = gemstone_init[stone_name]["count_range"][0]
        b = gemstone_init[stone_name]["count_range"][1]
        i = random.randint(a, b)
        while i > 0:
            new_stone = create_gemstone(
                stone_name,
                gemstone_init[stone_name]["x_pos_range"],
                gemstone_init[stone_name]["y_pos_range"],
            )

            if not is_overlaped(new_stone):
                gemstone_group.add(new_stone)
                total_score += new_stone.price
                i -= 1
    while total_score < goal_score + 200:
        new_stone = create_random_gemstone()
        if not is_overlaped(new_stone):
            gemstone_group.add(new_stone)
            total_score += new_stone.price


def update_score(score):
    global curr_score
    curr_score += score


def display_score():
    txt_curr_score = game_font.render(f"Curr Score: {curr_score:,}", True, BLACK)
    txt_goal_score = game_font.render(f"Goal Score: {goal_score:,}", True, BLACK)
    screen.blit(txt_curr_score, (50, 100))
    screen.blit(txt_goal_score, (50, 130))


def display_time(time):
    txt_color = BLACK if time > 10 else RED
    txt_timer = game_font.render(f"Time: {time}", True, txt_color)
    screen.blit(txt_timer, (1100, 50))


def level_up():
    global level, goal_score, curr_score, start_ticks
    level += 1
    curr_score = 0
    goal_score += next_score
    start_ticks = pygame.time.get_ticks()
    claw.upgrade_speed()


def display_level():
    game_font = pygame.font.SysFont("arialrounded", 60)  # 큰 폰트 적용
    txt_level = game_font.render(f"Level {level}", True, BLACK)
    screen.blit(txt_level, (50, 30))


def display_game_over():
    screen.fill(BLACK)
    game_font = pygame.font.SysFont("arialrounded", 90)  # 큰 폰트 적용
    txt_game_over = game_font.render(
        f"Game Over at level {level}",
        True,
        WHITE,
    )
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
returning = False  # 집게가 돌아오고 있는지
level = 1  # 레벨


# 색깔 변수
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 방향 변수
LEFT = 1
STOP = 0  # 집게를 뻗음
RIGHT = -1

# 점수 관련 변수
totel_score = 0  # 총 점수
goal_score = 300  # 목표 점수
curr_score = 0  # 현재 점수
next_score = +100  # 다음 레벨의 목표 점수

# 게임 오버 관련 변수
limit_time = 30  # 제한 시간
start_ticks = pygame.time.get_ticks()  # 현재 시간을 받아옴

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)  # 현재 파일 위치
background = pygame.image.load(os.path.join(current_path, "images/background.png"))


# 보석 그룹
gemstone_group = pygame.sprite.Group()
setup()  # 게임에 원하는 만큼의 보석을 정의

# 집게
claw_image = pygame.image.load(
    os.path.join(current_path, "images/claw.png")
).convert_alpha()
claw = Claw(claw_image, ((screen_width // 2, 110)))
running = True

# pygame.time.delay(2000)  # 2초 정도 delay

while running:
    clock.tick(30)  # FPS 값이 30으로 고정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if claw.direction != STOP:
            if event.type == pygame.MOUSEBUTTONDOWN:
                claw.set_direction(STOP)  # 좌우 멈춤
                to_x = claw.pick_speed  # pick_speed 만큼 빠르게 쭉 뻗음
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    claw.set_direction(STOP)  # 좌우 멈춤
                    to_x = claw.pick_speed  # pick_speed 만큼 빠르게 쭉 뻗음

    if (
        claw.rect.left < 0  # 화면 밖으로 나가면
        or claw.rect.right > screen_width
        or claw.rect.bottom > screen_height
    ):
        to_x = -(claw.pick_speed * claw.return_speed)
        returning = True

    if claw.offset.x < default_offset_x_claw:  # 원위치에 오면
        to_x = 0
        returning = False
        claw.set_init_state()  # 처음 상태로 되돌림

        if caught_gemstone:  # 잡힌 보석이 있다면
            update_score(caught_gemstone.price)
            gemstone_group.remove(caught_gemstone)
            caught_gemstone = None

    if caught_gemstone:
        caught_gemstone.set_position(claw.rect.center, claw.angle)

    elif returning == False:  # 잡힌 보석이 없다면 충돌체크
        for gemstone in gemstone_group:
            # if claw.rect.colliderect(gemstone.rect): # 직사각형 기준으로 충돌처리
            # 투명 영역 제외하고 실제 이미지 영역이 존재하는 부분에 대해 충돌 처리
            if pygame.sprite.collide_mask(claw, gemstone):
                caught_gemstone = gemstone  # 잡힌 보석
                to_x = -(
                    claw.pick_speed * caught_gemstone.speed
                )  # 잡힌 보석의 속도에 - 한 값을 이동 속도로 설정
                break

    screen.blit(background, (0, 0))
    gemstone_group.draw(screen)
    claw.update(to_x)  # 집게를 그리기 직전에 위치 조정
    claw.draw(screen)
    display_score()
    display_level()

    # 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # ms -> s
    display_time(limit_time - int(elapsed_time))

    if curr_score >= goal_score:
        level_up()
        setup()
        # pygame.time.delay(2000)  # 2초 정도 delay

    elif limit_time - elapsed_time <= 0:
        running = False
        display_game_over()

    pygame.display.update()

pygame.time.delay(2000)  # 2초 정도 delay
pygame.quit()
