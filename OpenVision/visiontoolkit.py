import RepoMan

# Loading Module dependencies.
repo = RepoMan.Module()
x = repo.load(module_path='FaceID', modules=['adaptiveLearning', 'faceId'])
print(x)
