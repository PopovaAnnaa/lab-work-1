import pygame
import main_menu
import gameplay

pygame.init()

def main():
    while True:
        choice = main_menu.show_menu()
        if choice == "play":
            gameplay.run_game()
        elif choice == "quit":
            pygame.quit()
            break

if __name__ == "__main__":
    main()

