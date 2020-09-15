# Copyright @ 2020 ABCOM Information Systems Pvt. Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.font.init()

FPS = 3
Width_window = 720
height_window = 600
size_cell = 30
assert height_window % size_cell == 0, "Window Height must be a multiple of Cell Size"
assert Width_window % size_cell == 0, "Window Width must be a multiple of Cell Size"
cell_width= int(Width_window / size_cell)
cell_height = int(height_window / size_cell)

#Colour Codes for usaing them in snake window
#			 R    G    B
WHITE    = (255, 255, 255)
BLACK    = (0,     0,   0)
GREEN    = (0,   255,   0)

RED      = (255,   0,   0)

DARKGREEN= (0,   155,   0)
DARKGRAY = (40,   40,  40)
YELLOW   = (255, 255,   0)

BGCOLOR = WHITE

#Control Keys
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 #Index of the snake's head
