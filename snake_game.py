import random
import sys
import time
import os
import msvcrt  # Windows-specific for non-blocking input

class SnakeGame:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.snake = [(width//2, height//2)]
        self.direction = (1, 0)  # Moving right initially
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        
    def generate_food(self):
        while True:
            food = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            if food not in self.snake:
                return food
    
    def move(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check boundaries
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()
    
    def change_direction(self, new_direction):
        # Prevent reversing into itself
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * (self.width + 2))
        for y in range(self.height):
            print("|", end="")
            for x in range(self.width):
                if (x, y) == self.snake[0]:
                    print("O", end="")  # Snake head
                elif (x, y) in self.snake:
                    print("o", end="")  # Snake body
                elif (x, y) == self.food:
                    print("*", end="")  # Food
                else:
                    print(" ", end="")
            print("|")
        print("=" * (self.width + 2))
        print(f"Score: {self.score}")
        print("Controls: WASD to move, Q to quit")
    
    def get_input(self):
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 'w':
                self.change_direction((0, -1))
            elif key == 's':
                self.change_direction((0, 1))
            elif key == 'a':
                self.change_direction((-1, 0))
            elif key == 'd':
                self.change_direction((1, 0))
            elif key == 'q':
                self.game_over = True
    
    def play(self):
        print("Snake Game Starting...")
        print("Use WASD keys to control the snake")
        print("Press Q to quit at any time")
        print("Press any key to start...")
        msvcrt.getch()
        
        while not self.game_over:
            self.draw()
            self.get_input()
            self.move()
            time.sleep(0.15)  # Game speed
        
        # Game over screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 30)
        print("         GAME OVER!")
        print(f"       Final Score: {self.score}")
        print("=" * 30)
        print("Thanks for playing!")

def main():
    game = SnakeGame()
    try:
        game.play()
    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
