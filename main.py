import agent
import util
import slither

if __name__ == '__main__':
    print('Start Game')
    slither = slither.Slither(400,400)
    slither.initGame()
    slither.runGame(agent.BreadthFirstSearch)