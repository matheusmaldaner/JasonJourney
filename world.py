from character import Character
from item import Item
import constants


class World:
    def __init__(self):
        self.level_length = None
        self.map_tiles = []
        self.overlay_tiles = []

        self.wall_tiles = []
        self.ladder_tile = None
        self.player = None
        self.all_items = []
        self.all_enemies = []
        self.all_npcs = []

    # "data" comes from the csv file, -1, 0, 1...
    # "tile_list" has images for the associated numbers in "data"
    def process_data(self, data, tile_list, item_list, mob_animations):
        self.level_length = len(data)

        # creates y and x counter in function definition
        for y, row in enumerate(data):
            for x, tile in enumerate(row):

                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                # 7 represents wall
                if tile == 7:
                    self.wall_tiles.append(tile_data)
                # 8 represents exit
                elif tile == 8:
                    self.ladder_tile = tile_data
                # 9 represents coins
                elif tile == 9:
                    coin = Item(image_x, image_y, 0, item_list[0], False)
                    self.all_items.append(coin)
                    # overrides coin tile with floor tile
                    tile_data[0] = tile_list[0]
                # 10 represents potions
                elif tile == 10:
                    # item_list[1] is a list of still images as of now
                    potion = Item(image_x, image_y, 1, item_list[1], False, 3)  # costs 3 coins
                    self.all_items.append(potion)
                    tile_data[0] = tile_list[0]
                # 11 represents the player
                elif tile == 11:
                    player = Character(image_x, image_y, 90, 100, mob_animations, 0, False, 1)
                    self.player = player
                    tile_data[0] = tile_list[0]
                # 12 - 16 are all enemies; 17 is the boss *** tweak HP values and size
                elif tile == 12:
                    enemy = Character(image_x, image_y, 10, 10, mob_animations, 1, False, 1)
                    self.all_enemies.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 13:
                    enemy = Character(image_x, image_y, 10, 10, mob_animations, 2, False, 1)
                    self.all_enemies.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 14:
                    enemy = Character(image_x, image_y, 10, 10, mob_animations, 3, False, 1)
                    self.all_enemies.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 15:
                    enemy = Character(image_x, image_y, 10, 10, mob_animations, 4, False, 1)
                    self.all_enemies.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 16:
                    enemy = Character(image_x, image_y, 10, 10, mob_animations, 5, False, 1)
                    self.all_enemies.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 17:
                    enemy = Character(image_x, image_y, 100, 100, mob_animations, 6, True, 2)
                    self.all_enemies.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 18:  # merchant
                    npc = Character(image_x, image_y, 50, 50, mob_animations, 7, False, 2, True)
                    self.all_enemies.append(npc)
                    tile_data[0] = tile_list[0]

                elif tile == 23 or tile == 24 or tile == 25:
                    self.wall_tiles.append(tile_data)

                # under development // overlay tiles
                elif tile == 26:
                    self.overlay_tiles.append(tile_data)
                    # tile_data[0] = tile_list[0]

                # adds the single tile to the map tiles list
                # no negative images so must be positive value
                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):

        for tile in self.map_tiles:
            # first argument is which tile, second argument is where to be drawn
            surface.blit(tile[0], tile[1])

        # draws overlay tiles
        for tile in self.overlay_tiles:
            surface.blit(tile[0], tile[1])
