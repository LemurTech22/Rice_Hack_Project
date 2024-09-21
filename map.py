import pygame

class TileKind:
    def __init__(self, name, imageName, isSolid):
        self.name = name
        self.image = pygame.image.load(imageName)
        self.isSolid = isSolid

class Map:
    def __init__(self, mapFile, tileKinds, tileSize) -> None:
        self.tileKinds = tileKinds

        file = open(mapFile, "r")
        data = file.read()
        file.close()

        self.tiles = []
        for line in data.split("\n"):
            row = []
            for tileNum in line:
                row.append(int(tileNum))
            self.tiles.append(row)
        self.tileSize = tileSize

    def draw(self, display, xOffset, yOffset):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                location = ((x*self.tileSize)-xOffset, (y*self.tileSize)-yOffset)
                image = self.tileKinds[tile].image
                display.blit(image,location)