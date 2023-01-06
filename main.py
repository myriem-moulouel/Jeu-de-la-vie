import pygame
from Ressources.variables import *
from Ressources.game import Game

pygame.init()

pygame.display.set_caption("Jeu De La Vie")

Win = pygame.display.set_mode((Width, Height))
input_rect = pygame.Rect((Width//2)-75, (Height//2)-16, 140, 32)
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()


def main():
    run = True
    FPS = 60
    n_rows_entered = False
    n_cols_entered = False
    created = False
    started = False
    new_Game = None
    n_rows = ''
    n_cols = ''
    

    while run:
        Win.fill(White)

        if not n_rows_entered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        n_rows = n_rows[:-1]

                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        n_rows_entered = True

                    else:
                        if event.unicode >= '0' and event.unicode <= '9':
                            n_rows += event.unicode
                    
            pygame.draw.rect(Win, (0,250,0), input_rect, 2)
            text = font.render(n_rows, True, (Black))
            text2 = font.render("rows : ", True, (Black))
            Win.blit(text2, (input_rect.x, input_rect.y - (font.size("n_rows")[1]+7)))
            Win.blit(text, (input_rect.x + 5, input_rect.y + 5))

        elif not n_cols_entered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        n_cols = n_cols[:-1]

                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        n_cols_entered = True

                    else:
                        if event.unicode >= '0' and event.unicode <= '9':
                            n_cols += event.unicode
            pygame.draw.rect(Win, (0,250,0), input_rect, 2)
            text = font.render(n_cols, True, (Black))
            text2 = font.render("cols : ", True, (Black))
            Win.blit(text2, (input_rect.x, input_rect.y - (font.size("n_cols")[1]+7)))
            Win.blit(text, (input_rect.x + 5, input_rect.y + 5))
        else:
            if not created:
                new_Game = Game(int(n_rows), int(n_cols))

                created = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()

                if started:
                    continue

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = pos[1]//new_Game.row, pos[0]//new_Game.col

                    if new_Game.grid_cells[row][col] == 0:
                        new_Game.grid_cells[row][col] = 1

                if pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    row, col = pos[1]//new_Game.row, pos[0]//new_Game.col

                    if new_Game.grid_cells[row][col] == 1:
                        new_Game.grid_cells[row][col] = 0

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        started = True

            
            new_Game.draw_grid()
        
        if new_Game and started:
            new_Game.update_grid_cells()
        pygame.display.update()
        clock.tick(FPS)

main()
