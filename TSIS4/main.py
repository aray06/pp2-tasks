import pygame, json, db, os
from config import *
from game import GameEngine

class App:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)
        self.settings = self.load_settings()
        db.init_db()
        self.username = ""
        self.state = "MENU"
        
        # Пути к звукам в папке assets
        try:
            self.eat_sound = pygame.mixer.Sound("assets/eat.wav")
            self.fail_sound = pygame.mixer.Sound("assets/fail.wav")
        except:
            self.eat_sound = self.fail_sound = None

    def load_settings(self):
        try:
            with open("settings.json", "r") as f: return json.load(f)
        except: return {"snake_color": [46, 204, 113], "grid": True, "sound": True}

    def save_settings(self):
        with open("settings.json", "w") as f: json.dump(self.settings, f)

    def draw_text(self, text, x, y, color=COLOR_TEXT):
        img = self.font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def menu_screen(self):
        self.screen.fill(COLOR_BG)
        self.draw_text(f"NAME: {self.username}", 150, 150, COLOR_FOOD_GOLD)
        self.draw_text("ENTER: Start | L: Leaders | S: Settings", 80, 250)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "QUIT"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and self.username: return "GAME"
                elif e.key == pygame.K_l: return "LEADERS"
                elif e.key == pygame.K_s: return "SETTINGS"
                elif e.key == pygame.K_BACKSPACE: self.username = self.username[:-1]
                else: self.username += e.unicode
        return "MENU"

    def settings_screen(self):
        self.screen.fill(COLOR_BG)
        grid_st = "ON" if self.settings["grid"] else "OFF"
        snd_st = "ON" if self.settings["sound"] else "OFF"
        self.draw_text(f"G: Grid [{grid_st}] | H: Sound [{snd_st}]", 120, 150)
        self.draw_text("Press M to Menu", 200, 300)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "QUIT"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_g: self.settings["grid"] = not self.settings["grid"]
                if e.key == pygame.K_h: self.settings["sound"] = not self.settings["sound"]
                if e.key == pygame.K_m: 
                    self.save_settings()
                    return "MENU"
        return "SETTINGS"

    def game_loop(self):
        game = GameEngine(self.settings)
        p_id = db.get_or_create_player(self.username)
        pb = db.get_personal_best(p_id)
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: return "QUIT"
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT and game.direction[0] == 0: game.direction = (-20, 0)
                    elif e.key == pygame.K_RIGHT and game.direction[0] == 0: game.direction = (20, 0)
                    elif e.key == pygame.K_UP and game.direction[1] == 0: game.direction = (0, -20)
                    elif e.key == pygame.K_DOWN and game.direction[1] == 0: game.direction = (0, 20)

            status = game.update()
            if status == "eat" and self.settings["sound"] and self.eat_sound: self.eat_sound.play()
            if status is False:
                if self.settings["sound"] and self.fail_sound: self.fail_sound.play()
                db.save_game(p_id, game.score, game.level)
                self.last_score, self.last_level = game.score, game.level
                return "GAMEOVER"

            self.screen.fill(COLOR_BG)
            if self.settings["grid"]:
                for x in range(0, WIDTH, SNAKE_BLOCK): pygame.draw.line(self.screen, (30,30,30), (x,40), (x,HEIGHT))
            
            # Отрисовка
            pygame.draw.circle(self.screen, COLOR_FOOD_BASE if game.food_type=='reg' else COLOR_FOOD_GOLD, (game.food[0]+10, game.food[1]+10), 8)
            pygame.draw.rect(self.screen, COLOR_POISON, [game.poison[0], game.poison[1], 20, 20])
            for o in game.obstacles: pygame.draw.rect(self.screen, COLOR_OBSTACLE, [o[0], o[1], 20, 20])
            for p in game.snake: pygame.draw.rect(self.screen, self.settings["snake_color"], [p[0], p[1], 20, 20])
            
            self.draw_text(f"Score: {game.score} | Best: {pb}", 10, 10, COLOR_FOOD_GOLD)
            pygame.display.flip()
            self.clock.tick(game.get_speed())

    def leaderboard_screen(self):
        self.screen.fill(COLOR_BG)
        self.draw_text("TOP 10", 250, 50, COLOR_FOOD_GOLD)
        try:
            data = db.get_top_10()
            for i, row in enumerate(data):
                self.draw_text(f"{i+1}. {row[0]} - {row[1]}", 150, 100 + i*25)
        except: pass
        self.draw_text("M: Menu", 250, 400)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_m: return "MENU"
            if e.type == pygame.QUIT: return "QUIT"
        return "LEADERS"

    def game_over_screen(self):
        self.screen.fill((60,0,0))
        self.draw_text("GAME OVER", 230, 150, (255,0,0))
        self.draw_text(f"Score: {self.last_score}", 250, 200)
        self.draw_text("SPACE: Restart | M: Menu", 160, 300)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "QUIT"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE: return "GAME"
                if e.key == pygame.K_m: return "MENU"
        return "GAMEOVER"

    def run(self):
        while self.state != "QUIT":
            if self.state == "MENU": self.state = self.menu_screen()
            elif self.state == "GAME": self.state = self.game_loop()
            elif self.state == "LEADERS": self.state = self.leaderboard_screen()
            elif self.state == "SETTINGS": self.state = self.settings_screen()
            elif self.state == "GAMEOVER": self.state = self.game_over_screen()
        pygame.quit()

if __name__ == "__main__":
    App().run()