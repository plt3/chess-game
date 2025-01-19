class Chesspiece:

    spots = [a + str(i) for i in range(1, 9) for a in 'abcdefgh']
    whitespotlist = []
    blackspotlist = []
    whiteobjlist = []
    blackobjlist = []

    def __init__(self, color, piece, spot):
        self.color = color
        self.piece = piece
        self.spot = spot
        if color == 'white':
            Chesspiece.whitespotlist.append(self.spot)
            Chesspiece.whiteobjlist.append(self)
        else:
            Chesspiece.blackspotlist.append(self.spot)
            Chesspiece.blackobjlist.append(self)
        if piece == 'pawn':
            self.moves = [['U2'], ['W1'], ['X1']]
            self.runcount = 1
        elif piece == 'knight':
            self.moves = [['U2', 'L1'], ['U2', 'R1'], ['R2', 'U1'], ['R2', 'D1'],
            ['D2', 'R1'], ['D2', 'L1'], ['L2', 'D1'], ['L2', 'U1']]
        elif piece == 'rook':
            self.moves = [['U7'], ['D7'], ['L7'], ['R7']]
        elif piece == 'bishop':
            self.moves = [['W7'], ['X7'], ['Y7'], ['Z7']]
        elif piece == 'queen':
            self.moves = [['U7'], ['D7'], ['L7'], ['R7'], ['W7'], ['X7'], ['Y7'], ['Z7']]
        elif piece == 'king':
            self.moves = [['U1'], ['D1'], ['L1'], ['R1'], ['W1'], ['X1'], ['Y1'], ['Z1']]

    def all_spaces(self):
        letters = 'abcdefgh'
        all_list = []

        if self.piece == 'pawn':
            if self.color == 'black':
                if self.runcount == 1:
                    self.moves = [['D2'], ['Y1'], ['Z1']]
                else:
                    self.moves = [['D1'], ['Y1'], ['Z1']]
            elif self.color == 'white':
                if self.runcount > 1:
                    self.moves = [['U1'], ['W1'], ['X1']]

        for possibility in self.moves:
            sublist = []
            splitspot = list(self.spot)
            splitspot[1] = int(splitspot[1])
            for move in possibility:
                lstrindex = letters.find(self.spot[0])
                for i in range(int(move[1])):
                    if move[0] == 'U':
                        if splitspot[1] > 7:
                            break
                        splitspot[1] += 1
                    elif move[0] == 'D':
                        if splitspot[1] < 2:
                            break
                        splitspot[1] -= 1
                    elif move[0] == 'L':
                        lstrindex -= 1
                        if lstrindex == -1:
                            break
                        splitspot[0] = letters[lstrindex]
                    elif move[0] == 'R':
                        lstrindex += 1
                        if lstrindex == 8:
                            break
                        splitspot[0] = letters[lstrindex]
                    elif move[0] == 'W':
                        lstrindex -= 1
                        if splitspot[1] > 7 or lstrindex == -1:
                            break
                        splitspot[1] += 1
                        splitspot[0] = letters[lstrindex]
                    elif move[0] == 'X':
                        lstrindex += 1
                        if splitspot[1] > 7 or lstrindex == 8:
                            break
                        splitspot[1] += 1
                        splitspot[0] = letters[lstrindex]
                    elif move[0] == 'Y':
                        lstrindex += 1
                        if splitspot[1] < 2 or lstrindex == 8:
                            break
                        splitspot[1] -= 1
                        splitspot[0] = letters[lstrindex]
                    elif move[0] == 'Z':
                        lstrindex -= 1
                        if splitspot[1] < 2 or lstrindex == -1:
                            break
                        splitspot[1] -= 1
                        splitspot[0] = letters[lstrindex]
                    sublist.append(''.join(str(c) for c in splitspot))
            if len(sublist) > 0:
                all_list.append(sublist)

        if self.piece == 'knight':
            temp_list = []
            for minilist in all_list:
                if len(minilist) == 3:
                    temp_list.append([minilist[-1]])
            return temp_list

        return all_list

    def poss_spaces(self):
        all = self.all_spaces()
        potenspaces = []
        sublistcount = 0
        for sublist in all:
            sublistcount += 1
            for place in sublist:
                if self.color == 'white':
                    if self.piece == 'pawn':
                        if sublistcount > 1:
                            if place in Chesspiece.blackspotlist:
                                potenspaces.append(place)
                        elif place not in Chesspiece.whitespotlist and place not in Chesspiece.blackspotlist:
                            potenspaces.append(place)
                        else:
                            break
                    elif place not in Chesspiece.whitespotlist:
                        potenspaces.append(place)
                        if place in Chesspiece.blackspotlist:
                            break
                    else:
                        break
                elif self.color == 'black':
                    if self.piece == 'pawn':
                        if sublistcount > 1:
                            if place in Chesspiece.whitespotlist:
                                potenspaces.append(place)
                        elif place not in Chesspiece.whitespotlist and place not in Chesspiece.blackspotlist:
                            potenspaces.append(place)
                        else:
                            break
                    elif place not in Chesspiece.blackspotlist:
                        potenspaces.append(place)
                        if place in Chesspiece.whitespotlist:
                            break
                    else:
                        break

        return potenspaces

    def actual_poss_spaces(self):
        possmoves = self.poss_spaces()
        returnspaces = []
        for move in possmoves:
            if not self.moveforcheck(move):
                returnspaces.append(move)

        return returnspaces

    def movepiece(self, space):
        print(self.color.capitalize(), self.piece, 'moves to', space, end='.\n')
        if self.color == 'white':
            index = Chesspiece.whitespotlist.index(self.spot)
            Chesspiece.whitespotlist[index] = space
            if space in Chesspiece.blackspotlist:
                for ins in Chesspiece.blackobjlist:
                    if ins.spot == space:
                        print('White', self.piece, 'takes black', ins.piece, end='.\n')
                        Chesspiece.blackspotlist.remove(ins.spot)
                        Chesspiece.blackobjlist.remove(ins)
                        break
        elif self.color == 'black':
            index = Chesspiece.blackspotlist.index(self.spot)
            Chesspiece.blackspotlist[index] = space
            if space in Chesspiece.whitespotlist:
                for ins in Chesspiece.whiteobjlist:
                    if ins.spot == space:
                        print('Black', self.piece, 'takes white', ins.piece, end='.\n')
                        Chesspiece.whitespotlist.remove(ins.spot)
                        Chesspiece.whiteobjlist.remove(ins)
                        break
        if self.piece == 'pawn':
            self.runcount += 1

        self.spot = space

    def moveforcheck(self, space):
        oldspot = self.spot

        if self.color == 'white':
            index = Chesspiece.whitespotlist.index(self.spot)
            Chesspiece.whitespotlist[index] = space
            self.spot = space
            istherecheck = ischeck(ki1)
            if space in Chesspiece.blackspotlist:
                for ins in Chesspiece.blackobjlist:
                    if ins.spot == space:
                        Chesspiece.blackspotlist.remove(ins.spot)
                        Chesspiece.blackobjlist.remove(ins)

                        istherecheck = ischeck(ki1)

                        Chesspiece.blackspotlist.append(ins.spot)
                        Chesspiece.blackobjlist.append(ins)
                        break
            Chesspiece.whitespotlist[index] = oldspot
            self.spot = oldspot
            return istherecheck

        elif self.color == 'black':
            index = Chesspiece.blackspotlist.index(self.spot)
            Chesspiece.blackspotlist[index] = space
            self.spot = space
            istherecheck = ischeck(ki2)
            if space in Chesspiece.whitespotlist:
                for ins in Chesspiece.whiteobjlist:
                    if ins.spot == space:
                        Chesspiece.whitespotlist.remove(ins.spot)
                        Chesspiece.whiteobjlist.remove(ins)

                        istherecheck = ischeck(ki2)

                        Chesspiece.whitespotlist.append(ins.spot)
                        Chesspiece.whiteobjlist.append(ins)
                        break
            Chesspiece.blackspotlist[index] = oldspot
            self.spot = oldspot
            return istherecheck


