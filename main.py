from game.runtime import Runtime

if __name__ == '__main__':
    game = Runtime((1280, 720))
    game.setup()
    game.run()