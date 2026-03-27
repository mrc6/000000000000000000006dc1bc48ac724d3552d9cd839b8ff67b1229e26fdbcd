import pgzrun
from const import Constants
from enemy import Enemy

WIDTH = Constants.WIDTH
HEIGHT = Constants.HEIGHT

start_game = False
game_sound = True
enemy_list = []

def build_world(filename, tile_size):
    with open(filename, 'r') as f:
        contents = f.read().splitlines()
    f.close()
    contents = [c.split(",") for c in contents]

    for row in range(len(contents)):
        for col in range(len(contents[0])):
            val = contents[row][col]
            if val.isdigit() or (val[0] == '-' and val[1:].isdigit()):
                contents[row][col] = int(val)
    items = []

    for row in range(len(contents)):
        for col in range(len(contents[0])):
            tile_num = contents[row][col]
            if tile_num != -1:
                item = Actor(f'tiles/tile_{tile_num:04d}')
                item.topleft = (tile_size * col, tile_size * row)
                items.append(item)
    return items

def create_button(pos, image, screen):
    screen.blit(image, pos)

def play_sound(sound):
    if game_sound:
        command = 'sounds.' + sound + '.play'
        eval(command)()

def on_mouse_down(pos, button):
    global start_game
    global game_sound
    if button == 1 and pos[0] >= Constants.START_BUTTON_POS[0] and pos[0] <= (Constants.START_BUTTON_POS[0] + Constants.TILE_SIZE):
        if pos[1] >= Constants.START_BUTTON_POS[1] and pos[1] <= (Constants.START_BUTTON_POS[1] + Constants.TILE_SIZE):
            print("Start button clicked!")
            start_game = True

    if button == 1 and pos[0] >= Constants.QUIT_BUTTON_POS[0] and pos[0] <= (Constants.QUIT_BUTTON_POS[0] + Constants.TILE_SIZE):
        if pos[1] >= Constants.QUIT_BUTTON_POS[1] and pos[1] <= (Constants.QUIT_BUTTON_POS[1] + Constants.TILE_SIZE):
            print("Quit button clicked!")
            start_game = False
            exit()

    if button == 1 and pos[0] >= Constants.SOUND_BUTTON_POS[0] and pos[0] <= (Constants.SOUND_BUTTON_POS[0] + Constants.TILE_SIZE):
        if pos[1] >= Constants.SOUND_BUTTON_POS[1] and pos[1] <= (Constants.SOUND_BUTTON_POS[1] + Constants.TILE_SIZE):
            print("Sound button clicked!")
            game_sound = not game_sound

def collision_platform_x(platforms, hero):
    platform_left = False
    platform_right = False

    for tile in platforms:
        if hero.colliderect(tile):
            if hero.vx < 0:
                hero.left = tile.right
                platform_left = True
            elif hero.vx > 0:
                hero.right = tile.left
                platform_right = True
    return platform_left, platform_right

def collision_platform_y(platforms, hero):
    platform_under = False
    platform_over = False

    for tile in platforms:
        if hero.colliderect(tile):
            if hero.vy > 0:
                hero.bottom = tile.top
                hero.vy = 0
                platform_under = True
            elif hero.vy < 0:
                hero.top = tile.bottom
                hero.vy = 0
                platform_over = True
    return platform_under, platform_over

def animation_images_list(actor, animation=None, list_size=[]):
    images_list = []
    for i in range(list_size):
        if animation == None:
            images_list.append(f'{actor}_{i}')
        else:
            images_list.append(f'{actor}_{animation}_{i}')
    return images_list


hero = Actor('hero_idle_1')
hero.pos = Constants.HERO_START_POSITION
hero.vy = Constants.Y_SPEED_START
hero.vx = Constants.X_SPEED_START
hero_idle_frame = 0
hero_walk_frame = 0
hero_lives = Constants.HERO_LIVES

goal_flag = Actor('goal_flag_animation_1')
goal_flag.left, goal_flag.bottom = Constants.GOAL_FLAG_POSITION
goal_flag_frame = 0

tree_attack = Actor('tree_attack_0')

bee = Actor('bee_walkright_0')

bee1 = Actor('bee_walkright_0')

red_head = Actor('red_head_walkleft_0')

hero_idle_images = animation_images_list('hero', 'idle', 18)
hero_walk_right_images = animation_images_list('hero', 'walk_right', 2)
hero_walk_left_images = animation_images_list('hero', 'walk_left', 2)

bee_walk_right_images = animation_images_list('bee', 'walkright', 2)
bee_walk_left_images = animation_images_list('bee', 'walkleft', 2)

red_head_walk_right_images = animation_images_list('red_head', 'walkright', 2)
red_head_walk_left_images = animation_images_list('red_head', 'walkleft', 2)

tree_attack_animation_images = animation_images_list('tree_attack', None, 2)

goal_flag_animation_images = animation_images_list('goal_flag', 'animation', 2)

# animation callback functions
def animate_hero_idle():
    global hero_idle_frame
    if hero.vx == 0 and hero.vy == 0:
        hero_idle_frame = (hero_idle_frame + 1) % len(hero_idle_images)
        hero.image = hero_idle_images[hero_idle_frame]

def animate_hero_walk():
    global hero_walk_frame
    if hero.vx != 0:
        hero_walk_frame = (hero_walk_frame + 1) % len(hero_walk_right_images)
        if hero.vx > 0:
            hero.image = hero_walk_right_images[hero_walk_frame]
        else:
            hero.image = hero_walk_left_images[hero_walk_frame]

