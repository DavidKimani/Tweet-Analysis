# import os.path
from os import path
from app.tweets import Tweet
from app.analyze import Analyze

if __name__ == "__main__":
    loop = True
    while(loop):
        screenName = input("Hi there! Please enter a Twitter username: ")

        if(screenName == ""):
            print("Enter a valid username!\n")
            break
        elif(screenName.lower() == "quit"):
            state = False
            break

        if(not path.exists(f"tweets/{screenName}.csv")):
            Tweet(screenName).fetch()
        Analyze(screenName).analyze()
        print("Type 'quit' to exit.\n\n")
        pass