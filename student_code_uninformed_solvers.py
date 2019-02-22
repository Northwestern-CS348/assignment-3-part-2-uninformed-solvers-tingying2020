
from solver import *
# from read import *
class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
    count = 1
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
        '''
        print(movables, "\n",self.currentState.nextChildToVisit)
        print(self.count,"current state = ",str(self.currentState.state))
        print("game state = ", str(self.gm.getGameState()), "\n\n")
        if self.count == 3:
            ask = parse_input("fact: (topof ?X peg1)")
            answer = self.gm.kb.kb_ask(ask)
            print(answer, "-=-=-=-=--=-=-=--=--=-=-=--=-=-")
            ask = parse_input("fact: (topof ?X peg3)")
            answer = self.gm.kb.kb_ask(ask)
            print(answer, "-=-=-=-=--=-=-=--=--=-=-=--=-=-")
            ask = parse_input("fact: (larger disk3 ?X)")
            answer = self.gm.kb.kb_ask(ask)
            print(answer, "-=-=-=-=--=-=-=--=--=-=-=--=-=-")
            ask = parse_input("fact: (movable disk1 ?X ?Y)")
            answer = self.gm.kb.kb_ask(ask)
            print(answer, "-=-=-=-=--=-=-=--=--=-=-=--=-=-")
        # print("nextchild", self.currentState.nextChildToVisit, "\n\n")
        # for i in range(self.currentState.nextChildToVisit, len(movables)):
        '''
        while self.currentState.nextChildToVisit < len(movables):
            # self.currentState.nextChildToVisit += 1
            self.gm.makeMove(movables[self.currentState.nextChildToVisit])
            self.count += 1
            newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, movables[self.currentState.nextChildToVisit])
            newState.parent = self.currentState
            if newState in self.visited:
                self.gm.reverseMove(movables[self.currentState.nextChildToVisit])
                self.count -= 1
                self.currentState.nextChildToVisit += 1

                # self.currentState.state = self.gm.getGameState()
            else:
                self.currentState.nextChildToVisit += 1
                # self.visited[newState] = True
                self.currentState = newState
                # newState.parent = self.currentState
                # print(self.currentState.state)
                return False
        # if i == len(movables)-1:
        self.gm.reverseMove(self.currentState.requiredMovable)
        self.currentState = self.currentState.parent
        # print("go back!")
        return False
        # return False









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
        if self.currentState.state == self.victoryCondition:
            return True
        # self.visited[self.currentState] = True
        movables = self.gm.getMovables()

        while self.currentState.nextChildToVisit < len(movables):
            nextChild = movables[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1
            self.gm.makeMove(nextChild)
            newState = GameState(self.gm.getGameState(), self.currentState.depth + 1,
                                 movables[self.currentState.nextChildToVisit])
            #newState.parent = self.currentState
            if newState in self.visited:
                self.gm.reverseMove(nextChild)
                continue
            else:
                self.visited[newState] = True
                self.currentState.children.append(newState)
                self.gm.reverseMove(nextChild)
                return False
        if self.currentState.nextChildToVisit == len(movables):
            for i in range(len(self.currentState.children)-1):
                self.currentState.children[i].parent = self.currentState.children[i+1]
                self.currentState.children[i + 1].parent = self.currentState.children[0]
            self.currentState.nextChildToVisit += 1



        #go to next layer




