from ursina import *
from random import randrange
from ursina.shaders import basic_lighting_shader


class Apple(Entity):
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.rotation = (90, 90, 0)
        self.scale = 0.007
        self.model = "3d_objects\Apple.fbx"
        self.double_sided = True
        self.new_position()
        self.color = color.red
        self.shader = basic_lighting_shader

    def new_position(self):
        self.position = (randrange(self.MAP_SIZE) + 0.5,
                         randrange(self.MAP_SIZE) + 0.5, -0.5)


class BonusScore(Entity):
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.scale = 0.003
        self.model = "3d_objects\Apple.fbx"
        self.double_sided = True
        self.new_position()
        self.color = color.gold
        self.shader = basic_lighting_shader

    def new_position(self):
        self.position = (randrange(self.MAP_SIZE) + 0.5,
                         randrange(self.MAP_SIZE) + 0.5, -0.5)


class BonusSpeed(Entity):
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.model = 'cube'
        self.scale = (0.7, 0.7, 0.7)
        self.double_sided = True
        self.new_position()
        self.color = (1, 1, 1, 0.8)
        self.shader = basic_lighting_shader

    def new_position(self):
        self.position = (randrange(self.MAP_SIZE) + 0.5,
                         randrange(self.MAP_SIZE) + 0.5, -0.5)


class Wall(Entity):
    def __init__(self, MAP_SIZE, i, j, **kwargs):
        super().__init__(**kwargs)
        self.model = 'cube'
        self.MAP_SIZE = MAP_SIZE
        self.color = color.dark_gray
        self.scale = (1, 1, 1)
        self.position = (i + 0.5, j + 0.5, -0.5)
        self.shader = basic_lighting_shader


class Snake:
    def __init__(self, MAP_SIZE):
        self.MAP_SIZE = MAP_SIZE
        self.segment_length = 1
        self.position_length = self.segment_length + 1
        self.segment_positions = [
            Vec3(randrange(MAP_SIZE) + 0.5, randrange(MAP_SIZE) + 0.5, -0.5)]
        self.segment_entities = []
        self.create_segment(self.segment_positions[0])
        self.directions = {
            'a': Vec3(-1, 0, 0), 'd': Vec3(1, 0, 0), 'w': Vec3(0, 1, 0), 's': Vec3(0, -1, 0)}
        self.direction = Vec3(0, 0, 0)
        self.permissions = {'a': 1, 'd': 1, 'w': 1, 's': 1}
        self.taboo_movement = {'a': 'd', 'd': 'a', 'w': 's', 's': 'w'}
        self.speed = 30
        self.score = 0
        self.frame_counter = 0
        self.shader = basic_lighting_shader

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

    def create_segment(self, position):
        entity = Entity(position=position)
        Entity(model='sphere', color=(0, 1, 0, 0.8), position=position).add_script(
            SmoothFollow(speed=5, target=entity, offset=(0, 0, 0)))
        self.segment_entities.insert(0, entity)

    def run(self):
        self.frame_counter += 1
        if not self.frame_counter % self.speed:
            self.control()
            self.segment_positions.append(
                self.segment_positions[-1] + self.direction)
            self.segment_positions = self.segment_positions[-self.segment_length:]
            for segment, segment_position in zip(self.segment_entities, self.segment_positions):
                segment.position = segment_position

    def control(self):
        for key in 'wasd':
            if held_keys[key] and self.permissions[key]:
                self.direction = self.directions[key]
                self.permissions = dict.fromkeys(self.permissions, 1)
                self.permissions[self.taboo_movement[key]] = 0
                break
