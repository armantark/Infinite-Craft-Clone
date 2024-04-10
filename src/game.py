import pygame
from elements import DraggableElement
from interface import ElementPanel, Button
from ai_service import OpenAIService
import random
import threading

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.elements = []
        self.font = pygame.font.Font(None, 36)
        self.init_elements()
        self.element_panel = ElementPanel(screen, self.base_elements, self.font)
        self.clear_button = Button(screen, "Clear", (10, 10), self.font)
        self.ai_service = OpenAIService()

    def init_elements(self):
        # Initialize the four basic elements for the panel
        self.base_elements = [DraggableElement("Fire", (0, 0), self.font),
                              DraggableElement("Water", (0, 0), self.font),
                              DraggableElement("Earth", (0, 0), self.font),
                              DraggableElement("Air", (0, 0), self.font)]

    def combine_elements(self, element1, element2):
        # Set processing state to True to gray out the elements
        element1.processing = True
        element2.processing = True
        self.render()  # Render immediately to show the grayed-out elements
        pygame.display.flip()

        # Generate the new word in a background thread
        def generate_and_create():
            new_word = self.ai_service.generate_word(element1.text, element2.text)
            # Create a new element with the generated word
            new_element_position = ((element1.position[0] + element2.position[0]) // 2,
                                    (element1.position[1] + element2.position[1]) // 2)
            new_element = DraggableElement(new_word, new_element_position, self.font)
            new_element.z_order = max((e.z_order for e in self.elements), default=0) + 1

            # Update the game state in the main thread
            def update_elements():
                self.elements.remove(element1)
                self.elements.remove(element2)
                self.elements.append(new_element)
                # Add the new element to the panel
                self.element_panel.add_element(new_element)

            # Schedule the update_elements function to be called in the main thread
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'code': 'update_elements', 'func': update_elements}))

        # Start the background task
        threading.Thread(target=generate_and_create).start()

    def handle_event(self, event):
        # Handle events for the element panel (scrolling, etc.)
        if self.element_panel.handle_event(event):
            return  # Skip element selection/creation if the scrollbar is being interacted with
        
        # Handle events for draggable elements
        for element in sorted(self.elements, key=lambda e: e.z_order, reverse=True):
            # Pass the event to the topmost element first
            was_dragging = element.handle_event(event, self.elements)
            if event.type == pygame.MOUSEBUTTONDOWN and element.dragging:
                # If the element starts being dragged, bring it to the front
                element.z_order = max(e.z_order for e in self.elements) + 1
                break  # Break to ensure no other elements start dragging

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the panel was clicked
            clicked_element = self.element_panel.check_click(event.pos)
            if clicked_element:
                # Create a copy of the clicked element on the canvas at a random position
                canvas_width = self.screen.get_width() - self.element_panel.panel_width
                canvas_height = self.screen.get_height()
                random_pos = (random.randint(0, canvas_width - 100), random.randint(0, canvas_height - 100))
                new_element = DraggableElement(clicked_element.text, random_pos, self.font)
                new_element.z_order = max((e.z_order for e in self.elements), default=0) + 1
                self.elements.append(new_element)
            if self.clear_button.check_click(event.pos):
                self.elements.clear()  # Clear the canvas elements
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for element in self.elements[:]:
                if element.dragging:
                    # First, check for collision with other elements
                    collided_with_element = False
                    for other_element in self.elements:
                        if other_element != element and other_element.bounding_box.colliderect(element.bounding_box):
                            self.combine_elements(element, other_element)
                            collided_with_element = True
                            break  # Break after combining elements

                    # If there was no collision with other elements, check for panel collision
                    if not collided_with_element and self.element_panel.panel_rect.colliderect(element.bounding_box):
                        self.elements.remove(element)  # Remove the element if it's over the panel

                    # Now set dragging to False after handling collisions and potential deletion
                    element.dragging = False
                    break  # Break after handling the element that was dragging

        # Handle custom events to update game state
        if event.type == pygame.USEREVENT and event.code == 'update_elements':
            event.func()  # Call the function to update elements

    def update(self):
        # Update game state
        for element in self.elements:
            element.update()

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black

        # First, render the panel so it's underneath the elements
        self.element_panel.render()

        # Then, render the elements on top of the panel
        for element in sorted(self.elements, key=lambda e: e.z_order):
            element.render(self.screen)

        # Finally, render the clear button on top of everything
        self.clear_button.render()