from const import Constants

class Enemy:
    def create_enemy(enemy, enemy_tile_left, enemy_tile_botton, enemy_vx, enemy_list):
        enemy.bottom = enemy_tile_botton * Constants.TILE_SIZE
        enemy.left = enemy_tile_left * Constants.TILE_SIZE
        enemy.frame = 0
        enemy.vx = enemy_vx
        enemy.start_left = enemy.left
        enemy_list.append(enemy)
        return len(enemy_list) - 1

    def enemy_walk(enemy, min, max):
        enemy.x = enemy.x + enemy.vx
        if enemy.left < min or enemy.right > max:
            enemy.vx = - enemy.vx
    
