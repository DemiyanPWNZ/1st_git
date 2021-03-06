#"риверси"
import random
import sys
WIDTH = 8 #игровое поле 8 на 8
HEIGHT = 8

def drawBoard(board):
    #выводит игровое поле ничего не возвращает
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
        print('%s|' % (y+1), end='')
        for x in range(WIDTH):
            print(board[x][y], end='')
        print('|%s' % (y+1))
    print(' +--------+')
    print('  12345678')

def getNewBoard():
    #создает чистое поле
    board = []
    for i in range(WIDTH):
        board.append([' ',' ',' ',' ', ' ', ' ',' ',' '])
    return board

def isValidMove(board,tile,xstart,ystart):
    #вернет False если ход игрока в клетку с координатами хстарт и устарт - недопустим
    #если это допустимый ход вернуть список клеток которые присвоил бы игрок
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []

    for xdirection, ydirection in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
        x , y = int(xstart), int(ystart)
        x += xdirection #первые шаги в направлении
        y += ydirection
        while isOnBoard(x,y) and board[x][y] == otherTile:
            # продолжать движение в направлении
            x += xdirection
            y += ydirection
            if isOnBoard(x,y) and board[x][y] == tile:
    #есть фишки которые можно перевернуть. двигаться в обратном навправлении до достежегния исходной клетки и отмечать фишки на пути
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x,y])
    if  len(tilesToFlip) == 0: #если ни одна из фишек не перевернулаась - недопустимый ход
        return False
    return tilesToFlip

def isOnBoard(x,y):
    #Вернуть тру если есть такая координата
    return int(x)>=0 and int(x)<=WIDTH-1 and  int(y)>=0 and int(y)<=HEIGHT-1

def getBoardWithValidMoves(board,tile):
    #Вернуть новое поле с точками обозначающие допустимые ходы которые может сделать игрок
    boardCopy = getBoardCopy(board)

    for x,y in getValidMoves(boardCopy, tile):
        boardCopy[x][y] = '.'
    return boardCopy

def getValidMoves(board, tile):
    #вернуть список списков с координатами х и у допустимых ходов для данного игрока на данном игровом поле.
    validMoves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board,tile,x,y) != False:
                validMoves.append([x,y])
    return validMoves

def getScoreOfBoard(board):
    #определить количество очков, подсчитав фишки. вернуть словарь с ключами 'x' и "о"
    xscore = 0
    oscore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X' : xscore ,'O' : oscore}

def enterPlayerTile():
    #позволяет игроку ввести выбраную фишку
#возвращает список фишек игрока в качестве первого элемента и фишкой компьютера в качестве второго.
    tile =''
    while not (tile =='X' or tile == 'O'):
        print('Вы играете за X или O?')
        tile = input().upper()

    #первый элемент в списке   - фишка игрока, второй элемент фишка компьютера
    if tile == 'X':
        return ['X','O']
    else :
        return ['O','X']

def whoGoesFirst():
    #случайно выбрать кто ъходит первым
    if random.randint(0,1) == 0:
        return  'Компьютер'
    else:
        return  'Человек'

def makeMove(board, tile, xstart,ystart):
    #поместить фишку на игровое поле в позицию хстарт и устарт и перевернуть какую либо фишку противника
        #вернуть false   если это недопустимый ход иначе вернуть True
        tilesToFlip = isValidMove(board,tile,xstart,ystart)

        if tilesToFlip == False:
            return False

        board[xstart][ystart] = tile
        for x,y in tilesToFlip:
            board[x][y] = tile
        return True

def getBoardCopy(board):
    #сделать копию списка boardи вернуть ее.
    boardCopy = getNewBoard()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y] = board[x][y]

    return boardCopy

def isOnCorner(x,y):
    #вернуть True  если указаная позиция назодится в одном из четырех углов
    return (x == 0 or x == WIDTH-1) and (y == 0 or y == HEIGHT -1)

def getPlayerMove(board, playerTile):
    #позволить игроку ввести свой ход
    #вернуть ход в виде [x,y] или вернуть строки 'подсказка' иди 'выход'
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Укажите ход, текст \'выход\' для завершения игры или \'подсказка\' для вывода посказки')
        move = input().lower()

        if move == 'выход' or 'подсказка':
            return move
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0])-1
            y = int(move[1])-1

            if isValidMove(board, playerTile, x,y) == False:
                continue
            else:
                break
        else:
            print('Это недопустимый ход. Введите номер столбца (1-8) и номер ряда (1-8).')
            print('К примеру, значение 81 перемешает в верхний правый угол')


    return [x,y]

def getComputerMove(board,computerTile):
    #учитывая данное игровое поле и данную фишку компьютера, определить,
    #куда сделать зодЮ и вернуть этот ход в виде списка [x,y]
    possibleMoves = getValidMoves(board,computerTile)
    random.shuffle(possibleMoves)# сделать случайным поряджок ходов

    #всегда делать ход в угол если это возможно
    for x,y in possibleMoves:
        if isOnCorner(x,y):
            return [x,y]

    #найти ход с наибольшим количеством очков.
    bestScore = -1
    for x,y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScoreOfBoard(boardCopy)[computerTile]
        if score > bestScore:
            bestMove = [x,y]
            bestScore = score
    return  bestMove

def printScore(board,playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print('Ваш счёт: %s. Счёт компьютера: %s.' % (scores[playerTile],scores[computerTile]))

def playGame(playerTile, computerTile):
    showHints = False
    turn = whoGoesFirst()
    print(turn + ' ходит первым.')

    #Очистить тигровое поле и выставить стартовые фишки
    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)

        if playerValidMoves == [] and computerValidMoves == []:
            return  board # ходов ни у кого нет окончить игру

        elif turn  == 'Человек':#ход человека
            if playerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                printScore(board,playerTile,computerTile)

                move = getPlayerMove(board, playerTile)
                if move == 'выход':
                    print('Благодарим за игру!')
                    sys.exit()
                elif move == 'подсказка':
                    showHints = not showHints
                    continue
                else:
                    makeMove(board,playerTile,int(move[0])-1,int(move[1])-1)

            turn = 'Компьютер'

        elif turn == 'Компьютер':
            if computerValidMoves != []:
                drawBoard(board)
                printScore(board,playerTile,computerTile)

                input('Нажмите клавишу Enter для просмотра хода компьютера.')
                move = getComputerMove(board,computerTile)
                makeMove(board,computerTile,move[0],move[1])
            turn = 'Человек'


print('приветствуем в игре "Реверси"')

playerTile, computerTile = enterPlayerTile()

while True:
    finalBoard = playGame(playerTile,computerTile)

    #отобразить итоговый счёт
    drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('Х набрал %s очков. О набрал %s очков.' % (scores['X'],scores['O']))
    if scores[playerTile] > scores[computerTile]:
        print('Вы поебедили компьютер, обогнав его на %s очков! Поздравления!' % (scores[playerTile]-scores[computerTile]))
    elif scores[playerTile]< scores[computerTile]:
        print('Вы проиграли. Компьютер победил вас, обогнав на %s очков' % (scores[computerTile] - scores[playerTile]))
    else :
        print('Ничья!')

    print('Хотите сыграть еще раз? (да или нет)')
    if not input().lower().startswith('д'):
        break


