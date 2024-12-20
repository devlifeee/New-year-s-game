import pygame 
import random 
 
#инициализация Pygame 
pygame.init() 
 
#константы-параметры окна 
WIDTH = 1380 
HEIGHT = 700 
#константы-цвета 
WHITE = (255, 255, 255) 
BLUE = (0, 0, 255) 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
GOLD = (255, 215, 0) 
BLACK = (0, 0, 0) 
 
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("НОВОГОДНЯЯ ИГРА")


icon = pygame.image.load("img/New Piskel (2).png")
pygame.display.set_icon(icon)

         
#класс для игрока 
class Player(pygame.sprite.Sprite): 
    def __init__(self, x, y, width=60, height=60, image_path="img/New Piskel (2).png"): #Добавлен параметр image_path, width и height по умолчанию
        super().__init__()

        # Загрузка изображения
        try:
            self.image = pygame.image.load(image_path).convert_alpha() # convert_alpha() для прозрачности
            self.image = pygame.transform.scale(self.image, (width, height)) #Масштабирование
        except pygame.error as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image = pygame.Surface((width, height)) #создаем пустую поверхность если изображение не загрузилось
            self.image.fill(GOLD) # Заполняем ее золотым цветом в качестве заглушки

 
        #создание хитбокса для спрайта 
        self.rect = self.image.get_rect() 
        self.rect.x = x 
        self.rect.y = y 
 
        #компоненты скорости по оси X и Y 
        self.x_velocity = 0 
        self.y_velocity = 0 
 
        #переменная-флаг для отслеживания в прыжке ли спрайт 
        self.on_ground = False 
 
    def update(self): 
        # Обновление позиции игрока 
        self.rect.x += self.x_velocity 
        self.rect.y += self.y_velocity 
 
#класс для патрулирующих врагов 
class Enemy(pygame.sprite.Sprite): 
    def __init__(self, x, y, width=60, height=60, image_path="img/гном.png"): #Добавлен параметр image_path, width и height по умолчанию
        super().__init__()

        # Загрузка изображения
        try:
            self.image = pygame.image.load(image_path).convert_alpha() # convert_alpha() для прозрачности
            self.image = pygame.transform.scale(self.image, (width, height)) #Масштабирование
        except pygame.error as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image = pygame.Surface((width, height)) #создаем пустую поверхность если изображение не загрузилось
            self.image.fill(GOLD) # Заполняем ее золотым цветом в качестве заглушки
 
        #начальная позиция по Х, нужна для патрулирования 
        self.x_start = x 
        #выбор направления начального движения 
        self.direction = random.choice([-1, 1]) 
 
        #создание хитбокса для спрайта 
        self.rect = self.image.get_rect() 
        self.rect.x = x 
        self.rect.y = y 
 
        #компоненты скорости по оси Х и Y 
        self.x_velocity = 1 
        self.y_velocity = 0 
     
    def update(self): 
        #если расстояние от начальной точки превысило 50 
        #то меняем направление 
        if abs(self.x_start - self.rect.x) > 50: 
            self.direction *= -1 
 
        #движение спрайта по оси Х 
        self.rect.x += self.x_velocity * self.direction 

#подарки
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, width=40, height=40, image_path="img\podarok.png"): #Добавлен параметр image_path, width и height по умолчанию
        super().__init__()

        # Загрузка изображения
        try:
            self.image = pygame.image.load(image_path).convert_alpha() # convert_alpha() для прозрачности
            self.image = pygame.transform.scale(self.image, (width, height)) #Масштабирование
        except pygame.error as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image = pygame.Surface((width, height)) #создаем пустую поверхность если изображение не загрузилось
            self.image.fill(GOLD) # Заполняем ее золотым цветом в качестве заглушки

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path="img\platform (1).png"): #Добавлен параметр image_path
        super().__init__()
        #Загрузка изображения
        try:
            self.image = pygame.image.load(image_path).convert_alpha() # convert_alpha() сохраняет прозрачность
        except pygame.error as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image = pygame.Surface((width, height)) #создаем пустую поверхность если изображение не загрузилось
            self.image.fill(WHITE) # Заполняем ее белым цветом в качестве заглушки

        #Масштабирование изображения (если нужно)
        self.image = pygame.transform.scale(self.image,(width, height))

        #создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#функция для проверки коллизий c платформой 