def ischeck(kingobj):
    if kingobj.color == 'white':
        for piece in Chesspiece.blackobjlist:
            all = piece.poss_spaces()
            if kingobj.spot in all:
                return True
                break
    else:
        for piece in Chesspiece.whiteobjlist:
            all = piece.poss_spaces()
            if kingobj.spot in all:
                return True
                break

    return False


def ischeckmate(kingobj):
    if kingobj.color == 'white':
        for obj in Chesspiece.whiteobjlist:
            if obj.actual_poss_spaces() != []:
                return False
                break
    else:
        for obj in Chesspiece.blackobjlist:
            if obj.actual_poss_spaces() != []:
                return False
                break
    return True


pa1 = Chesspiece('white', 'pawn', 'a2')
pa2 = Chesspiece('white', 'pawn', 'b2')
pa3 = Chesspiece('white', 'pawn', 'c2')
pa4 = Chesspiece('white', 'pawn', 'd2')
pa5 = Chesspiece('white', 'pawn', 'e2')
pa6 = Chesspiece('white', 'pawn', 'f2')
pa7 = Chesspiece('white', 'pawn', 'g2')
pa8 = Chesspiece('white', 'pawn', 'h2')
ro1 = Chesspiece('white', 'rook', 'a1')
ro2 = Chesspiece('white', 'rook', 'h1')
kn1 = Chesspiece('white', 'knight', 'b1')
kn2 = Chesspiece('white', 'knight', 'g1')
bi1 = Chesspiece('white', 'bishop', 'c1')
bi2 = Chesspiece('white', 'bishop', 'f1')
qu1 = Chesspiece('white', 'queen', 'd1')
ki1 = Chesspiece('white', 'king', 'e1')

