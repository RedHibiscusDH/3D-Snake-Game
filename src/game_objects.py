from src.const import Objects
import ursina
from random import randrange
from ursina.shaders import basic_lighting_shader


class Apple(ursina.Entity):
    '''Яблоко'''
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.rotation = Objects.apple_rotation
        self.scale = Objects.apple_scale
        self.model = "3d_objects\\Apple.fbx"
        self.double_sided = True
        self.new_position()
        self.color = Objects.apple_color
        self.shader = basic_lighting_shader

    def new_position(self):
        self.position = (randrange(self.MAP_SIZE) + 0.5,
                         randrange(self.MAP_SIZE) + 0.5, -0.5)


class BonusScore(ursina.Entity):
    '''Яблоко-бонус'''
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.scale = Objects.bonus_score_scale
        self.model = "3d_objects\\Apple.fbx"
        self.double_sided = True
        self.new_position()
        self.color = Objects.bonus_score_color
        self.shader = basic_lighting_shader

    def new_position(self):
        self.position = (randrange(self.MAP_SIZE) + 0.5,
                         randrange(self.MAP_SIZE) + 0.5, -0.5)


class BonusSpeed(ursina.Entity):
    '''Бонус скорости'''
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.model = 'cube'
        self.scale = Objects.bonus_speed_scale
        self.double_sided = True
        self.new_position()
        self.color = Objects.bonus_speed_color
        self.shader = basic_lighting_shader

    def new_position(self):
        self.position = (randrange(self.MAP_SIZE) + 0.5,
                         randrange(self.MAP_SIZE) + 0.5, -0.5)


class Wall(ursina.Entity):
    '''Стена'''
    def __init__(self, MAP_SIZE, i, j, **kwargs):
        super().__init__(**kwargs)
        self.model = 'cube'
        self.MAP_SIZE = MAP_SIZE
        self.color = Objects.wall_color
        self.scale = Objects.wall_scale
        self.position = (i + 0.5, j + 0.5, -0.5)
        self.shader = basic_lighting_shader


class Snake:
    '''Змейка'''
    def __init__(self, MAP_SIZE):
        self.MAP_SIZE = MAP_SIZE
        self.segment_length = 1
        self.position_length = self.segment_length + 1
        self.segment_positions = [
            ursina.Vec3(randrange(MAP_SIZE) + 0.5, randrange(MAP_SIZE) + 0.5, -0.5)]
        self.segment_entities = []
        self.create_segment(self.segment_positions[0])
        self.directions = {
            'a': ursina.Vec3(-1, 0, 0), 'd': ursina.Vec3(1, 0, 0), 'w': ursina.Vec3(0, 1, 0), 's': ursina.Vec3(0, -1, 0)}
        self.direction = ursina.Vec3(0, 0, 0)
        self.permissions = {'a': 1, 'd': 1, 'w': 1, 's': 1} #Разрешенные клавишы
        self.taboo_movement = {'a': 'd', 'd': 'a', 'w': 's', 's': 'w'}
        self.speed = 30
        self.score = 0
        self.frame_counter = 0
        self.shader = basic_lighting_shader

    '''Добавление сегмента'''
    def add_segment(self):
        self.segment_length += 1
        self.position_length += 1
        self.score += 1
        self.speed = max(self.speed - 1, 5)
        self.create_segment(self.segment_positions[0])

    def bonus_score(self):
        self.score += 3

    def bonus_speed(self):
        self.speed += 5

    '''Создание нового сегмента'''
    def create_segment(self, position):
        entity = ursina.Entity(position=position)
        ursina.Entity(model='sphere', color=Objects.snake_color, position=position).add_script(
            ursina.SmoothFollow(speed=5, target=entity, offset=(0, 0, 0)))
        self.segment_entities.insert(0, entity)

    '''Движение'''
    def run(self):
        self.frame_counter += 1
        if not self.frame_counter % self.speed:
            self.control()
            self.segment_positions.append(
                self.segment_positions[-1] + self.direction)
            self.segment_positions = self.segment_positions[-self.segment_length:]
            for segment, segment_position in zip(self.segment_entities, self.segment_positions):
                segment.position = segment_position

    '''Проверка нажатых клавиш'''
    def control(self):
        for key in 'wasd':
            if ursina.held_keys[key] and self.permissions[key]:
                self.direction = self.directions[key]
                self.permissions = dict.fromkeys(self.permissions, 1)
                self.permissions[self.taboo_movement[key]] = 0
                break
