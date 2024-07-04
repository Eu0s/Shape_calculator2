import pygame
import sys
import math


# Initialize Pygame
pygame.init()


# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shape Calculator')


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
grey = (200, 200, 200)
light_grey = (230, 230, 230)
blue = (0, 0, 255)


# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)


# Shapes
shapes = ['Circle', 'Rectangle', 'Square', 'Triangle', 'Right-Angle Triangle']
current_shape = shapes[0]


# User inputs
radius = 0
width = 0
height = 0
angle = 0
area = 0
circumference = 0
angles = (0, 0)  # To store the remaining angles for the right-angle triangle


# Input state
input_active = {'radius': False, 'width': False, 'height': False, 'angle': False}
input_text = {'radius': '', 'width': '', 'height': '', 'angle': ''}
input_rects = {
 'radius': pygame.Rect(200, 200, 140, 32),
 'width': pygame.Rect(200, 250, 140, 32),
 'height': pygame.Rect(200, 300, 140, 32),
 'angle': pygame.Rect(200, 350, 140, 32)
}


calculate_button_rect = pygame.Rect(screen_width - 200, screen_height - 100, 140, 40)


# Boundary box dimensions
boundary_box_width = 400
boundary_box_height = 300
boundary_box_x = screen_width - boundary_box_width - 50
boundary_box_y = (screen_height - boundary_box_height) // 2


def draw_text(text, x, y, font=font, color=black):
 text_surface = font.render(text, True, color)
 screen.blit(text_surface, (x, y))


def calculate_area(shape, w, h):
 if shape == 'Circle':
     return math.pi * (w ** 2)
 elif shape == 'Rectangle':
     return w * h
 elif shape == 'Square':
     return w ** 2
 elif shape == 'Triangle' or shape == 'Right-Angle Triangle':
     return 0.5 * w * h


def calculate_circumference(shape, w, h):
 if shape == 'Circle':
     return 2 * math.pi * w
 elif shape == 'Rectangle':
     return 2 * (w + h)
 elif shape == 'Square':
     return 4 * w
 elif shape == 'Triangle':
     return w + 2 * math.sqrt((w / 2) ** 2 + h ** 2)
 elif shape == 'Right-Angle Triangle':
     return w + h + math.sqrt(w ** 2 + h ** 2)


def calculate_right_angle_triangle_angles(a, b):
 angle_a = math.degrees(math.atan(a / b))
 angle_b = 90 - angle_a
 return round(angle_a, 2), round(angle_b, 2)


