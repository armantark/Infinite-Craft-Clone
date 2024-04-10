import pygame

class DraggableElement:
    def __init__(self, text, position, font, color=(0, 0, 0), bgcolor=(255, 255, 255)):
        self.text = text
        self.position = position
        self.font = font
        self.color = color
        self.bgcolor = bgcolor
        self.rect = None
        self.dragging = False
        self.mouse_offset_x = 0
        self.mouse_offset_y = 0
        self.z_order = 0
        self.processing = False
        self.rect = pygame.Rect(position[0], position[1], 0, 0)  # Initialize with a default rect
        self.bounding_box = self.rect.inflate(20, 20)  # Inflate by an arbitrary amount for initial bounding box

    def handle_event(self, event, elements):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.bounding_box.collidepoint(event.pos):
                # Start dragging and update z_order only if this element is not already being dragged
                if not self.dragging:
                    self.dragging = True
                    self.mouse_offset_x = self.bounding_box.x - event.pos[0]
                    self.mouse_offset_y = self.bounding_box.y - event.pos[1]
                    current_max_z_order = max((e.z_order for e in elements), default=-1)
                    self.z_order = current_max_z_order + 1

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Update the position of the element while dragging
                self.position = (event.pos[0] + self.mouse_offset_x, event.pos[1] + self.mouse_offset_y)

        return False  # Default return value if no dragging state change occurred

    def update(self):
        # Update the element's state if necessary
        pass

    def render(self, screen):
        render_color = (200, 200, 200) if self.processing else self.color
        render_bgcolor = (220, 220, 220) if self.processing else self.bgcolor

        text_surface = self.font.render(self.text, True, render_color, render_bgcolor)
        
        # Render the text
        text_surface = self.font.render(self.text, True, self.color, self.bgcolor)
        self.rect = text_surface.get_rect(topleft=self.position)

        # Inflate the rectangle to make the bounding box bigger
        margin = 10  # Margin size
        self.bounding_box = self.rect.inflate(margin * 2, margin * 2)

        # Draw the background box
        screen.fill(self.bgcolor, self.bounding_box)
        # Draw the text
        screen.blit(text_surface, self.rect)
        # Draw the bounding box
        pygame.draw.rect(screen, self.color, self.bounding_box, 1)  # 1 is the thickness of the box # 2 is the thickness of the box