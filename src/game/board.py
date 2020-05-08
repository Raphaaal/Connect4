import random
import copy
import numpy as np
from src.common.constants import EMPTY, RED, YELLOW, DX, DY, NUMBER_TO_WIN
from src.game.move import Move
class Board():
    def __init__(self):
        self.board = np.full((DX, DY), EMPTY)
        self.tokens_level = np.full(DY, DX-1)
        self.turn = RED
        self.finished = False
        self.winner = 0
        
        
    def legal_moves(self):
        moves = []
        for i in range(DY):
            if self.tokens_level[i] >= 0:
                moves.append(Move(self.turn, i))
        return moves
    
    
    def playout(self, played=None, verbose=False):
        while (not self.finished):
            possible_moves = self.legal_moves()
            move = random.choice(possible_moves)
            if played is not None:
                played.append(move)
            self.play(move)
            if verbose:
                print("-------------")
                print(self.board)
 
        return self.winner

    
    def play(self, move):
        column = move.column
        row = self.tokens_level[column]
        color = move.color
        self.board[row][column] = color
        self.tokens_level[column] = row-1
        self._change_turn()
        self._check_finished(row, column, color)
         
    
    def manual_move(self, n=None):
        moves = self.legal_moves()
        legal=False
        while(not legal):
            column = input("In which column do you want to insert your token ?")
            move = Move(self.turn, int(column))

            for legal_move in moves:
                if move.equals(legal_move):
                    print("Let's do that")
                    legal=True
            if(not legal):
                print("you tried: ")
                move.render()
                print("This move isn't valid, here are valids moves :")
                for m in moves:
                    m.render()  
        return move
    
    
    def flat_mc(self, n=1000):
        moves = self.legal_moves()
        scores = []
        nb_ite_per_move = int(n/len(moves))
        for move in moves:
            total = 0
            for i in range(nb_ite_per_move):
                copy_board = copy.deepcopy(self)
                copy_board.play(move)
                won = 1 if copy_board.playout() == self.turn else 0
                total += won
            scores.append(total)
        return moves[scores.index(max(scores))]

    
    def _change_turn(self):
        if self.turn == RED:
            self.turn = YELLOW
        elif self.turn == YELLOW :
            self.turn = RED
                             
                             
    def _check_finished(self, row_played, column_played, color):
        if row_played == 0:
            if np.array([x < 0 for x in self.tokens_level]).all():
                self.finished = True
                self.winner = 0
        if (self._check_column(column_played, color) or 
            self._check_row(row_played, color) or 
            self._check_diagonal(row_played, column_played, color) or
            self._check_diagonal(row_played, column_played, color, False)):
            self.finished = True
            self.winner = color
            
        
    def _check_column(self, column, color):
        connected = 0
        for i in range(DX):
            if self.board[i, column] == color:
                connected += 1 
            elif connected < NUMBER_TO_WIN:
                connected = 0
        return connected >= NUMBER_TO_WIN

                             
    def _check_row(self, row, color):
        connected = 0
        for j in range(DY):
            if self.board[row, j] == color:
                connected += 1 
            elif connected < NUMBER_TO_WIN:
                connected = 0
        return connected >= NUMBER_TO_WIN
   
       
    def _check_diagonal(self, row, column, color, ascending=True):
        if ascending:                     
            range_x = range(min(row + column, DX-1), max(-1, row - (DY-column)), -1)
            range_y = range(max(0, column - ((DX-1) - row)), min(DY, row+column+1))
        else:
            range_x = range(max(row - column, 0), min(DX, row+(DY-column)))
            range_y = range(max(0, column-row), min(DY, column+((DX-1) - row) + 1))
        connected = 0
        for i,j in zip(range_x, range_y):
            if self.board[i, j] == color:
                connected += 1 
            elif connected < NUMBER_TO_WIN:
                connected = 0
        return connected >= NUMBER_TO_WIN