from src.const import Globals
import src.game_objects as game_objects
import src.maps as maps
import src.sounds as sounds
import ursina
from ursina.shaders import lit_with_shadows_shader

class Game(ursina.Ursina):
    def __init__(self):
        super().__init__()
        ursina.window.color = Globals.color_window
        ursina.window.borderless = False
        ursina.window.fullscreen_size = Globals.fullscreen_size
        ursina.window.fullscreen = True
        ursina.AmbientLight(color=Globals.color_ambient)
        ursina.DirectionalLight(color=Globals.color_direct_light, direction=Globals.light_direction)
        self.max = 0
        ursina.camera.shader = lit_with_shadows_shader
        self.map_nom = 0
        self.map = maps.Maps()
        self.MAP_SIZE = len(self.map.walls[self.map_nom])
        self.snake = game_objects.Snake(self.MAP_SIZE)
        self.new_game()

    def create_map(self, MAP_SIZE):
        '''Создает карту размера MAP_SIZE'''
        sounds.Ambient().vhs.play()
        ursina.Entity(model='quad', scale=MAP_SIZE, position=(
            MAP_SIZE // 2, MAP_SIZE // 2, 0), texture="sky\\DeathScreen.png")
        ursina.Entity(model=ursina.Grid(MAP_SIZE, MAP_SIZE), scale=MAP_SIZE,
                      position=(MAP_SIZE // 2, MAP_SIZE // 2, -0.01), color=ursina.color.green)

    def new_game(self):
        '''Новая игра - меняет расположение камеры под размер карты, обновляет объекты'''
        ursina.camera.position = (self.MAP_SIZE // 2, -1 *
                                  self.MAP_SIZE - 1, -1 * self.MAP_SIZE)
        ursina.camera.rotation_x = Globals.camera_rotation_x
        with open("src\\Scores.txt", "a+") as f:
            f.write(str(self.snake.score) + '\n')
            f.close()
        with open("src\\Scores.txt", "r+") as f:
            self.max = max(list(map(int, f.readlines())))
            f.close()
        ursina.scene.clear()
        self.create_map(self.MAP_SIZE)
        self.apple = game_objects.Apple(self.MAP_SIZE)
        self.snake = game_objects.Snake(self.MAP_SIZE)
        self.bonus_score = game_objects.BonusScore(self.MAP_SIZE)
        self.bonus_speed = game_objects.BonusSpeed(self.MAP_SIZE)
        for i in range(self.MAP_SIZE):
            for j in range(self.MAP_SIZE):
                if self.map.walls[self.map_nom][i][j] == '1':
                    self.wall = game_objects.Wall(self.MAP_SIZE, i, j)

    def check_apple_eaten(self):
        '''Проверка на то, съедено ли в данный момент яблоко'''
        if self.snake.segment_positions[-1] == self.apple.position:
            self.snake.add_segment()
            self.apple.new_position()
            sounds.Biting().apple_bite.play()
            if ursina.random.randrange(10) == 1:
                ursina.destroy(self.bonus_score, delay=0)
                self.bonus_score = game_objects.BonusScore(self.MAP_SIZE)
            if ursina.random.randrange(10) == 1:
                ursina.destroy(self.bonus_speed, delay=0)
                self.bonus_speed = game_objects.BonusSpeed(self.MAP_SIZE)

    def check_bonus_score_eaten(self):
        '''Проверка на то, съедено ли в данный момент яблоко-бонус'''
        if self.snake.segment_positions[-1] == self.bonus_score.position:
            self.snake.bonus_score()
            sounds.Biting().bonus_bite.play()
            self.bonus_score.position = (Globals.out_of_map, Globals.out_of_map, 0)

    def check_bonus_speed_eaten(self):
        '''Проверка на то, съеден ли в данный момент бонус скорости'''
        if self.snake.segment_positions[-1] == self.bonus_speed.position:
            self.snake.bonus_speed()
            sounds.Bonus_speed().glass.play()
            self.bonus_speed.position = (Globals.out_of_map, Globals.out_of_map, 0)

    def check_apple_not_in_wall(self):
        '''Исключает генерацию яблока в стене'''
        if self.map.walls[self.map_nom][int(self.apple.position[0] - 0.5)][int(self.apple.position[1] - 0.5)] == '1':
            self.apple.new_position()

    def check_game_over(self):
        '''Умерла ли змейка в данный момент? Если да, то новая игра'''
        snake = self.snake.segment_positions
        if 0 < snake[-1][0] < self.MAP_SIZE and 0 < snake[-1][1] < self.MAP_SIZE and len(snake) == len(set(snake)) and self.map.walls[self.map_nom][int(snake[-1][0] - 0.5)][int(snake[-1][1] - 0.5)] == '0':
            return
        sounds.GameOver().broken.play()
        ursina.print_on_screen('GAME OVER', position=Globals.game_over_pos,
                        scale=10, duration=1)
        self.snake.direction = ursina.Vec3(0, 0, 0)
        self.snake.permissions = dict.fromkeys(self.snake.permissions, 0)
        ursina.invoke(self.new_game, delay=1)

    def map_change(self):
        '''Обновление карты при нажатии на соответсвующие клавиши'''
        if ursina.held_keys['1']:
            self.map_nom = 0
            self.MAP_SIZE = len(self.map.walls[self.map_nom])
            self.new_game()
        elif ursina.held_keys['2']:
            self.map_nom = 1
            self.MAP_SIZE = len(self.map.walls[self.map_nom])
            self.new_game()
        elif ursina.held_keys['3']:
            self.map_nom = 2
            self.MAP_SIZE = len(self.map.walls[self.map_nom])
            self.new_game()
        elif ursina.held_keys['4']:
            self.map_nom = 3
            self.MAP_SIZE = len(self.map.walls[self.map_nom])
            self.new_game()
        elif ursina.held_keys['5']:
            self.map_nom = 4
            self.MAP_SIZE = len(self.map.walls[self.map_nom])
            self.new_game()

    def update(self):
        '''Обновление, проверяются вышеперечисленные условия и текст на экране'''
        self.apple.rotation_x += ursina.time.dt + 2
        self.bonus_score.rotation_x += ursina.time.dt + 2
        self.bonus_speed.rotation_x += ursina.time.dt + 2
        ursina.print_on_screen(f'Score: {self.snake.score}',
                               position=Globals.score_pos, scale=3, duration=Globals.text_duration)
        ursina.print_on_screen(f'Leader: {self.max}',
                               position=Globals.leader_pos, scale=3, duration=Globals.text_duration)
        self.check_apple_eaten()
        self.check_apple_not_in_wall()
        self.check_game_over()
        self.check_bonus_score_eaten()
        self.check_bonus_speed_eaten()
        self.map_change()
        self.snake.run()