pa9 = Chesspiece('black', 'pawn', 'a7')
pa10 = Chesspiece('black', 'pawn', 'b7')
pa11 = Chesspiece('black', 'pawn', 'c7')
pa12 = Chesspiece('black', 'pawn', 'd7')
pa13 = Chesspiece('black', 'pawn', 'e7')
pa14 = Chesspiece('black', 'pawn', 'f7')
pa15 = Chesspiece('black', 'pawn', 'g7')
pa16 = Chesspiece('black', 'pawn', 'h7')
ro3 = Chesspiece('black', 'rook', 'a8')
ro4 = Chesspiece('black', 'rook', 'h8')
kn3 = Chesspiece('black', 'knight', 'b8')
kn4 = Chesspiece('black', 'knight', 'g8')
bi3 = Chesspiece('black', 'bishop', 'c8')
bi4 = Chesspiece('black', 'bishop', 'f8')
qu2 = Chesspiece('black', 'queen', 'd8')
ki2 = Chesspiece('black', 'king', 'e8')


def main():
    counter = 0
    print("\nWelcome to playchess.py. Follow the program's instructions to move pieces.")
    print('After selecting the spot of the piece you would like to move, you may enter')
    input('"moves" to see the list all of possible moves. Press Enter to start the game: ')
    print()

    while True:
        if counter % 2 == 0:
            userspot = input('White, enter spot of piece to move: ')

            if userspot in Chesspiece.whitespotlist:
                for instance in Chesspiece.whiteobjlist:
                    if instance.spot == userspot:
                        allmoves = instance.poss_spaces()
                        noncheckmoves = instance.actual_poss_spaces()
                        break

            while userspot not in Chesspiece.whitespotlist or allmoves == [] or noncheckmoves == []:
                if userspot not in Chesspiece.whitespotlist:
                    print('No white piece is at ' + userspot + '. Try again:', end=' ')
                elif allmoves == []:
                    print(instance.color.capitalize(), instance.piece, 'at', instance.spot, 'can not move anywhere. Try again:', end=' ')
                else:
                    print('Any move', instance.color, instance.piece, 'at', instance.spot, 'can make will put',
                          instance.color, 'king in check. Try again:', end=' ')

                userspot = input()

                if userspot in Chesspiece.whitespotlist:
                    for instance in Chesspiece.whiteobjlist:
                        if instance.spot == userspot:
                            allmoves = instance.poss_spaces()
                            noncheckmoves = instance.actual_poss_spaces()
                            break

            for instance in Chesspiece.whiteobjlist:
                if instance.spot == userspot:
                    print('Where would you like to move', instance.color, instance.piece, 'to?', end=' ')
                    usermove = input()

                    while True:
                        if usermove == 'moves':
                            print('Possible moves:', ', '.join(noncheckmoves))
                            print('Where would you like to move?', end=' ')
                        elif usermove not in instance.poss_spaces():
                            print(usermove, 'is not a possible spot. Try again:', end=' ')
                        elif instance.moveforcheck(usermove):
                            print('Moving to', usermove, 'will put', instance.color, 'king in check. Try again:', end=' ')
                        else:
                            break

                        usermove = input()

                    instance.movepiece(usermove)
                    v = ischeck(ki2)
                    x = ischeckmate(ki2)
                    if v and not x:
                        print('Black king is in check.')
                    break

            if x:
                print('Checkmate. White wins!')
                break
        else:
            userspot = input('Black, enter spot of piece to move: ')

            if userspot in Chesspiece.blackspotlist:
                for instance in Chesspiece.blackobjlist:
                    if instance.spot == userspot:
                        allmoves = instance.poss_spaces()
                        noncheckmoves = instance.actual_poss_spaces()
                        break

            while userspot not in Chesspiece.blackspotlist or allmoves == [] or noncheckmoves == []:
                if userspot not in Chesspiece.blackspotlist:
                    print('No black piece is at ' + userspot + '. Try again:', end=' ')
                elif allmoves == []:
                    print(instance.color.capitalize(), instance.piece, 'at', instance.spot, 'can not move anywhere. Try again:', end=' ')
                else:
                    print('Any move', instance.color, instance.piece, 'at', instance.spot, 'can make will put',
                          instance.color, 'king in check. Try again:', end=' ')

                userspot = input()

                if userspot in Chesspiece.blackspotlist:
                    for instance in Chesspiece.blackobjlist:
                        if instance.spot == userspot:
                            allmoves = instance.poss_spaces()
                            noncheckmoves = instance.actual_poss_spaces()
                            break

            for instance in Chesspiece.blackobjlist:
                if instance.spot == userspot:
                    print('Where would you like to move', instance.color, instance.piece, 'to?', end=' ')
                    usermove = input()

                    while True:
                        if usermove == 'moves':
                            print('Possible moves:', ', '.join(noncheckmoves))
                            print('Where would you like to move?', end=' ')
                        elif usermove not in instance.poss_spaces():
                            print(usermove, 'is not a possible spot. Try again:', end=' ')
                        elif instance.moveforcheck(usermove):
                            print('Moving to', usermove, 'will put', instance.color, 'king in check. Try again:', end=' ')
                        else:
                            break

                        usermove = input()

                    instance.movepiece(usermove)
                    v = ischeck(ki1)
                    x = ischeckmate(ki1)
                    if v and not x:
                        print('White king is in check.')
                    break

            if x:
                print('Checkmate. Black wins!')
                break

        counter += 1

if __name__ == "__main__":
    main()