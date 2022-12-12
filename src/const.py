import ursina

class Globals:
    out_of_map = -100000
    score_pos = (-0.85, 0.45)
    leader_pos = (-0.5, 0.45)
    game_over_pos = (-0.7, 0.1)
    fullscreen_size = (1920, 1080)
    text_duration = 1/10
    camera_rotation_x = -57
    color_window = (0.6, 0.3, 0.6, 1)
    color_ambient = (0.75, 0.75, 0.75, 1)
    light_direction = (1, 1, 1)
    color_direct_light = (1, 1, 1, 1)

class Objects:
    apple_color = ursina.color.red
    apple_scale = 0.007
    apple_rotation = (90, 90, 0)
    bonus_score_color = ursina.color.gold
    bonus_score_scale = 0.003
    bonus_speed_color = (1, 1, 1, 0.8)
    bonus_speed_scale = (0.7, 0.7, 0.7)
    snake_color = (0, 1, 0, 0.8)
    wall_color = ursina.color.dark_gray
    wall_scale = (1, 1, 1)