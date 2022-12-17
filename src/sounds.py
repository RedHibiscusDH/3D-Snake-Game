import ursina

class Biting():
    def __init__(self):
        self.apple_bite = ursina.Audio('sound\\bite1.mp3', loop=False, autoplay=False)
        self.bonus_bite = ursina.Audio('sound\\bite2.mp3', loop=False, autoplay=False)

class Bonus_speed():
    def __init__(self):
        self.glass = ursina.Audio('sound\\glass.mp3', loop=False, autoplay=False)

class GameOver():
    def __init__(self):
        self.broken = ursina.Audio('sound\\broken.mp3', loop=False, autoplay=False)

class Ambient():
    def __init__(self):
        self.vhs = ursina.Audio('sound\\vhs-hum.mp3', loop=True, autoplay=False)
