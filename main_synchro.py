import pygame
import time
import threading
from Ressources.variables import *


pygame.init()

pygame.display.set_caption("Jeu De La Vie")

Win = pygame.display.set_mode((Width, Height))
input_rect = pygame.Rect((Width // 2) - 75, (Height // 2) - 16, 140, 32)
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()





class Game:

    # Initialisation du jeu
    def __init__(self, n_rows, n_cols, refresh_rate):
        self.display_surface = pygame.display.get_surface()
        self.w = self.display_surface.get_width()
        self.h = self.display_surface.get_height()
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.refresh_rate = refresh_rate

        self.row = self.create_cell(1)
        self.col = self.create_cell(0)

        self.grid_cells = self.create_grid()
        self.grid_neighbors = self.create_grid()

        self.stop_event = threading.Event()
        self.list_thread = [
            [
                threading.Thread(target=self.count_cells, args=(i, j))
                for j in range(self.n_cols)
            ] for i in range(self.n_rows)
        ]

        # +1 car on attends aussi la time barrier
        self.barrier = threading.Barrier((n_rows * n_cols))

    def quit(self):
        self.stop_event.set()
        self.barrier.abort()

    # Indexation des cellules de la grille
    def create_cell(self, cell_type):
        if cell_type:
            if self.n_rows % self.h != 0:
                return (self.h // self.n_rows) + 1
            else:
                return self.h // self.n_rows

        else:
            if self.n_cols % self.w != 0:
                return (self.w // self.n_cols) + 1
            else:
                return self.w // self.n_cols

    # Création de la grille (matrice de 0)
    def create_grid(self):
        return [[0 for _ in range(self.n_cols)] for _ in range(self.n_rows)]

    # Dessiner la grille
    def draw_grid(self):
        self.display_surface.fill(White)

        for row in range(self.n_rows):
            pygame.draw.line(self.display_surface, Black, (0, row * self.row),
                             (self.w, row * self.row))

        for col in range(self.n_cols):
            pygame.draw.line(self.display_surface, Black, (col * self.col, 0),
                             (col * self.col, self.h))

        for row in range(len(self.grid_cells)):
            for col in range(len(self.grid_cells[row])):
                if self.grid_cells[row][col]:
                    Rect = pygame.Rect(col * self.col, row * self.row,
                                       self.col, self.row)
                    pygame.draw.rect(self.display_surface, Black, Rect)

    # mettre à jour la grille du nombre de voisins
    def update_grid(self):
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                self.list_thread[r][c].start()

    def count_cells(self, r, c):
        while not self.stop_event.is_set():
            nei = 0
            for i in range(r - 1, r + 2):
                for j in range(c - 1, c + 2):
                    if ((i == r and j == c) or i < 0 or j < 0 or
                            i == len(self.grid_cells) or j == len(
                                self.grid_cells[0])):
                        continue
                    if self.grid_cells[i][j]:
                        nei += 1
            self.grid_neighbors[r][c] = nei
            try:
                self.barrier.wait()
            except threading.BrokenBarrierError:
                return

            if self.grid_cells[r][c]:
                if self.grid_neighbors[r][c] in [2, 3]:
                    self.grid_cells[r][c] = 1
                else:
                    self.grid_cells[r][c] = 0
            else:
                if self.grid_neighbors[r][c] == 3:
                    self.grid_cells[r][c] = 1
                else:
                    self.grid_cells[r][c] = 0
            if self.barrier.n_waiting == self.n_rows * self.n_cols-1:
                time.sleep(self.refresh_rate)
                self.draw_grid()

            try:
                self.barrier.wait()
            except threading.BrokenBarrierError:
                return









def main():
    run = True
    fps = 60
    n_rows_entered = False
    n_cols_entered = False
    created = False
    started = False
    started_thread = False
    new_Game = None
    n_rows = ''
    n_cols = ''

    while run:
        Win.fill(White)

        if not n_rows_entered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    if new_Game is not None:
                        new_Game.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        n_rows = n_rows[:-1]

                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        n_rows_entered = True

                    else:
                        if '0' <= event.unicode <= '9':
                            n_rows += event.unicode

            pygame.draw.rect(Win, (0, 250, 0), input_rect, 2)
            text = font.render(n_rows, True, Black)
            text2 = font.render("rows : ", True, Black)
            Win.blit(text2, (
            input_rect.x, input_rect.y - (font.size("n_rows")[1] + 7)))
            Win.blit(text, (input_rect.x + 5, input_rect.y + 5))

        elif not n_cols_entered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    if new_Game is not None:
                        new_Game.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        n_cols = n_cols[:-1]

                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        n_cols_entered = True

                    else:
                        if '0' <= event.unicode <= '9':
                            n_cols += event.unicode
            pygame.draw.rect(Win, (0, 250, 0), input_rect, 2)
            text = font.render(n_cols, True, Black)
            text2 = font.render("cols : ", True, Black)
            Win.blit(text2, (
            input_rect.x, input_rect.y - (font.size("n_cols")[1] + 7)))
            Win.blit(text, (input_rect.x + 5, input_rect.y + 5))
        else:
            if not created:
                new_Game = Game(int(n_rows), int(n_cols), REFRESH_RATE)

                created = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    if new_Game is not None:
                        new_Game.quit()

                if started:
                    continue

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = pos[1] // new_Game.row, pos[0] // new_Game.col

                    if new_Game.grid_cells[row][col] == 0:
                        new_Game.grid_cells[row][col] = 1

                if pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    row, col = pos[1] // new_Game.row, pos[0] // new_Game.col

                    if new_Game.grid_cells[row][col] == 1:
                        new_Game.grid_cells[row][col] = 0

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        started = True

            new_Game.draw_grid()

        if new_Game and started and not started_thread:
            print(
                f"la longueur de la list thread : "
                f"{len(new_Game.list_thread)} {len(new_Game.list_thread[0])}"
            )
            new_Game.update_grid()
            started_thread = True

        pygame.display.update()
        clock.tick(fps)


main()