def check_collision_platforms(object, platform_list): 
    #перебираем все платформы из списка (не группы спрайтов) 
    for platform in platform_list: 
        if object.rect.colliderect(platform.rect): 
            if object.y_velocity > 0: # Если спрайт падает 
                #меняем переменную-флаг 
                object.on_ground = True 
                #ставим его поверх платформы и сбрасываем скорость по оси Y 
                object.rect.bottom = platform.rect.top 
                object.y_velocity = 0 
            elif object.y_velocity < 0: # Если спрайт движется вверх 
                #ставим спрайт снизу платформы 
                object.rect.top = platform.rect.bottom 
                object.y_velocity = 0 
            elif object.x_velocity > 0: # Если спрайт движется вправо 
                #ставим спрайт слева от платформы 
                object.rect.right = platform.rect.left 
            elif object.x_velocity < 0: # Если спрайт движется влево 
                #ставим спрайт справа от платформы 
                object.rect.left = platform.rect.right 
 
#функция проверки коллизии выбранного объекта с объектами Enemies 
def check_collision_enemies(object, enemies_list): 
    #running делаем видимой внутри функции чтобы было возможно 
    #завершить ить игру 
    global running 
    #в списке проверяем 
    for enemy in enemies_list: 
        #при коллизии 
        if object.rect.colliderect(enemy.rect): 
            #объект пропадает из всех групп спрайтов и игра заканчивается 
            object.kill() 
            running = False 
 
#функция проверки коллизии выбранного объекта с объектами Enemies 
def check_collision_enemies(object, enemies_list): 
    #running делаем видимой внутри функции чтобы было возможно 
    #завершить игру 
    global running 
    #в списке проверяем 
    for enemy in enemies_list: 
        #при коллизии 
        if object.rect.colliderect(enemy.rect): 
            #объект пропадает из всех групп спрайтов и игра заканчивается 
            object.kill() 
            running = False 
 
#проверка  
def check_collision_collectibles(object): 
    #делаем видимыми объекты для подбора в игре и очки 
    global collectibles_list 
    global score 
    #если object касается collictible  
    for collectible in collectibles_list: 
        if object.rect.colliderect(collectible.rect): 
            #убираем этот объект из всех групп 
            collectible.kill() 
            #убираем этот объект из списка (чтобы не было проверки коллизии) 
            collectibles_list.remove(collectible) 
            #прибавляем одно очко 
            score += 1 
 
 
#создаем экран, счетчик частоты кадров и очков 
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
clock = pygame.time.Clock() 
score = 0 
 
#создаем игрока, платформы, врагов и то, что будем собирать в игре 
player = Player(50, 50) 
# все остальные платфоры (певрое значение это расстояние от левого края, второе значение это расстояние от верха,
# третье значение это длина платформы, а последнее ширина платформы
platforms_list = [Platform(200, 600, 100, 20), Platform(500, 400, 100, 20), Platform(1220, 210, 100, 20), 
                  Platform(450, 170, 100, 20), Platform(500, 300, 100, 20), Platform(650, 200, 100, 20), 
                  Platform(1200, 370, 100, 20), Platform(1020, 300, 100, 20), Platform(990, 300, 100, 20), 
                  Platform(0, 250, 300, 20), Platform(220, 350, 100, 20), Platform(700, 350, 100, 20),
                  Platform(950, 170, 100, 20), Platform(800, 570, 100, 20), Platform(1090, 500, 100, 20), 
                  Platform(0, 600, 100, 20), Platform(600, 600, 100, 20), Platform(1000, 600, 100, 20),
                  Platform(420, 560, 100, 20)] 



platform_start = [Platform(0, 170, 200, 20),] #начальная платформа 

collectibles_list = [] 
for platform in platforms_list: 
    x = random.randint(platform.rect.x, platform.rect.x + platform.rect.width - 16) 
    y = platform.rect.y - 32   # Поднимаем Collectible над платформой 
    collectibles_list.append(Collectible(x, y)) 
 
