from pygame import *
import pygame 
import random 

pygame.init()
width = 1380
height = 700


screen = pygame.display.set_mode((width, height))

def show_menu():
    screen.fill(BLACK)
    
    # Загрузка изображения для кнопки "Старт"
    play_image = pygame.image.load("img/start.png")  # Исправлено: заменен обратный слэш на прямой
    play_image = pygame.transform.scale(play_image, (300, 150))  # Увеличиваем размер кнопки
    
    play_rect = play_image.get_rect(center=(width // 2, height // 4))  # Центрируем кнопку
    
    screen.blit(play_image, play_rect)
    
    pygame.display.flip()
    
    return play_rect 

ARIAL_50 = pygame.font.SysFont("arial", 50)  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

running = True  
play_rect = show_menu()  # Получаем прямоугольник кнопки

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):  # Переход к игре
                # Здесь можно добавить код для перехода к игровому процессу
                running = False  # Остановим меню, чтобы перейти к игре

    show_menu()
#ОСНОВНАЯ ИГРА
# Константы-параметры окна 
WIDTH = 1380    
HEIGHT = 700 

# Константы-цвета 
WHITE = (255, 255, 255) 
BLUE = (0, 0, 255) 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
GOLD = (255, 215, 0) 
BLACK = (0, 0, 0) 

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("НОВОГОДНЯЯ ИГРА")

icon = pygame.image.load("img/MOROZ2.png")
pygame.display.set_icon(icon)

# Класс для игрока 
class Player(pygame.sprite.Sprite): 
    def __init__(self, x, y, width=60, height=60, image_path="img/DED_MOROZ.png"):
        super().__init__()
        # Загрузка изображения
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image = pygame.Surface((width, height))
            self.image.fill(GOLD)

        self.rect = self.image.get_rect() 
        self.rect.x = x 
        self.rect.y = y 
        self.x_velocity = 0 
        self.y_velocity = 0 
        self.on_ground = False 

    def update(self): 
        self.rect.x += self.x_velocity 
        self.rect.y += self.y_velocity 

# Класс для патрулирующих врагов 
class Enemy(pygame.sprite.Sprite): 
    def __init__(self, x, y, width=60, height=60, image_path="img/гном.png"):
        super().__init__()
        # Загрузка изображения
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image = pygame.Surface((width, height))
            self.image.fill(GOLD)

        self.x_start = x 
        self.direction = random.choice([-1, 1]) 
        self.rect = self.image.get_rect() 
        self.rect.x = x 
        self.rect.y = y 
        self.x_velocity = 1 
        self.y_velocity = 0 
        
    def update(self): 
        if abs(self.x_start - self.rect.x) > 50: 
            self.direction *= -1 
        self.rect.x += self.x_velocity * self.direction 

# Подарки
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, width=40, height=40, image_path="img/podarok.png"):
        super().__init__()
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image = pygame.Surface((width, height))
            self.image.fill(GOLD)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#ПЛАТФОРМЫ
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path="img/snow platform.png"):
        super().__init__()
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image = pygame.Surface((width, height))
            self.image.fill(WHITE)

        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def check_collision_platforms(object, platform_list): 
    for platform in platform_list: 
        if object.rect.colliderect(platform.rect): 
            if object.y_velocity > 0: 
                object.on_ground = True 
                object.rect.bottom = platform.rect.top 
                object.y_velocity = 0 
            elif object.y_velocity < 0: 
                object.rect.top = platform.rect.bottom 
                object.y_velocity = 0 
            elif object.x_velocity > 0: 
                object.rect.right = platform.rect.left 
            elif object.x_velocity < 0: 
                object.rect.left = platform.rect.right 

def check_collision_enemies(object, enemies_list): 
    global running 
    for enemy in enemies_list: 
        if object.rect.colliderect(enemy.rect): 
            object.kill() 
            running = False 

def check_collision_collectibles(object): 
    global collectibles_list 
    global score 
    for collectible in collectibles_list: 
        if object.rect.colliderect(collectible.rect): 
            collectible.kill() 
            collectibles_list.remove(collectible) 
            score += 1 

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
clock = pygame.time.Clock() 
score = 0 

player = Player(50, 50) 
platforms_list = [Platform(200, 600, 100, 20), Platform(500, 400, 100, 20), Platform(1220, 210, 100, 20), 
                  Platform(450, 170, 100, 20), Platform(500, 300, 100, 20), Platform(650, 200, 100, 20), 
                  Platform(1200, 370, 100, 20), Platform(1020, 300, 100, 20), Platform(990, 300, 100, 20), 
                  Platform(0, 250, 300, 20), Platform(220, 350, 100, 20), Platform(700, 350, 100, 20),
                  Platform(950, 170, 100, 20), Platform(800, 570, 100, 20), Platform(1090, 500, 100, 20), 
                  Platform(0, 600, 100, 20), Platform(600, 600, 100, 20), Platform(1000, 600, 100, 20),
                  Platform(420, 560, 100, 20)] 

platform_start = [Platform(0, 170, 200, 20),] 

collectibles_list = [] 
for platform in platforms_list: 
    x = random.randint(platform.rect.x, platform.rect.x + platform.rect.width - 16) 
    y = platform.rect.y - 32  
    collectibles_list.append(Collectible(x, y)) 

enemies_list = [] 
num_enemies = 5
if len(platforms_list) >= num_enemies:
    selected_platforms = random.sample(platforms_list, num_enemies)
    for platform in selected_platforms:
        x = random.randint(platform.rect.x, platform.rect.x + platform.rect.width - 0)
        y = platform.rect.y - 50
        enemies_list.append(Enemy(x, y))

font = pygame.font.Font(None, 36) 
score_text = font.render("Подарков: 0", True, BLACK) 
score_rect = score_text.get_rect() 
score_rect.topleft = (WIDTH // 60, 10) 

player_and_platforms = pygame.sprite.Group() 
enemies = pygame.sprite.Group() 
collectibles = pygame.sprite.Group() 

for i in enemies_list: 
    enemies.add(i) 

for i in platforms_list: 
    player_and_platforms.add(i) 

for i in platform_start: 
    player_and_platforms.add(i)

for i in collectibles_list: 
    collectibles.add(i) 

player_and_platforms.add(player) 

running = True 

while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False 

    keys = pygame.key.get_pressed() 
    player.x_velocity = 0 
    if keys[pygame.K_LEFT]: 
        player.x_velocity = -5             
    if keys[pygame.K_RIGHT]: 
        player.x_velocity = 5 
    if keys[pygame.K_SPACE] and player.on_ground: 
        player.y_velocity = -9 
        player.on_ground = False 

    player.y_velocity += 0.3  

    player.update() 
    enemies.update() 

    if player.rect.y > HEIGHT: 
        running = False  

    land = pygame.image.load("img/фон.jpg")
    land = pygame.transform.scale(land, (WIDTH, HEIGHT)) 
    screen.blit(land, (0, 0))

    player_and_platforms.draw(screen) 
    enemies.draw(screen) 
    collectibles.draw(screen) 

    check_collision_platforms(player, platforms_list) 
    check_collision_platforms(player, platform_start) 
    check_collision_enemies(player, enemies_list) 
    check_collision_collectibles(player) 

    score_text = font.render("КОЛИЧЕСТВО СОБРАННЫХ ПОДАРКОВ: " + str(score), True, WHITE) 
    screen.blit(score_text, score_rect) 

    pygame.display.update() 
    clock.tick(70) 

pygame.quit()