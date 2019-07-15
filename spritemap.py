from actors.platform import Platform
import spritesheet


def getSpriteMap(tileSize):

    ss = spritesheet.spritesheet('PixelAtlas.png')
    groundImage = ss.load_image_at((0, 0, tileSize, tileSize))
    skyimage = ss.load_image_at((32, 96, tileSize, tileSize))
    wallImage = ss.load_image_at((32, 0, tileSize, tileSize))
    ceilingImage = ss.load_image_at((96, 0, tileSize, tileSize))

    spriteMap = {
        "P" : groundImage,
        "W" : wallImage,
        " " : skyimage,
        "C" : ceilingImage
    }
    return spriteMap