# Создаем врагов 
enemies_list = [] 
num_enemies = 5
if len(platforms_list) >= num_enemies:
    selected_platforms = random.sample(platforms_list, num_enemies)
    for platform in selected_platforms:
        x = random.randint(platform.rect.x, platform.rect.x + platform.rect.width - 0)
        y = platform.rect.y - 50
        enemies_list.append(Enemy(x, y))
 
#счёт игры 
font = pygame.font.Font(None, 36) # создание объекта, выбор размера шрифта 
score_text = font.render("Подарков: 0", True, BLACK) # выбор цвета и текст 
score_rect = score_text.get_rect() # создание хитбокса текста 
score_rect.topleft = (WIDTH // 60, 10) # расположение хитбокса\текста на экране 
 
#создаем групп спрайтов 
player_and_platforms = pygame.sprite.Group() 
enemies = pygame.sprite.Group() 
collectibles = pygame.sprite.Group() 
 
#в трех циклах добавляем объекты в соответствующие группы 
for i in enemies_list: 
    enemies.add(i) 
 
for i in platforms_list: 
    player_and_platforms.add(i) 
  
for i in platform_start: 
    player_and_platforms.add(i)

for i in collectibles_list: 
    collectibles.add(i) 


    
 
#отдельно добавляем игрока 
player_and_platforms.add(player) 
 
#игровой цикл 
running = True 
 
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
 
    #проверяем нажатие на клавиши для перемещения 
    keys = pygame.key.get_pressed() 
    player.x_velocity = 0 
    if keys[pygame.K_LEFT]: 
        player.x_velocity = -5             
    if keys[pygame.K_RIGHT]: 
        player.x_velocity = 5 
    #условие прыжка более сложное 
    if keys[pygame.K_SPACE] and player.on_ground == True: 
        player.y_velocity = -9 
        player.on_ground = False 
 
    #гравитация для игрока 
    player.y_velocity += 0.3  
 
    #обновляем значения атрибутов игрока и врагов 
    player.update() 
    enemies.update() 
 
    # Проверка, упал ли игрок за пределы экрана 
    if player.rect.y > HEIGHT: 
        running = False  # Завершить игру, если игрок упал вниз 
 
 
    #отрисовываем фон, платформы, врагов и собираемые предметы 
    #screen.fill(WHITE)
    land = pygame.image.load("img\фон.jpg")
    land = pygame.transform.scale(land, (WIDTH, HEIGHT)) # Масштабируем до размеров экрана
    screen.blit(land, (0, 0))

    player_and_platforms.draw(screen) 
    enemies.draw(screen) 
    collectibles.draw(screen) 

    #отрисовываем игровые элементы (платформы, враги, собираемые предметы)
    player_and_platforms.draw(screen)
    enemies.draw(screen)
    collectibles.draw(screen)
    

    #проверяем все возможные коллизии 
    check_collision_platforms(player, platforms_list) 
    check_collision_platforms(player, platform_start) 
    check_collision_enemies(player, enemies_list) 
    check_collision_collectibles(player) 
 
    #обновление счёта на экране 
    score_text = font.render("КОЛИЧЕСТВО СОБРАННЫХ ПОДАРКОВ: " + str(score), True, WHITE) 
    screen.blit(score_text, score_rect) 
 
    #обновление экрана и установка частоты кадров 
    pygame.display.update() 
    clock.tick(70) 

    # Основной игровой цикл
running = True
clock = pygame.time.Clock()
show_cutscene = False





   
#пауза 
#def pause(): 
#    pygame.mixer.music.pause() 
#     
#    pause = True 
#    while pause: 
#        for event in pygame.event.get(): 
#            if event.type == pygame.QUIT: 
#                pygame.quit() 
#                quit() 
# 
#        #print_text("Paused. Press enter to continue", 320, 300) 
# 
#        keys = pygame.key.get_pressed() 
#        if keys[pygame.K_RETURN]: 
#            pause = False 
# 
#        pygame.display.update() 
#        clock.tick(15) 
# 
#    pygame.mixer.music.unpause() 
 
# Загружаем изображение катсцены
cutscene_image = pygame.image.load("img/New Piskel (8).png").convert() # Замените на путь к вашему изображению

pygame.quit()