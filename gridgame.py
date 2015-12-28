from random import random,randint,choice
import gp

def start(players):
    board_size = (3, 3)
    last_move = [-1, -1]
    max_moves = 50
    total_dir = 4

    # remebers the player location
    location = [[randint(0, board_size[0]), randint(0, board_size[1])]]

    # put the second player a suffient distance from the first
    location.append([(location[0][0]+2)%total_dir,(location[0][1]+2)%total_dir])

    # maximum 50 moves before a tie
    for k in range(max_moves):

        # for each player
        for i in range(2):
            locations = location[i][:] + location[1-i][:]
            locations.append(last_move[i])
            move = players[i].evaluate(locations)%4

            # you lose if you move the same location twice in a row
            if last_move[i] == move: return i - 1

            last_move[i] = move

            if move == 0:
                location[i][0] -= 1
                # board limits
                if location[i][0] < 0: location[i][0] = 0

            if move == 1:
                location[i][0] += 1
                if location[i][0]>board_size[0]: location[i][0] = board_size[0]

            if move == 2:
                location[i][1] -= 1
                if location[i][1] < 0: location[i][1] = 0

            if move == 3:
                location[i][1] += 1
                if location[i][1]>board_size[1]: location[i][1] = board_size[1]

            # if you have captured the other player, you win
            if location[i] == location[i-1]: return i

    return -1


def tournament(players):
    losses = [0 for p in players]

    # every player plays against other players
    for i in range(len(players)):
        for j in range(len(players)):
            if i == j: continue

            winner = start([players[i], players[j]])

            # two points for a loss, one for a tie
            if winner == 0:
                losses[j] += 2
            elif winner == 1:
                losses[i] += 2
            elif winner == -1:
                losses[i] += 1
                losses[j] += 1
                pass

    z = zip(losses, players)
    z.sort()

    return z


class HumanPlayer:
    def evaluate(self, board):
        # get my location and the location of other players
        me = tuple(board[0:2])
        others = [tuple(board[x:x+2]) for x in range(2, len(board)-1, 2)]

        # display the board
        for i in range(4):
            for j in range(4):
                if (i,j) == me:
                    print '0',
                elif (i,j) in others:
                    print 'X',
                else:
                    print '.',
            print

        # show moves for reference
        print 'Your last move was %d' % board[len(board) - 1]
        print ' 0'
        print '2 3'
        print ' 1'
        print 'Enter move:'

        # return whatever the user enters
        move = int(raw_input())
        return move
