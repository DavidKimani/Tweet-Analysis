from app.tweets import Tweet

if __name__ == "__main__":

    state = True
    while (state):
        screenName = input("Hi there! Please enter your Twitter username\n")

        if(screenName == ""):
            print("You must enter a value\n")
            screenName = "NdirituDayvd"
            # break
        elif(screenName.lower() == "exit"):
            state = False
            break

        tweep = Tweet(screenName)
        tweep.fetch()
        pass