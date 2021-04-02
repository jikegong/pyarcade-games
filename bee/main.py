import arcade
from random import randint
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = ""
TILE_SCALING = 0.5
COIN_SCALING = 0.5
MOVEMENT_SPEED = 5
PLAYER_MOVEMENT_SPEED = 10
# 重力
GRAVITY = 0.2


class GameOver(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 1
        self.texture = arcade.load_texture("gameover.png")
        self.gameover = False
        self.to_center_x = 0

    def update(self):
        if self.gameover:
            self.center_x = self.to_center_x
        else:
            self.center_x = 10000


class FlyingSprite(arcade.Sprite):
    def update(self):
        super().update()
        if self.right < 0:
            self.remove_from_sprite_lists()


class FireSprite(arcade.Sprite):
    def update(self):
        super().update()
        if self.right > float(SCREEN_WIDTH):
            self.remove_from_sprite_lists()


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 1
        self.textures = []
        self.time = 0
        texture = arcade.load_texture("bee0.png")
        self.textures.append(texture)
        texture = arcade.load_texture("bee1.png")
        self.textures.append(texture)
        self.texture = texture

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
        if self.change_y > 0:
            self.time += 1
            if self.time % 10 == 0:
                self.texture = self.textures[0]
            if self.time % 20 == 0:
                self.texture = self.textures[1]


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        self.score = 0
        self.player_list = None
        self.coin_list = None
        self.wall_list = None
        self.bullet_list = None
        self.item_list = None
        self.enemies_list = None
        self.player_sprite = None
        self.all_sprites = arcade.SpriteList()
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        arcade.set_background_color(arcade.color.AMAZON)
        self.paused = False
        self.gameover = False

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.enemies_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.gameover_sprite = GameOver()
        self.gameover_sprite.center_x = self.width/2
        self.gameover_sprite.to_center_x = self.width/2
        self.gameover_sprite.center_y = self.height/2
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 300
        self.player_sprite.change_y = -5
        # self.player_sprite.velocity = (0, -5)
        self.player_list.append(self.player_sprite)
        self.all_sprites.append(self.player_sprite)
        arcade.schedule(self.add_enemy, 1.0)

    def add_enemy(self, delta_time: float):
        enemy = FlyingSprite("brick.png", 0.1)
        enemy.velocity = (-5, 0)
        enemy.left = randint(self.width, self.width + 80)
        enemy.top = randint(0, self.height)
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()
        arcade.draw_text(f"Score: {self.score}", 20, 20, arcade.color.WHITE, 30)

    def on_update(self, delta_time):
        self.gameover_sprite.update()
        if self.paused:
            return
        if self.gameover:
            return
        self.all_sprites.update()
        if self.player_sprite.collides_with_list(self.enemies_list):
            self.gameover = True
            self.gameover_sprite.gameover = True
            print('game over')

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.enemies_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.UP:
            if self.gameover:
                self.gameover = False
                self.gameover_sprite.gameover = False
                self.enemies_list = arcade.SpriteList()
            else:
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
                arcade.play_sound(self.jump_sound)

        # fire
        if key == arcade.key.SPACE:
            if self.gameover:
                pass
            else:
                fire = FlyingSprite("fire.png", 0.05)
                fire.velocity = (5, 0)
                fire.left = self.player_sprite.left+self.player_sprite.width
                fire.top = self.player_sprite.top-self.player_sprite.height/2
                self.bullet_list.append(fire)
                self.all_sprites.append(fire)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.UP:
            self.player_sprite.change_y = -5


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
