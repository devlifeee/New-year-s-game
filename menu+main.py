from pygame import *
import pygame 
import random 

pygame.init()
width = 1380
height = 700

screen = pygame.display.set_mode((width, height))

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ARIAL_50 = pygame.font.SysFont("arial", 50)  

def show_menu():
    # Загрузка изображения фона
    background_image = pygame.image.load("img\фон меню.png")  
    background_image = pygame.transform.scale(background_image, (width, height))  # Масштабируем под размер экрана
    
    screen.blit(background_image, (0, 0))  # Отображаем фон
    
    # Загрузка изображения для кнопки "Старт"
    play_image = pygame.image.load("img\start-button.png")  
    play_image = pygame.transform.scale(play_image, (500, 350))  
    play_rect = play_image.get_rect(center=(width // 2, height // 3))  
    
    # Загрузка изображения для кнопки "Настройки"
    settings_image = pygame.image.load("img\settings.png")
    settings_image = pygame.transform.scale(settings_image, (500, 350))
    settings_rect = settings_image.get_rect(center=(width // 2, height // 2 + 100))
    
    screen.blit(play_image, play_rect)
    screen.blit(settings_image, settings_rect)
    
    pygame.display.flip()
    
    return play_rect, settings_rect 

def settings():
    settings_running = True
    
    # Загрузка изображения фона
    background_image = pygame.image.load('img\фон меню.png')
    
    while settings_running:
        # Отображение фона
        screen.blit(background_image, (0, 0))
        
        # Отображение текста настроек
        settings_text = ARIAL_50.render("Настройки", True, WHITE)
        screen.blit(settings_text, (width // 2 - settings_text.get_width() // 2, height // 4))
        
        # Отображение кнопки "Назад"
        back_text = ARIAL_50.render("Назад", True, WHITE)
        back_rect = back_text.get_rect(center=(width // 2, height // 2))
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                settings_running = False
            if event.type == MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):  # Возврат в главное меню
                    settings_running = False

def show_game_over_menu():
    background_image = pygame.image.load("img\фон меню.png")  
    background_image = pygame.transform.scale(background_image, (width, height))  # Масштабируем под размер экрана
    screen.blit(background_image, (0, 0))  # Отображаем фон
    
    game_over_text = ARIAL_50.render("Игра окончена", True, WHITE)
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))
    
    menu_text = ARIAL_50.render("В главное меню", True, WHITE)
    menu_rect = menu_text.get_rect(center=(width // 2, height // 2 + 100))
    screen.blit(menu_text, menu_rect)
    
    pygame.display.flip()
    
    return menu_rect   # Возвращаем только прямоугольник для меню

# Основной игровой цикл
running = True  
play_rect, settings_rect = show_menu()  # Получаем оба прямоугольника

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):  # Переход к игре
                running = False  # Остановим меню, чтобы перейти к игре
            elif settings_rect.collidepoint(event.pos):  # Переход к меню настроек
                settings()  # Вызов функции настроек

    show_menu()

# ОСНОВНАЯ ИГРА
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

icon = pygame.image.load("img\MOROZ2.png")
pygame.display.set_icon(icon)

# Класс для игрока 
class Player(pygame.sprite.Sprite): 
    def __init__(self, x, y, width=60, height=60, image_path="img\DED_MOROZ.png"):
        super().__init__()
        # Загрузка изображения
        try:
            self.image = pygame.image.load(image_path).convert_alpha ()
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
    def __init__(self, x, y, width=60, height=60, image_path="img\гном.png"):
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
    def __init__(self, x, y, width=40, height=40, image_path="img\podarok.png"):
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

# Платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path="img\snow platform.png"):
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
            if object.y_velocity > 0:  # Если игрок падает
                object.on_ground = True 
                object.rect.bottom = platform.rect.top 
                object.y_velocity = 0 
            elif object.y_velocity < 0:  # Если игрок прыгает
                object.rect.top = platform.rect.bottom 
                object.y_velocity = 0 
            elif object.x_velocity > 0:  # Если игрок движется вправо
                object.rect.right = platform.rect.left 
            elif object.x_velocity < 0:  # Если игрок движется влево
                object.rect.left = platform.rect.right 

def check_collision_enemies(object, enemies_group): 
    global game_over 
    for enemy in enemies_group: 
        # Проверяем коллизию с врагом
        if object.rect.colliderect(enemy.rect): 
            # Проверяем, находится ли игрок на земле
            if object.on_ground:  # Игрок на земле
                game_over = True  # Устанавливаем флаг окончания игры
            else:  # Игрок в воздухе
                # Проверяем, падает ли игрок на врага
                if object.rect.bottom > enemy.rect.top and object.rect.centerx > enemy.rect.left and object.rect.centerx < enemy.rect.right:
                    game_over = True  # Игрок умирает, если падает на врага

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
                  Platform(0, 250, 300,20), Platform(220, 350, 100, 20), Platform(700, 350, 100, 20),
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

# Основной игровой цикл
running = True 
game_over = False  # Флаг для отслеживания состояния игры

# Показать начальное меню
play_rect, settings_rect = show_menu()  # Получаем прямоугольники для кнопок


while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False 

    if not game_over:  # Если игра не окончена
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
            game_over = True  # Игрок умер, показываем меню

        land = pygame.image.load("img\больший фон2.png")
        land = pygame.transform.scale(land, (WIDTH, HEIGHT)) 
        screen.blit(land, (0, 0))

        player_and_platforms.draw(screen) 
        enemies.draw(screen) 
        collectibles.draw(screen) 

        # Проверка коллизий
        check_collision_platforms(player, platforms_list) 
        check_collision_platforms(player, platform_start) 
        check_collision_enemies(player, enemies)  # Проверка коллизий с врагами
        check_collision_collectibles(player) 

        score_text = font.render(" ПОДАРКОВ: " + str(score), True, WHITE) 
        screen.blit(score_text, score_rect) 

    else:  # Если игра окончена, показываем меню
        menu_rect = show_game_over_menu()  # Получаем только прямоугольник для меню
        menu_running = True  # Флаг для отслеживания состояния меню
        while menu_running:  # Цикл для меню
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                    running = False  # Завершаем основную игру
                if event.type == MOUSEBUTTONDOWN:
                    if menu_rect.collidepoint(event.pos):  # Вернуться в главное меню
                        menu_running = False  # Выходим из меню
                        game_over = False  # Сбрасываем состояние игры
                        play_rect , settings_rect = show_menu()  # Показать главное меню

            pygame.display.update() 
            clock.tick(70) 

    pygame.display.update() 
    clock.tick(70) 

pygame.quit()
