from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        '''
        if answer != []:
            print("123",answer[0].bindings_dict[x],"123")
            for disk in answer:
                pass
        
        ask1 = parse_input("fact: (topof ?X peg1)")
        answer = self.kb.kb_ask(ask1)
        peglist1 = []

        if answer != []:
            print(answer.list_of_bindings[0][0].bindings_dict['?X'], '\n')
        '''
        ask1 = parse_input("fact: (topof ?X peg1)")
        ask2 = parse_input("fact: (topof ?X peg2)")
        ask3 = parse_input("fact: (topof ?X peg3)")
        return(self.stateInPeg(ask1),self.stateInPeg(ask2), self.stateInPeg(ask3))


    def stateInPeg(self, ask1):
        answer = self.kb.kb_ask(ask1)
        peglist1 = []
        while answer != False:
            # print(type(answer))
            disk_peg = answer.list_of_bindings[0][0].bindings_dict['?X']
            # print(type(disk_peg), '----------------', disk_peg)
            peglist1.append(int(disk_peg[4:]))
            ask1 = parse_input("fact: (top {} ?X)".format(disk_peg))
            answer = self.kb.kb_ask(ask1)
            # print(peglist1)
        return tuple(peglist1)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        #str(movable_statement.terms[0].term) is disk1 str(movable_statement.terms[1].term) is peg1
        ### Student code goes here
        #if it is not a move
        if movable_statement.predicate != 'movable':
            return


        a1,a2,a3,a4,a5 = [], [],[],[],[]

        ask3 = parse_input("fact: (top {} ?X)".format(str(movable_statement.terms[0].term)))
        answer3 = self.kb.kb_ask(ask3)
        if answer3 != False:
            #print(answer3.list_of_bindings[0][0].bindings_dict['?X'], 'is blow')
            r5 = parse_input("fact: (top {} {})".format(str(movable_statement.terms[0].term),
                                                        str(answer3.list_of_bindings[0][0].bindings_dict['?X'])))
            #print('retract', r5)
            self.kb.kb_retract(r5)
            a4 = parse_input("fact: (topof {} {})".format(str(answer3.list_of_bindings[0][0].bindings_dict['?X']),
                                                          str(movable_statement.terms[1].term)))
            #print('add', a4)
            ##self.kb.kb_assert(a4)
        else:
            a5 = parse_input("fact: (empty {})".format(str(movable_statement.terms[1].term)))
            #print('add', a5)
            ##self.kb.kb_assert(a5)
        target_empty = 0

        ask1 = parse_input("fact: (empty ?X)")
        answer1 = self.kb.kb_ask(ask1)
        if answer1 != False:
            for i in answer1.list_of_bindings:
                # print(type(movable_statement.terms[2].term))
                if str(movable_statement.terms[2].term) == i[0].bindings_dict['?X']:
                    #print(movable_statement.terms[2], 'is empty')
                    target_empty = 1

        # term[2] is an empty peg
        if target_empty == 1:
            r3 = parse_input("fact: (empty {})".format(str(movable_statement.terms[2].term)))
            #print('retract', r3)
            self.kb.kb_retract(r3)
        else:
            # term[2] is not an empty peg
            ask2 = parse_input("fact: (topof ?X {})".format(str(movable_statement.terms[2].term)))
            answer2 = self.kb.kb_ask(ask2)
            if answer2 == False:
                print("============={} has nothing on it!=================".format(str(movable_statement.terms[2].term)))
            else:
                r4 = parse_input("fact: (topof {} {})".format(str(answer2.list_of_bindings[0][0].bindings_dict['?X']),str(movable_statement.terms[2].term)))
                #print('retract', r4)
                self.kb.kb_retract(r4)
                a3 = parse_input("fact: (top {} {})".format(str(movable_statement.terms[0].term), str(answer2.list_of_bindings[0][0].bindings_dict['?X'])))
                #print('add', a3)
                ##self.kb.kb_assert(a3)

        r1 = parse_input(
            "fact: (topof {} {})".format(str(movable_statement.terms[0].term), str(movable_statement.terms[1].term)))
        #print('retract', r1)
        self.kb.kb_retract(r1)
        r2 = parse_input(
            "fact: (on {} {})".format(str(movable_statement.terms[0].term), str(movable_statement.terms[1].term)))
        #print('retract', r2)
        self.kb.kb_retract(r2)
        a1 = parse_input(
            "fact: (topof {} {})".format(str(movable_statement.terms[0].term), str(movable_statement.terms[2].term)))
        #print('add', a1)
        ##self.kb.kb_assert(a1)
        a2 = parse_input(
            "fact: (on {} {})".format(str(movable_statement.terms[0].term), str(movable_statement.terms[2].term)))
        #print('add', a2)
        ##self.kb.kb_assert(a2)

        A05 = [a1,a2,a3,a4,a5]
        for item in A05:
            if item!=[]:
                self.kb.kb_assert(item)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        return (self.getByRow('pos1'), self.getByRow('pos2'), self.getByRow('pos3'))

    def getByRow(self, rowNum):
        rowPuzzle = []
        ask1 = parse_input("fact: (at ?X pos1 {})".format(rowNum))
        answer1 = self.kb.kb_ask(ask1)
        if answer1 == False:
            rowPuzzle.append(-1)
        else:
            tile1 = answer1.list_of_bindings[0][0].bindings_dict['?X']
            rowPuzzle.append(int(tile1[4:]))

        ask2 = parse_input("fact: (at ?X pos2 {})".format(rowNum))
        answer2 = self.kb.kb_ask(ask2)
        if answer2 == False:
            rowPuzzle.append(-1)
        else:
            tile2 = answer2.list_of_bindings[0][0].bindings_dict['?X']
            rowPuzzle.append(int(tile2[4:]))

        ask3 = parse_input("fact: (at ?X pos3 {})".format(rowNum))
        answer3 = self.kb.kb_ask(ask3)
        if answer3 == False:
            rowPuzzle.append(-1)
        else:
            tile3 = answer3.list_of_bindings[0][0].bindings_dict['?X']
            rowPuzzle.append(int(tile3[4:]))

        return tuple(rowPuzzle)



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if movable_statement.predicate != 'movable':
            print("can't move")
            return

        term0 = movable_statement.terms[0].term.element
        term1 = movable_statement.terms[1].term.element
        term2 = movable_statement.terms[2].term.element
        term3 = movable_statement.terms[3].term.element
        term4 = movable_statement.terms[4].term.element

        r1 = parse_input("fact: (at {} {} {})".format(term0, term1, term2))
        self.kb.kb_retract(r1)
        r2 = parse_input("fact: (empty {} {})".format(term3, term4))
        self.kb.kb_retract(r2)
        a1 = parse_input("fact: (at {} {} {})".format(term0, term3, term4))
        self.kb.kb_assert(a1)
        a1 = parse_input("fact: (empty {} {})".format(term1, term2))
        self.kb.kb_assert(a1)



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
