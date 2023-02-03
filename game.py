import pyxel
from engine import *

SKY_COLOR = 6
PLAYER_COLOR = 8
FLOOR_COLOR = 4


class App:
    def __init__(self):
        pyxel.init(400, 300, title="Platformer", quit_key=pyxel.KEY_Q)
        self.floors = [
            Box(0, pyxel.height - 20, pyxel.width, 20, FLOOR_COLOR, filled=True),
            Box(50, pyxel.height - 100, 40, 20, FLOOR_COLOR, filled=True),
        ]
        self.player = Player(
            20,
            20,
            20,
            20,
            PLAYER_COLOR,
            filled=True,
            keys_move_x_pos=[pyxel.KEY_D, pyxel.KEY_RIGHT],
            keys_move_x_neg=[pyxel.KEY_A, pyxel.KEY_LEFT],
            keys_jump=[pyxel.KEY_W, pyxel.KEY_SPACE, pyxel.KEY_UP],
        )
        pyxel.run(self.update, self.draw)

    def update(self):
        for floor in self.floors:
            self.player.fall(floor.is_colliding_top)
        self.player.inputs()
        pyxel.camera(self.player.x - 50, 0)

    def draw(self):
        pyxel.cls(SKY_COLOR)

        for floor in self.floors:
            floor.draw()
        self.player.draw()


App()
