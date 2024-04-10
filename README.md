# Infinite Craft Clone - README

## Overview
Infinite Craft Clone is a game inspired by [Neal's Infinite Craft](https://neal.fun/infinite-craft/) where players can combine basic elements to create new ones. The game features a draggable interface for elements, a scrollable panel for selecting elements, and an AI service that generates new elements based on combinations.

## Environment Setup

To run Infinite Craft Clone, you need to have Python and Pygame installed on your system. Follow these steps to set up your environment:

1. **Install Python**: Download and install Python from the official website: [python.org](https://www.python.org/downloads/).

2. **Install Pygame**: Pygame is a set of Python modules designed for writing video games. Install it using pip (Python's package installer):

   ```sh
   pip install pygame
   ```

3. **Clone the Repository**: Clone the source code to your local machine:

   ```sh
   git clone https://github.com/armantark/infinite-craft-clone.git
   cd infinite-craft-clone
   ```

4. **Run Setup Script**: To install all the required additional Python packages, execute the `setup.sh` script using bash:

   ```sh
   bash setup.sh
   ```

5. **Run the Game**: Execute the main script to start the game:

   ```sh
   python src/main.py
   ```

## Gameplay

- Click and drag elements from the right panel onto the canvas.
- Combine two elements by dragging them on top of each other.
- If the combination is valid, a new element will be generated and added to the panel.
- Use the scrollbar to navigate through the list of elements if it exceeds the panel's height.
- Click the "Clear" button to remove all elements from the canvas.

## Contributing

Contributions to Infinite Craft Clone are welcome. Please follow the standard fork-and-pull request workflow:

1. Fork the repository.
2. Make your changes in a new branch.
3. Submit a pull request with a clear description of your changes.

## License

Infinite Craft Clone is released under the [MIT License](LICENSE).