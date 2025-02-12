import pygame
import menu
import game

pygame.init()

def main():
    while True:
        choice = menu.show_menu()
        if choice == "play":
            game.run_game()
        elif choice == "quit":
            pygame.quit()
            break

if __name__ == "__main__":
    main()
