import pyxel
from typing import Optional, List, Callable
from enum import Enum

GRAVITY = 0.5
TERMINAL_VELOCITY = 6
PLAYER_SPEED = 6


class PhysicsStates(Enum):
    IDLE = 0
    FALLING = 1
    JUMPING = 2
    RUNNING_LEFT = 3
    RUNNING_RIGHT = 4


class PhysicsStateMachine:
    def __init__(self):
        self.state = PhysicsStates.FALLING


class Physics:
    def __init__(self, state_machine: PhysicsStateMachine):
        self.dy = 0
        self.is_grounded = False
        self.is_falling = True
        self.state_machine = state_machine

    def ground(self):
        self.dy = 0
        self.is_grounded = True
        self.is_falling = False

    def fall(self, is_colliding=False):
        if self.is_grounded and not self.is_falling:
            self.ground()

        if self.dy >= GRAVITY:
            self.is_grounded = False
            self.state_machine.state = PhysicsStates.FALLING
        elif self.dy < 0:
            self.state_machine.state = PhysicsStates.JUMPING
        else:
            self.state_machine.state = PhysicsStates.IDLE

        if not is_colliding or not self.is_grounded:
            self.is_falling = True
            self.dy += GRAVITY
            if self.dy > TERMINAL_VELOCITY:
                self.dy = TERMINAL_VELOCITY


class Box:
    def __init__(
        self, x: float, y: float, w: float, h: float, col: int, filled=False, phys=False
    ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col
        self.filled = filled
        self.state_machine = PhysicsStateMachine() if phys else None
        self.phys = Physics(self.state_machine) if phys else None

    def is_colliding_top(self, box):
        if (
            (box.y + box.h >= self.y and box.y <= self.y)
            and box.phys
            and (
                (self.x <= box.x + box.w and self.x + self.w >= box.x + box.w)
                or (self.x <= box.x and self.x + self.w >= box.x)
            )
        ):
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

    def draw(self):
        if self.state_machine:
            print(self.state_machine.state)
        if self.filled:
            pyxel.rect(self.x, self.y, self.w, self.h, self.col)
        else:
            pyxel.rectb(self.x, self.y, self.w, self.h, self.col)


class Player(Box):
    def __init__(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        col: int,
        filled=False,
        keys_move_x_pos: List[int] = [],
        keys_move_x_neg: List[int] = [],
        keys_jump: List[int] = [],
    ):
        super().__init__(x, y, w, h, col, filled, True)
        self.keys_move_x_pos = keys_move_x_pos
        self.keys_move_x_neg = keys_move_x_neg
        self.keys_jump = keys_jump

    def inputs(self):
        x = self.x
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

        if self.state_machine.state == PhysicsStates.IDLE:
            if self.x > x:
                self.state_machine.state = PhysicsStates.RUNNING_RIGHT
            elif self.x < x:
                self.state_machine.state = PhysicsStates.RUNNING_LEFT
