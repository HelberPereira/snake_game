import pygame
import sys
import random


# MENU PRINCIPAL
def main_menu():
    pygame.init()
    pygame.mixer.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game Menu")
    pygame.mixer.music.load("MenuMusic.mp3")
    pygame.mixer.music.play(-1)
    background = pygame.image.load("MenuSnake.png")
    background = pygame.transform.scale(background, (width, height))
    font = pygame.font.Font(None, 40)

    button_width_st, button_height_st = 200, 30
    button_width_sc, button_height_sc = 105, 30
    button_width_ex, button_height_ex = 75, 30
    hover_color = (0, 140, 0, 100)

    start_button = pygame.Rect((width // 2 - button_width_st // 2, 300), (button_width_st, button_height_st))
    score_button = pygame.Rect((width // 2 - button_width_sc // 2, 350), (button_width_sc, button_height_sc))
    exit_button = pygame.Rect((width // 2 - button_width_ex // 2, 400), (button_width_ex, button_height_ex))

    running = True
    while running:
        screen.blit(background, (0, 0))

        draw_button(screen, "INICIAR JOGO", start_button, hover_color, font)
        draw_button(screen, "SCORE", score_button, hover_color, font)
        draw_button(screen, "SAIR", exit_button, hover_color, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    snake_game()
                elif score_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    show_scores(screen)
                elif exit_button.collidepoint(event.pos):
                    running = False

    pygame.quit()
    sys.exit()


# MOSTRAR PONTUAÇÃO
def show_scores(screen):
    font = pygame.font.Font(None, 40)
    back_button = pygame.Rect(300, 500, 210, 30)

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_button(screen, "Voltar ao Menu", back_button, (140, 0, 0), font)

        y_pos = 100
        for player, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
            score_text = font.render(f"{player}: {score}", True, (255, 255, 255))
            screen.blit(score_text, (300, y_pos))
            y_pos += 50

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return "menu"


# JOGO
def snake_game():
    font = pygame.font.Font(None, 35)
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    point_sound = pygame.mixer.Sound("PointSong.mp3")
    pygame.mixer.music.load("MusicGame.mp3")
    pygame.mixer.music.play(-1)

    green = (0, 255, 0)
    red = (255, 0, 0)
    black = (0, 0, 0)

    snake_pos = [[100, 50], [90, 50], [80, 50]]
    snake_direction = 'RIGHT'
    change_to = snake_direction

    food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
    food_spawn = True

    score = 0
    speed = 15

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    change_to = 'RIGHT'

        snake_direction = change_to

        if snake_direction == 'UP':
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] - 10])
        elif snake_direction == 'DOWN':
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] + 10])
        elif snake_direction == 'LEFT':
            snake_pos.insert(0, [snake_pos[0][0] - 10, snake_pos[0][1]])
        elif snake_direction == 'RIGHT':
            snake_pos.insert(0, [snake_pos[0][0] + 10, snake_pos[0][1]])

        if snake_pos[0] == food_pos:
            score += 10
            food_spawn = False
            point_sound.play()
        else:
            snake_pos.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
        food_spawn = True

        screen.fill(black)
        for pos in snake_pos:
            pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if snake_pos[0][0] < 0 or snake_pos[0][0] > width or snake_pos[0][1] < 0 or snake_pos[0][1] > height:
            result = game_over_screen(screen, score)
            if result == "retry":
                snake_game()
                if isinstance(result, tuple) and result[0] == "save":
                    save_score(screen, result[1])
            else:
                main_menu()
            return

        for block in snake_pos[1:]:
            if snake_pos[0] == block:
                result = game_over_screen(screen, score)
                if result == "retry":
                    snake_game()
                    if isinstance(result, tuple) and result[0] == "save":
                        save_score(screen, result[1])
                    snake_game()
                else:
                    main_menu()
                return
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.update()
        clock.tick(speed)


# BOTOES
def draw_button(screen, text, rect, hover_color, font):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect, border_radius=25)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


# TELA DE GAMEOVER
def game_over_screen(screen, score):
    pygame.mixer.music.stop()
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 40)

    retry_button = pygame.Rect(275, 250, 250, 30)
    menu_button = pygame.Rect(295, 320, 210, 30)
    save_button = pygame.Rect(280, 380, 250, 30)

    running = True
    while running:
        screen.fill((0, 0, 0))
        game_over_text = font.render("Você perdeu!", True, (255, 0, 0))
        screen.blit(game_over_text, (285, 150))

        draw_button(screen, "Tentar Novamente", retry_button, (0, 140, 0), button_font)
        draw_button(screen, "Voltar ao Menu", menu_button, (140, 0, 0), button_font)
        draw_button(screen, "Salvar Pontuação", save_button, (0, 0, 140), button_font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    return "retry"
                elif menu_button.collidepoint(event.pos):
                    return "menu"
                elif save_button.collidepoint(event.pos):
                    save_score(screen, score)


# SALVAR PONTUAÇÃO
def save_score(screen, score):
    name = ''
    font = pygame.font.Font(None, 50)
    input_box = pygame.Rect(300, 250, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0, 0, 0))
        prompt_text = font.render("Digite seu nome e pressione a tecla enter:", True, (255, 255, 255))
        screen.blit(prompt_text, (50, 200))
        txt_surface = font.render(name, True, (255, 255, 255))
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if len(name) > 0:
                            scores[name] = score
                            running = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 4:
                        name += event.unicode
        clock.tick(30)
    main_menu()


scores = {}
if __name__ == "__main__":
    main_menu()
