from ursina import *
from game_objects import *
from maps import *


class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.color = (0.52, 0, 0.31, 1)
        window.borderless = False
        window.fullscreen_size = 1920, 1080
        window.fullscreen = True
        AmbientLight(color=(0.5, 0.5, 0.5, 1))
        DirectionalLight(color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))
        self.max = 0
        self.map_nom = 0
        self.map = Maps()
        self.MAP_SIZE = len(self.map.walls[self.map_nom])
        self.snake = Snake(self.MAP_SIZE)
        self.new_game()

    def create_map(self, MAP_SIZE):
        Entity(model='quad', scale=MAP_SIZE, position=(
            MAP_SIZE // 2, MAP_SIZE // 2, 0), texture="sky\DeathScreen.png")
        Entity(model=Grid(MAP_SIZE, MAP_SIZE), scale=MAP_SIZE,
               position=(MAP_SIZE // 2, MAP_SIZE // 2, -0.01), color=color.pink)

    def new_game(self):
        camera.position = (self.MAP_SIZE // 2, -1 *
                           self.MAP_SIZE - 1, -1 * self.MAP_SIZE)
        camera.rotation_x = -57
        with open("Scores.txt", "a+") as f:
            f.write(str(self.snake.score) + '\n')
            f.close()
        with open("Scores.txt", "r+") as f:
            self.max = max(list(map(int, f.readlines())))
            f.close()
        scene.clear()
        self.create_map(self.MAP_SIZE)
        self.apple = Apple(self.MAP_SIZE)
        self.snake = Snake(self.MAP_SIZE)
        self.bonus_score = BonusScore(self.MAP_SIZE)
        self.bonus_speed = BonusSpeed(self.MAP_SIZE)
        for i in range(self.MAP_SIZE):
            for j in range(self.MAP_SIZE):
                if self.map.walls[self.map_nom][i][j] == '1':
                    self.wall = Wall(self.MAP_SIZE, i, j)

    def check_apple_eaten(self):
        if self.snake.segment_positions[-1] == self.apple.position:
            self.snake.add_segment()
            self.apple.new_position()
            if random.randrange(10) == 1:
                destroy(self.bonus_score, delay=0)
                self.bonus_score = BonusScore(self.MAP_SIZE)
            if random.randrange(10) == 1:
                destroy(self.bonus_speed, delay=0)
                self.bonus_speed = BonusSpeed(self.MAP_SIZE)

    def check_bonus_score_eaten(self):
        if self.snake.segment_positions[-1] == self.bonus_score.position:
            self.snake.bonus_score()
            self.bonus_score.position = (-10000, -10000, 0)

    def check_bonus_speed_eaten(self):
        if self.snake.segment_positions[-1] == self.bonus_speed.position:
            self.snake.bonus_speed()
            self.bonus_speed.position = (-10000, -10000, 0)

    def check_apple_not_in_wall(self):
        if self.map.walls[self.map_nom][int(self.apple.position[0] - 0.5)][int(self.apple.position[1] - 0.5)] == '1':
            self.apple.new_position()

    def check_game_over(self):
        snake = self.snake.segment_positions
        if 0 < snake[-1][0] < self.MAP_SIZE and 0 < snake[-1][1] < self.MAP_SIZE and len(snake) == len(set(snake)) and self.map.walls[self.map_nom][int(snake[-1][0] - 0.5)][int(snake[-1][1] - 0.5)] == '0':
            return
        print_on_screen('GAME OVER', position=(-0.7, 0.1),
                        scale=10, duration=1)
        self.snake.direction = Vec3(0, 0, 0)
        self.snake.permissions = dict.fromkeys(self.snake.permissions, 0)
        invoke(self.new_game, delay=1)

    def update(self):
        self.apple.rotation_x += time.dt + 2
        self.bonus_score.rotation_x += time.dt + 2
        self.bonus_speed.rotation_x += time.dt + 2
        if held_keys['1']:
            self.map_nom = 0
            self.MAP_SIZE = len(self.map.walls[self.map_nom])
            self.new_game()
        elif held_keys['2']:
            self.map_nom = 1
            self.MAP_SIZE = len(self.map.walls[self.map_nom])
            self.new_game()
        elif held_keys['3']:
            self.map_nom = 2
            self.MAP_SIZE = len(self.map.walls[self.map_nom])
            self.new_game()
        elif held_keys['4']:
            self.map_nom = 3
            self.MAP_SIZE = len(self.map.walls[self.map_nom])
            self.new_game()
        elif held_keys['5']:
            self.map_nom = 4
            self.MAP_SIZE = len(self.map.walls[self.map_nom])
            self.new_game()
        print_on_screen(f'Score: {self.snake.score}',
                        position=(-0.85, 0.45), scale=3, duration=1/10)
        print_on_screen(f'Leader: {self.max}',
                        position=(-0.5, 0.45), scale=3, duration= 1/10)
        self.check_apple_eaten()
        self.check_apple_not_in_wall()
        self.check_game_over()
        self.check_bonus_score_eaten()
        self.check_bonus_speed_eaten()
        self.snake.run()


if __name__ == '__main__':
    game = Game()
    update = game.update
    game.run()
