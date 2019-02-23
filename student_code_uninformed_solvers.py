
from solver import *
import queue
import copy
# from read import *
class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
    # count = 1
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
            # self.count += 1
            newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, movables[self.currentState.nextChildToVisit])
            newState.parent = self.currentState
            if newState in self.visited:
                self.gm.reverseMove(movables[self.currentState.nextChildToVisit])
                # self.count -= 1
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
        self.queue = queue.Queue()
        self.flagInsert = 0

        self.currentState.requiredMovable = []
        self.initiategm = copy.deepcopy(gameMaster)
        self.count = 0
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
        self.count += 1
        # movables = self.gm.getMovables()
        # input the root node into queue
        if self.flagInsert == 0:
            self.flagInsert = 1
            self.queue.put(self.currentState)

        # not find and queue is empty
        if self.queue.empty():
            return False

        while not self.queue.empty():
            # get from queue until it is empty
            nextState = self.queue.get()
            if nextState in self.visited:
                # if this is root
                if nextState.requiredMovable == []:
                    for movables in self.gm.getMovables():
                        self.gm.makeMove(movables)
                        newState = GameState(self.gm.getGameState(), self.currentState.depth + 1,
                                             [movables])
                        if newState in self.visited:
                            self.gm.reverseMove(movables)
                        else:
                            newState.parent = nextState
                            self.queue.put(newState)
                            self.gm.reverseMove(movables)
                            # self.gm = self.initiategm
                    # after put all children into queue, return
                    # return False
                    continue
                else:
                    continue
            else:
                #get one node and break
                break
        # queue is empty now and all nodes have been visited
        if nextState in self.visited and self.queue.empty():
            return False
        else:
            self.gm = copy.deepcopy(self.initiategm)
            self.visited[nextState] = True
            # successfully get nextState from queue
            # from init state to the state here
            for step in nextState.requiredMovable:
                self.gm.makeMove(step)
            print("self.currentState", self.currentState.state)
            print(self.count, "current state = ", str(nextState.state))
            print("game state = ", str(self.gm.getGameState()), "\n\n")

            # get new node and put them into queue
            for movables in self.gm.getMovables():
                # deep copy?
                # is it reference?
                # maybe I need to edit it
                self.gm.makeMove(movables)
                temp = nextState.requiredMovable[:]
                temp.append(movables)
                newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, temp)
                # will it be a problem that newState.requiredMovables are different?
                if newState in self.visited:
                    self.gm.reverseMove(movables)
                else:
                    self.queue.put(newState)
                    newState.parent = nextState
                    # go back to parent and get other children
                    self.gm.reverseMove(movables)
            # go back to root
            self.currentState = copy.deepcopy(nextState)

        return False
















        '''
        if self.queue.empty():
            return False
        else:
            nextState = self.queue.get()
            while nextState in self.visited:
                nextState = self.queue.get()
            # here is root, nextState is self.currentState
            if nextState.requiredMovable == None:
                # input all the children into queue
                for movables in self.gm.getMovables():
                    self.gm.makeMove(movables)
                    newState = GameState(self.gm.getGameState(), self.currentState.depth + 1,
                                         movables)
                    if newState in self.visited:
                        self.gm.reverseMove(movables)
                    else:
                        self.queue.put(newState)
                        #record all the children node
                        nextState.nextChildrenToVisit += 1
                        nextState.children.append(newState)
                        newState.parent = nextState
                        self.gm.reverseMove(movables)
            # not root, go back
            else:
                # nextstate is not the child of the current state, go up
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                nextChild = self.currentState.nextChildToVisit
                # if the child are the last
                while self.currentState.nextChildToVisit < len(self.currentState.children):
                    # if the child is visited
                    if self.currentState.children[self.currentState.nextChildToVisit] in self.visited:
                        # to try the next child
                        self.currentState.nextChildToVisit += 1
                        continue
                    else:
                        # go down
                        if self.currentState.children[self.currentState.nextChildToVisit] != nextState:
                            print("state is not corresponding to ")
                        self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit].requiredMovable)

                        # one more child has been visited
                        self.currentState.nextChildToVisit += 1

                        # state go down and it is new node
                        self.currentState = nextState
                        return False
                else:
                    while self.currentState.nextChildToVisit >= len(self.currentState.children):
                        self.gm.reverseMove(self.currentState.requiredMovable)
                        self.currentState = self.currentState.parent
            #self.gm.makeMove(nextState.requiredMovable)
            #self.currentState = nextState
        '''