def draw_shape(shape, w, h):
 # Center coordinates for drawing shapes
 center_x = boundary_box_x + boundary_box_width // 2
 center_y = boundary_box_y + boundary_box_height // 2


 # Limiting shape dimensions to fit within the boundary box
 if shape == 'Circle':
     radius = min(w, h, min(boundary_box_width, boundary_box_height) // 2)
     pygame.draw.circle(screen, red, (center_x, center_y), radius)
 elif shape == 'Rectangle':
     width = min(w, boundary_box_width)
     height = min(h, boundary_box_height)
     pygame.draw.rect(screen, red, pygame.Rect(center_x - width // 2, center_y - height // 2, width, height))
 elif shape == 'Square':
     size = min(w, h, min(boundary_box_width, boundary_box_height))
     pygame.draw.rect(screen, red, pygame.Rect(center_x - size // 2, center_y - size // 2, size, size))
 elif shape == 'Triangle':
     points = [
         (center_x, boundary_box_y),
         (center_x - boundary_box_width // 2, boundary_box_y + boundary_box_height),
         (center_x + boundary_box_width // 2, boundary_box_y + boundary_box_height)
     ]
     pygame.draw.polygon(screen, red, points)
 elif shape == 'Right-Angle Triangle':
     points = [
         (center_x, center_y - h // 2),
         (center_x - w // 2, center_y + h // 2),
         (center_x + w // 2, center_y + h // 2)
     ]
     pygame.draw.polygon(screen, red, points)


def draw_radio_button(text, x, y, selected):
 pygame.draw.circle(screen, black, (x, y), 10, 2)
 if selected:
     pygame.draw.circle(screen, black, (x, y), 5)
 draw_text(text, x + 20, y - 10, small_font)


# Main loop
running = True
while running:
 screen.fill(white)


 for event in pygame.event.get():
     if event.type == pygame.QUIT:
         running = False
     elif event.type == pygame.KEYDOWN:
         if any(input_active.values()):
             if event.key == pygame.K_BACKSPACE:
                 for key in input_active:
                     if input_active[key]:
                         input_text[key] = input_text[key][:-1]
             else:
                 for key in input_active:
                     if input_active[key]:
                         input_text[key] += event.unicode
     elif event.type == pygame.MOUSEBUTTONDOWN:
         for key in input_rects:
             if input_rects[key].collidepoint(event.pos):
                 input_active = {k: False for k in input_active}
                 input_active[key] = True
                 break
         else:
             input_active = {k: False for k in input_active}


         if calculate_button_rect.collidepoint(event.pos):
             try:
                 if current_shape == 'Circle':
                     radius = int(input_text['radius'])
                     width = height = radius
                 else:
                     width = int(input_text['width'])
                     height = int(input_text['height'])
                     if current_shape == 'Square':
                         height = width
                     radius = 0


                 area = round(calculate_area(current_shape, width if current_shape != 'Circle' else radius, height), 2)
                 circumference = round(calculate_circumference(current_shape, width if current_shape != 'Circle' else radius, height), 2)


                 if current_shape == 'Right-Angle Triangle':
                     angle = float(input_text['angle']) if input_text['angle'] else 0
                     angles = calculate_right_angle_triangle_angles(width, height)
             except ValueError:
                 pass


         for i, shape in enumerate(shapes):
             if pygame.Rect(50 + i * 150, 130, 20, 20).collidepoint(event.pos):
                 current_shape = shape
                 input_active = {'radius': False, 'width': False, 'height': False, 'angle': False}
                 input_text = {'radius': '', 'width': '', 'height': '', 'angle': ''}
                 radius = width = height = area = circumference = angle = 0
                 angles = (0, 0)
                 break


 draw_text("Shape Calculator", 300, 30)
 draw_text("Select Shape:", 50, 80)
 for i, shape in enumerate(shapes):
     draw_radio_button(shape, 60 + i * 150, 130, shape == current_shape)


 if current_shape == 'Circle':
     draw_text('Insert radius:', 38, 205)
     pygame.draw.rect(screen, light_grey if input_active['radius'] else grey, input_rects['radius'])
     pygame.draw.rect(screen, black, input_rects['radius'], 2)  # Add black border
     draw_text(input_text['radius'], 205, 205)
 else:
     draw_text('Insert Width:', 45, 255)
     pygame.draw.rect(screen, light_grey if input_active['width'] else grey, input_rects['width'])
     pygame.draw.rect(screen, black, input_rects['width'], 2)  # Add black border
     draw_text(input_text['width'], 205, 255)
     draw_text('Insert Height:', 38, 305)
     pygame.draw.rect(screen, light_grey if input_active['height'] else grey, input_rects['height'])
     pygame.draw.rect(screen, black, input_rects['height'], 2)  # Add black border
     draw_text(input_text['height'], 205, 305)
     if current_shape == 'Right-Angle Triangle':
         draw_text('Insert Angle:', 46, 350)
         pygame.draw.rect(screen, light_grey if input_active['angle'] else grey, input_rects['angle'])
         pygame.draw.rect(screen, black, input_rects['angle'], 2)  # Add black border
         draw_text(input_text['angle'], 205, 355)


 # Draw the boundary box
 pygame.draw.rect(screen, black, (boundary_box_x, boundary_box_y, boundary_box_width, boundary_box_height), 2)


 pygame.draw.rect(screen, black, calculate_button_rect)
 draw_text('Calculate', screen_width - 180, screen_height - 90, font=small_font, color=white)


 draw_text(f'Area: {area}', 50, 400)
 draw_text(f'Circumference: {circumference}', 50, 450)
 if current_shape == 'Right-Angle Triangle' and width > 0 and height > 0:
     draw_text(f'Angles: {angles[0]}°, {angles[1]}°', 50, 500)


 if (current_shape == 'Circle' and radius > 0) or (current_shape != 'Circle' and width > 0 and height > 0):
     draw_shape(current_shape, width if current_shape != 'Circle' else radius, height if current_shape not in ['Circle', 'Square'] else width)


 pygame.display.flip()


pygame.quit()
sys.exit()
