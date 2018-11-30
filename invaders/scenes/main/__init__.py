import cocos
from invaders.resources.resources import Resources
from invaders.input.joystick import JoyStick
from invaders.managers.enemy_attack_manager import EnemyAttackManager
from invaders.managers.player_attack_manager import PlayerAttackManager
from invaders.managers.sprite_manager import SpriteManager


class Main_Scene(cocos.scene.Scene):
    def __init__(self):
        super(Main_Scene, self).__init__()
        self.layer = Main_Layer()
        self.add(self.layer)


class Main_Layer(cocos.layer.Layer):
    def __init__(self):
        super(Main_Layer, self).__init__()
        self.width = self.anchor[0] * 2
        self.height = self.anchor[1] * 2
        self.joystick = JoyStick(self)

        self.resources = Resources()
        self.sprite_manager = SpriteManager(self.resources)
        self.enemy_attack_manager = EnemyAttackManager(self.sprite_manager)
        self.player_attack_manager = PlayerAttackManager(self.sprite_manager)

        self.invaders = self.sprite_manager.create_invaders(self)
        self.player = self.sprite_manager.create_player(self.width, self.height)
        self.add(self.player)
        self.schedule(self.loop)

    def loop(self, dt, *args, **kwargs):
        self.invaders.move_sprites(dt, self.player_attack_manager, self)
        self.enemy_attack_manager.update_attack(self, self.player, self.invaders)

    def on_joyaxis_motion(self, joystick, axis, value):
        if axis == "x":
            self.player.move(value)

    def on_joybutton_press(self, joystick, button):
        if button == 0 or button == 1:
            self.player_attack_manager.fire_player_missile(self, self.player)
