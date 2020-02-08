import logging

import pylights.game as game

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Starting Game")
    game.start()
    logger.info("Game Stopped")
