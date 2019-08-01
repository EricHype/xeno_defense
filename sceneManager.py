from scenes.titleScene import TitleScene
from scenes.gameScene import GameScene
from scenes.gameOverScene import GameOverScene

class SceneMananger(object):
    def __init__(self):
        self.currentScene = TitleScene({})
        self.currentScene.manager = self
        self.nextScene = None

    def get_scene(self):
        if(self.nextScene != None):
            self.currentScene = self.nextScene
            self.nextScene = None

        return self.currentScene

    def scene_change(self, sceneName, argsMap):
        statesMap = {
            "Title" : TitleScene,
            "Game" : GameScene,
            "GameOver" : GameOverScene 
        }

        self.nextScene = statesMap[sceneName](argsMap)
        self.nextScene.manager = self