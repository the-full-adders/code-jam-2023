if True:
    import os

    from dotenv import load_dotenv
    load_dotenv()
    os.environ['SDL_VIDEO_X11_WMCLASS'] = 'cj-10-game'


from .manager.game_manager import GameManager


def run_game():
    """Runs the game

    Use this function to run the game.
    """
    game_manager = GameManager()
    game_manager.run()


if __name__ == '__main__':
    run_game()
