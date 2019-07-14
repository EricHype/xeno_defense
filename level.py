import os

class Level(object):
    def __init__(self, fileName):
        dirname = os.path.dirname(__file__)
        sub_dir = os.path.join(dirname, "levels")
        sub_file_path = os.path.join(sub_dir, fileName)

        file_object = open(sub_file_path, 'r')

        self.contents = file_object.readlines()

        file_object.close()

        self.height = self.__getHeight()
        self.width = self.__getWidth()

    def __getWidth(self):
        max_length = max(map(len, self.contents))
        return max_length

    def __getHeight(self):
        return len(self.contents)
