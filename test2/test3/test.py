import os

for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        print(file)

