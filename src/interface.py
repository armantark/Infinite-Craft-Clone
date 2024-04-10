import pygame

class ElementPanel:
    def __init__(self, screen, elements, font, panel_width=200, panel_color=(240, 240, 240)):
        self.screen = screen
        self.elements = elements
        self.font = font
        self.panel_width = panel_width
        self.panel_color = panel_color
        self.panel_rect = pygame.Rect(screen.get_width() - self.panel_width, 0, self.panel_width, screen.get_height())
        self.scroll_y = 0  # Initial scroll position
        self.element_height = 30  # Assuming a fixed height for each element
        self.scrollbar_width = 20  # Width of the scrollbar
        self.dragging_scrollbar = False
        self.scrollbar_rect = pygame.Rect(screen.get_width() - self.scrollbar_width, 0, self.scrollbar_width, screen.get_height())

    def render(self):
        # Draw the panel
        pygame.draw.rect(self.screen, self.panel_color, self.panel_rect)

        # Calculate the total height of the elements
        self.total_height = len(self.elements) * self.element_height

        # List elements in the panel based on the current scroll position
        for i, element in enumerate(self.elements):
            # Calculate the y position of the element, adjusted for scrolling
            y_pos = 10 + i * self.element_height - self.scroll_y

            # Check if the element is within the visible area of the panel
            if 0 <= y_pos < self.screen.get_height():
                text_surface = self.font.render(element.text, True, (0, 0, 0))
                self.screen.blit(text_surface, (self.panel_rect.x + 10, y_pos))

        # Only draw the scrollbar if the total height of elements exceeds the panel height
        if self.total_height > self.panel_rect.height:
            # Draw scrollbar track
            pygame.draw.rect(self.screen, (200, 200, 200), self.scrollbar_rect)

            # Calculate scrollbar handle size and position based on the scrollable content size
            handle_height = max(self.panel_rect.height * self.panel_rect.height / self.total_height, 20)  # Minimum handle size
            handle_y = self.scroll_y * (self.panel_rect.height - handle_height) / (self.total_height - self.panel_rect.height)
            handle_rect = pygame.Rect(self.scrollbar_rect.x, self.scrollbar_rect.y + handle_y, self.scrollbar_width, handle_height)

            # Draw scrollbar handle
            pygame.draw.rect(self.screen, (150, 150, 150), handle_rect)
                
    def handle_event(self, event):
        # Check for mouse wheel event
        if event.type == pygame.MOUSEWHEEL:
            # Only handle the mouse wheel event if the total height of elements exceeds the panel height
            if self.total_height > self.panel_rect.height:
                # Adjust the scroll position based on the wheel direction
                self.scroll_y -= event.y * 10  # Scroll speed factor
                # Prevent scrolling beyond the content
                self.scroll_y = max(0, min(self.scroll_y, self.total_height - self.panel_rect.height))
                return True  # Indicate that the mouse wheel event has been handled for scrolling
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.scrollbar_rect.collidepoint(event.pos):
                self.dragging_scrollbar = True
                self.scroll_drag_pos_y = event.pos[1]
                return True  # Indicate that the scrollbar is being interacted with

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_scrollbar:
                self.dragging_scrollbar = False
                return True  # Indicate that the scrollbar was being interacted with

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_scrollbar:
                # Calculate the new scroll position based on mouse movement
                delta_y = event.pos[1] - self.scroll_drag_pos_y
                self.scroll_drag_pos_y = event.pos[1]
                scrollable_height = len(self.elements) * self.element_height - self.panel_rect.height
                handle_height = max(self.panel_rect.height * self.panel_rect.height / (len(self.elements) * self.element_height), 20)
                self.scroll_y += delta_y * (scrollable_height / (self.panel_rect.height - handle_height))
                self.scroll_y = max(0, min(self.scroll_y, scrollable_height))
                # Clamp the scroll_y value to prevent it from going out of bounds
                max_scroll = max(0, self.total_height - self.panel_rect.height)
                self.scroll_y = max(0, min(self.scroll_y, max_scroll))
                return True  # Indicate that the scrollbar is being interacted with

        return False  # No scrollbar interaction occurred

    def check_click(self, position):
        # Only check clicks within the panel bounds
        if self.panel_rect.collidepoint(position):
            # Adjust the y position of the click based on the current scroll position
            adjusted_y = position[1]

            # Determine the index of the first element displayed at the current scroll position
            start_index = self.scroll_y // self.element_height

            # Iterate through the elements that could be displayed in the panel
            for i in range(start_index, min(start_index + self.panel_rect.height // self.element_height + 1, len(self.elements))):
                element = self.elements[i]
                # Calculate the rect for each element based on its index and the scroll position
                element_rect = pygame.Rect(self.panel_rect.x + 10, 10 + i * self.element_height - self.scroll_y, self.panel_width - 20, self.element_height)
                # Check if the adjusted click position collides with the element rect
                if element_rect.collidepoint((position[0], adjusted_y)):
                    return element
        return None
    
    def add_element(self, new_element):
        self.elements.append(new_element)
    
class Button:
    def __init__(self, screen, text, position, font, color=(0, 0, 0), bgcolor=(200, 200, 200), padding=(10, 5)):
        self.screen = screen
        self.text = text
        self.position = position
        self.font = font
        self.color = color
        self.bgcolor = bgcolor
        self.padding = padding
        self.rect = None

    def render(self):
        text_surface = self.font.render(self.text, True, self.color)
        self.rect = text_surface.get_rect(topleft=self.position)

        # Inflate the rect to add padding
        self.rect.inflate_ip(self.padding[0] * 2, self.padding[1] * 2)

        # Draw the button
        pygame.draw.rect(self.screen, self.bgcolor, self.rect)
        self.screen.blit(text_surface, (self.rect.x + self.padding[0], self.rect.y + self.padding[1]))

    def check_click(self, position):
        return self.rect.collidepoint(position) if self.rect else False