import pygame
import sys
from States.menu import Menu
from States.game import Game
from States.option import Option

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Guessing Game")

STATE_MENU = "menu"
STATE_GAME = "game"
STATE_OPTION = "option"

def main():
    clock = pygame.time.Clock()
    state = STATE_MENU

    menu = Menu(WIDTH, HEIGHT)
    game = Game(WIDTH, HEIGHT)   # has Visualization inside
    option = Option(WIDTH, HEIGHT)  # manages num_points

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- MENU STATE ---
            if state == STATE_MENU:
                new_state = menu.handle_event(event)
                if new_state == "game":
                    # use whatever Option currently stores
                    game.visualization.reset(option.num_points)
                    state = STATE_GAME
                elif new_state == "option":
                    state = STATE_OPTION

            # --- GAME STATE ---
            elif state == STATE_GAME:
                game.handle_event(event)

            # --- OPTION STATE ---
            elif state == STATE_OPTION:
                new_state = option.handle_event(event)
                if new_state == "menu":
                    state = STATE_MENU
                elif new_state == "game":
                    game.visualization.reset(option.num_points)
                    state = STATE_GAME

        # --- DRAW LOOP ---
        if state == STATE_MENU:
            menu.draw(screen)
        elif state == STATE_GAME:
            game.draw(screen)
        elif state == STATE_OPTION:
            option.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()