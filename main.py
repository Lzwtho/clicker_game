import arcade
import random
import time
import math

WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Clicker Game with Moving Target (I used Arcade)"

CIRCLE_RAD = 30
INITIAL_SPEED = 3.0 # pixels per frame, is FLOAT
GAME_DURATION = 30.0 # seconds not ms

BLUE = arcade.color.BLUE # create color here as easier access throughout code
WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK


class MovingTargetGame(arcade.Window):

    def __init__(self):
        # necessary, else errors, cuz arcade
        super().__init__(WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # DO NOT REMOVE
        self.score = 0
        self.start_time = 0.0
        self.game_over = False # bool, yes or no means True or False

        # circle vars
        self.circle_x = 0.0
        self.circle_y = 0.0
        self.circle_spedx = 0.0
        self.circle_speed_y = 0.0
        self.circle_radius = 30
        arcade.set_background_color(arcade.color.WHITE) # also #ffffff

    def setup(self):
        # setup, also used for reset
        self.score = 0
        self.game_over = False
        self.start_time = time.time() # gets start time, SECONDS, not ms

        # creates circle x & y (random, but in screen)
        self.circle_x = random.uniform(self.circle_radius, WIDTH - self.circle_radius)
        self.circle_y = random.uniform(self.circle_radius, SCREEN_HEIGHT - self.circle_radius)
        self.circle_spedx = INITIAL_SPEED #global var, look at top of file to change
        self.circle_speed_y = INITIAL_SPEED

    def on_draw(self):
        self.clear() # clears screen, else trails :(

        if self.game_over:
            arcade.draw_text( # vertical param declaration, cuz long line
            "Game Over!",
            WIDTH / 2,
            SCREEN_HEIGHT / 2 + 30,
            BLACK,
            font_size=50,
            anchor_x="center"
            )
            arcade.draw_text(
                f"Your Score: {self.score}",
                WIDTH / 2,
                SCREEN_HEIGHT / 2 - 20,
                BLACK,
                font_size=36,
                anchor_x="center"
            )
        else:
            arcade.draw_circle_filled( # draws circle using cur x & y
            self.circle_x,
            self.circle_y,
            self.circle_radius,
            BLUE
            )

        # Calculate remaining time, else too easy
        elapsed_time = time.time() - self.start_time
        remaining_time = max(GAME_DURATION - elapsed_time, 0)

        # show score
        arcade.draw_text(
            f"Score: {self.score}",
            10,
            SCREEN_HEIGHT - 30,
            BLACK,
            font_size=20 )

        # draw timer IN SECONDS
        arcade.draw_text(
        f"Time Left: {int(remaining_time)}s",
        650, # screen width - 150 px
        SCREEN_HEIGHT - 30,
        BLACK,
        font_size=20
        )

    def on_update(self, delta_time: float):
        screen_width = WIDTH
        if self.game_over:
            return

        # checks params for game over
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= GAME_DURATION:
            self.game_over = True
            arcade.schedule(self.quit, 3.0) # ncessary, else updates forever
            return # EXITS!!! DO NOT REMOVE, elsr func continues
        self.circle_x += self.circle_spedx
        self.circle_y += self.circle_speed_y

        if self.circle_x < CIRCLE_RAD:
            self.circle_x = CIRCLE_RAD
            self.circle_spedx *= -1
        elif self.circle_x > screen_width - CIRCLE_RAD:
            self.circle_x = screen_width - CIRCLE_RAD
            self.circle_spedx *= -1

        if self.circle_y < self.circle_radius:
                self.circle_y = self.circle_radius
                self.circle_speed_y *= -1
        elif self.circle_y > SCREEN_HEIGHT - self.circle_radius:
            self.circle_y = SCREEN_HEIGHT - self.circle_radius
            self.circle_speed_y *= -1

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.game_over:
            return

        """
        # d in dx mean,s difference, 
        dx = x - self.circle_x
        dy = y - self.circle_y
        distance_squared = dx * dx + dy * dy # pythag, dunno why, but ok 
        if distance_squared <= self.circle_radius * self.circle_radius:
            self.score += 1

        """


        # checks if click is in curcle, more CPU tho :( cuz external lib 
        distance = math.dist((x, y), (self.circle_x, self.circle_y)) # calc distance, 
        if distance <= self.circle_radius: 
                self.score += 1 # icnrements score

        cirlce_speed_x = self.circle_spedx

        if cirlce_speed_x < 0:
            self.circle_spedx -= 0.5
        else:
            self.circle_spedx += 0.5
        if self.circle_speed_y < 0:
            self.circle_speed_y -= 0.5
        else:
            self.circle_speed_y += 0.5



# Main Execution Block
def main():
    game = MovingTargetGame()
    game.setup()
    arcade.run() # starts game

if __name__ == "__main__":
    main()
