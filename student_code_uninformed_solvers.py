
from solver import *

class SolverDFS(UninformedSolver):
    count = 1
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        # print(type(self.victoryCondition))

        if self.currentState.state == self.victoryCondition:
            return True
        self.visited[self.currentState] = True
        movables = self.gm.getMovables()
        print(self.count,"current state = ",str(self.currentState.state))
        print("game state = ", str(self.gm.getGameState()))
        print("nextchild", self.currentState.nextChildToVisit, "\n\n")
        # for i in range(self.currentState.nextChildToVisit, len(movables)):
        while self.currentState.nextChildToVisit < len(movables):
            nextChild = movables[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1
            self.gm.makeMove(nextChild)
            self.count += 1

            newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, nextChild)
            newState.parent = self.currentState
            if newState in self.visited:
                self.gm.reverseMove(nextChild)
                # self.currentState.nextChildToVisit += 1
                self.count -= 1

                # self.currentState.state = self.gm.getGameState()
            else:
                # self.currentState.nextChildToVisit += 1
                self.visited[newState] = True
                self.currentState = newState
                # newState.parent = self.currentState
                # print(self.currentState.state)
                return False
        # if i == len(movables)-1:
        self.gm.reverseMove(self.currentState.requiredMovable)
        self.currentState = self.currentState.parent
        print("go back!")
        return False
        # return False
        '''
        # load all possible moves to children
        for i in self.gm.getMovables():
            self.currentState.children.append(i)

        while 1:
            if self.currentState.nextChildToVisit < len(self.currentState.children):
                movables = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1

                self.gm.makeMove(movables)
                # create new GameState and attach the current state to it
                newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, movables)
                newState.parent = self.currentState
                newState.state = self.gm.getGameState()
                print(newState.state)
                newState.nextChildToVisit = 0
                for i in self.gm.getMovables():
                    newState.children.append(i)

                if self.visited.__contains__(newState):
                    # this state has been visited, go back
                    self.gm.reverseMove(movables)
                    self.currentState.state = self.gm.getGameState()
                else:

                    # switch to the new state
                    self.currentState = newState
                    self.visited[self.currentState] = True

                    if self.currentState.state == self.victoryCondition:
                        return True
            else:
                # can't find
                if self.currentState.depth == 0:
                    return False

                # go back to parent
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
        '''







class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
