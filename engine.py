import pyxel
from typing import Optional, List, Callable

GRAVITY = 0.5
TERMINAL_VELOCITY = 8
PLAYER_SPEED = 4


class Physics:
    def __init__(self):
        self.dy = 0
        self.is_grounded = False
        self.is_falling = True

    def ground(self):
        self.dy = 0
        self.is_grounded = True
        self.is_falling = False

    def fall(self, is_colliding=False):
        if self.is_grounded and not self.is_falling:
            self.ground()

        if self.dy >= GRAVITY:
            self.is_grounded = False

        if not is_colliding or not self.is_grounded:
            self.is_falling = True
            self.dy += GRAVITY
            if self.dy > TERMINAL_VELOCITY:
                self.dy = TERMINAL_VELOCITY


class BoxWithCollision:
    def __init__(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        col: int,
        filled=False,
        phys=False,
        keys_move_x_pos: List[int] = [],
        keys_move_x_neg: List[int] = [],
        keys_jump: List[int] = [],
    ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col
        self.filled = filled
        self.phys = Physics() if phys else None
        self.keys_move_x_pos = keys_move_x_pos
        self.keys_move_x_neg = keys_move_x_neg
        self.keys_jump = keys_jump

    def is_colliding_top(self, box):
        if (
            (box.y + box.h >= self.y and box.y <= self.y)
            and box.phys
            and (
                (self.x <= box.x + box.w and self.x + self.w >= box.x + box.w)
                or (self.x <= box.x and self.x + self.w >= box.x)
            )
        ):
            print("COLLIDE")
            if box.phys.dy > 0:
                # knockback
                box.phys.ground()
                box.y = self.y - box.h - GRAVITY
            return True
        return False

    def fall(self, collider: Callable[[any], bool]):
        if self.phys:
            # call the collider to see if the object can fall
            self.phys.fall(collider(self))
            self.y += self.phys.dy
            # call the collider a second time for knockback
            collider(self)

    def inputs(self):
        for key in self.keys_move_x_pos:
            # move x positive
            if pyxel.btn(key):
                self.x += PLAYER_SPEED
                break

        for key in self.keys_move_x_neg:
            # move x negative
            if pyxel.btn(key):
                self.x -= PLAYER_SPEED
                break

        for key in self.keys_jump:
            # jump
            if pyxel.btnp(key) and self.phys and self.phys.is_grounded:
                self.phys.is_grounded = False
                self.phys.dy = -10
                break

    def draw(self):
        if self.filled:
            pyxel.rect(self.x, self.y, self.w, self.h, self.col)
        else:
            pyxel.rectb(self.x, self.y, self.w, self.h, self.col)
