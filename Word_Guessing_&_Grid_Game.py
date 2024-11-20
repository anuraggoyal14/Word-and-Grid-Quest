import random
import os
from collections import Counter

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def hangman_game():
    def choose_difficulty():
        print()
        print("Choose difficulty level:")
        print("1. Easy (10 chances)")
        print("2. Medium (7 chances)")
        print("3. Hard (5 chances)")
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == '1':
            return 10
        elif choice == '2':
            return 7
        elif choice == '3':
            return 5
        else:
            print("Invalid choice. Defaulting to Medium.")
            return 7

    someWords = '''apple banana mango strawberry 
    orange grape pineapple apricot lemon coconut watermelon 
    cherry papaya berry peach lychee muskmelon'''
    someWords = someWords.split()
    word = random.choice(someWords)

    print('Guess the word! HINT: Word is a name of a fruit')

    guessed_word = ['_'] * len(word)
    print(' '.join(guessed_word))

    chances = choose_difficulty()
    letterGuessed = ''
    correct = 0

    while chances > 0 and correct < len(word):
        guess = input('Enter a letter to guess: ').lower()
        
        if not guess.isalpha() or len(guess) != 1:
            print('Enter only a single letter.')
            continue
        
        if guess in letterGuessed:
            print('You have already guessed that letter.')
            continue
        
        letterGuessed += guess

        if guess in word:
            for idx, char in enumerate(word):
                if char == guess:
                    guessed_word[idx] = guess
                    correct += 1
        else:
            chances -= 1

        print(' '.join(guessed_word))
        print(f'Chances left: {chances}')

    if correct == len(word):
        print(f'Congratulations, You won! The word is: {word}')
    else:
        print(f'You lost! The word was {word}')

def grid_game():
    def create_player(x, y):
        return [x, y, 100, 0]  

    def create_enemy(width, height):
        return [random.randint(0, width - 1), random.randint(0, height - 1),10]  

    def create_treasure(width, height):
        return [random.randint(0, width - 1), random.randint(0, height - 1)]  

    def is_valid_move(x, y, width, height):
        return 0 <= x < width and 0 <= y < height

    def move_entity(entity, dx, dy):
        entity[0] += dx
        entity[1] += dy

    def display_game(player, enemies, treasures, width, height, destination):
        clear_screen()
        for y in range(height):
            for x in range(width):
                if x == player[0] and y == player[1]:
                    print('P', end=' ')  
                elif any(enemy[0] == x and enemy[1] == y for enemy in enemies):
                    print('E', end=' ') 
                elif any(treasure[0] == x and treasure[1] == y for treasure in treasures):
                    print('T', end=' ')  
                elif x == destination[0] and y == destination[1]:
                    print('D', end=' ')  
                else:
                    print('.', end=' ')  
            print()

        print(f"\nHealth: {player[2]} | Treasures: {player[3]}\n")

    def update_enemies(enemies, width, height):
        for enemy in enemies:
            if random.choice([True, False]):
                dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                new_x = enemy[0] + dx
                new_y = enemy[1] + dy
                if is_valid_move(new_x, new_y, width, height):
                    enemy[0], enemy[1] = new_x, new_y

    player = create_player(0, 0)
    width, height = 5, 5
    enemies = [create_enemy(width, height) for _ in range(3)]
    treasures = [create_treasure(width, height) for _ in range(3)]
    destination = (4, 4)

    while True:
        display_game(player, enemies, treasures, width, height, destination)
        print("Here P: Player  E: Enemy  T: Treasures  D: Destination")
        print(" ")
        direction = input("Enter direction (up/down/left/right): ").strip().lower()
        while direction not in ["up", "down", "left", "right"]:
            print("Invalid direction. Please enter up, down, left, or right.")
            direction = input("Enter direction (up/down/left/right): ").strip().lower()
        
        dx, dy = 0, 0
        if direction == "up":
            dy = -1
        elif direction == "down":
            dy = 1
        elif direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1

        new_x = player[0] + dx
        new_y = player[1] + dy

        if is_valid_move(new_x, new_y, width, height):
            move_entity(player, dx, dy)
            update_enemies(enemies, width, height)

            if any(player[0] == enemy[0] and player[1] == enemy[1] for enemy in enemies):
                player[2] -= 10
                print("You were attacked by an enemy! Health decreased by 10.")

            if any(player[0] == treasure[0] and player[1] == treasure[1] for treasure in treasures):
                player[3] += 1
                treasures = [treasure for treasure in treasures if treasure != [player[0], player[1]]]
                print(f"You found a treasure! Treasures collected: {player[3]}")

            if (player[0], player[1]) == destination:
                print("Congratulations! You reached the destination.")
                break

            if player[2] <= 0:
                print("Game over! Your health reached zero.")
                break
        else:
            print("Invalid move. Try again.")

def main_menu():
    while True:
        print("\nWelcome to the Playstation!")
        print("1. Word-Guessing Game")
        print("2. Grid-based Game")
        print("3. Exit")
        
        choice = input("Enter the number of the game you want to play: ").strip()
        
        while choice not in ['1', '2', '3']: 
            print("Invalid choice. Please enter a valid option.")
            choice = input("Enter the number of the game you want to play: ").strip()

        if choice == '1':
            hangman_game()
        elif choice == '2':
            grid_game()
        elif choice == '3':
            print('Exiting the program...')
            break

if __name__ == "__main__":
    main_menu()