def animate_goal_flag():
    global goal_flag_frame
    goal_flag_frame = (goal_flag_frame + 1) % len(goal_flag_animation_images)
    goal_flag.image = goal_flag_animation_images[goal_flag_frame]

def animate_bee_walk():
    for enemy in enemy_list:
        enemy_filename = str(enemy.image)
        if enemy_filename.startswith('bee'):
            if enemy.vx != 0:
                enemy.frame = (enemy.frame + 1) % len(bee_walk_right_images)
                if enemy.vx > 0:
                    enemy.image = bee_walk_right_images[enemy.frame]
                else:
                    enemy.image = bee_walk_left_images[enemy.frame]

def animate_red_head_walk():
    if red_head.vx != 0:
        red_head.frame = (red_head.frame + 1) % len(red_head_walk_right_images)
        if red_head.vx > 0:
            red_head.image = red_head_walk_right_images[red_head.frame]
        else:
            red_head.image = red_head_walk_left_images[red_head.frame]

def animate_tree_attack():
    tree_attack.frame = (tree_attack.frame + 1) % len(tree_attack_animation_images)
    tree_attack.image = tree_attack_animation_images[tree_attack.frame ]

platforms = build_world('platform_map.csv', Constants.TILE_SIZE)
obstacles = build_world('obstacle_map.csv', Constants.TILE_SIZE)
enemy_tree = Enemy.create_enemy(tree_attack, 10, 11, 0, enemy_list)
enemy_red_head = Enemy.create_enemy(red_head, 24, 4, Constants.RED_HEAD_WALK_SPEED, enemy_list)
enemy_bee_1 = Enemy.create_enemy(bee, 0, 4, Constants.BEE_WALK_SPEED, enemy_list)
enemy_bee_2 = Enemy.create_enemy(bee1, 0, 4, Constants.BEE_WALK_SPEED/2, enemy_list)

def draw():
    clock.schedule_interval(animate_hero_idle, Constants.HERO_IDLE_SPEED)
    clock.schedule_interval(animate_hero_walk, Constants.HERO_WALK_SPEED)
    clock.schedule_interval(animate_goal_flag, Constants.GOAL_FLAG_ANIMATION_SPEED)
    clock.schedule_interval(animate_tree_attack, Constants.TREE_ATTACK_SPEED )
    clock.schedule_interval(animate_bee_walk, Constants.BEE_WALK_SPEED)
    clock.schedule_interval(animate_red_head_walk, Constants.RED_HEAD_WALK_SPEED)
    
    screen.clear()
    screen.fill('skyblue')
    screen.draw.text("FLAG HUNTER", (WIDTH/2, 210), width=400, lineheight=1.5)

    create_button(Constants.START_BUTTON_POS, 'start_button.png', screen)
    if not game_sound:
        create_button(Constants.SOUND_BUTTON_POS, 'sound_button_1.png', screen)
    else:
        create_button(Constants.SOUND_BUTTON_POS, 'sound_button_0.png', screen)
    create_button(Constants.QUIT_BUTTON_POS, 'quit_button.png', screen)

    if start_game:
        screen.clear()
        screen.fill('skyblue')

        screen.draw.text("Lifes " + str(hero_lives), (WIDTH-100, 100))

        for platform in platforms:
            platform.draw()
    
        for obstacle in obstacles:
            obstacle.draw()
    
        hero.draw()
        goal_flag.draw()

        for enemy in enemy_list:
            enemy.draw()

def update():
    global start_game
    global hero_lives

    if keyboard.down:
        start_game = True

    if keyboard.escape:
        exit()

    if hero_lives <= 0:
        start_game = False
        hero_lives = Constants.HERO_LIVES
    
    if start_game:
        Enemy.enemy_walk(enemy_list[enemy_bee_1], 0, WIDTH)
        Enemy.enemy_walk(enemy_list[enemy_bee_2], 0, WIDTH)
        Enemy.enemy_walk(enemy_list[enemy_red_head], Constants.RED_HEAD_TILES_MIN, Constants.RED_HEAD_TILES_MAX)

    hero.vy = hero.vy + Constants.GRAVITY
    hero.y = hero.y + hero.vy

    platform_under, platform_over = collision_platform_y(platforms, hero)

    hero.vx = 0
    if keyboard.space:
        if platform_under:
            hero.vy = Constants.JUMP_FORCE
            play_sound('sfx_jump')

    if keyboard.left:
        hero.vx = -Constants.X_SPEED 

    if keyboard.right:
        hero.vx = Constants.X_SPEED

    hero.x = hero.x + hero.vx

    platform_left, platform_right = collision_platform_x(platforms, hero)

    for obstacle in obstacles:
        if hero.colliderect(obstacle):
            hero.pos = Constants.HERO_START_POSITION
            play_sound('sfx_hurt')
            hero_lives = hero_lives - 1
            break
        
    for enemy in enemy_list:
        if hero.colliderect(enemy):
            hero.pos = Constants.HERO_START_POSITION
            play_sound('sfx_hurt')
            hero_lives = hero_lives - 1
            break
        
    if hero.left < 0:
        hero.left = 0
    
    if hero.right > Constants.WIDTH:
        hero.right = Constants.WIDTH

    if hero.colliderect(goal_flag):
        hero.pos = Constants.HERO_START_POSITION
        play_sound('sfx_coin')

pgzrun.go()
