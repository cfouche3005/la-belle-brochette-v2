from game.runtime import Runtime

def main():
    """
        Main function to run the game.
    :return:
    """
    game = Runtime((1280, 690)) # Initialize the game with a screen size of 1280x690
    game.run() # Run the game loop


if __name__ == '__main__':
    main()
