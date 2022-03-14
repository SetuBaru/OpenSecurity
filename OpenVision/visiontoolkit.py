import RepoMan

# Loading Module dependencies.
loader = RepoMan.Module()
loader.load()
loader.load(_path='FaceID', modules=['adaptiveLearning', 'faceId'])
