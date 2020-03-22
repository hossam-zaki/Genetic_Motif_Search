import sys
import argparse
from argparse import ArgumentParser
import os
import re

class local_aligning:
    def __init__(self, seq1, seq2, scoring_matrix, gap_penalty):
        self.gap_penalty = int(gap_penalty)
        self.seq1 = seq1
        self.seq2 = seq2
        self.scoring_dict = scoring_matrix
        self.alignment_matrix = None
        self.direction_matrix = None
        self.max_Rindex = 0
        self.max_Cindex = 0
        self.final_top_seq = None
        self.final_bottom_seq = None
        self.final_alignment_seq = None      
    def align_locally(self):
        self.alignment_matrix = [[0 for y in range (0, len(self.seq2) + 1)] for z in range(0, len(self.seq1) + 1)]
        self.direction_matrix = [[None for y in range (0, len(self.seq2) + 1)] for z in range(0, len(self.seq1) + 1)]
        for x in range (0, len(self.seq1)+ 1):
            self.alignment_matrix[x][0] = 0
            self.direction_matrix[x][0] = -1
        for y in range (0, len(self.seq2) + 1):
            self.alignment_matrix[0][y] = 0
            self.direction_matrix[0][y] = 0
        max_value = -float('inf')
        for i in range (1, len(self.alignment_matrix)):
            for j in range (1, len(self.alignment_matrix[0])):
                self.alignment_matrix[i][j] = max(0, (self.alignment_matrix[i-1][j] + self.gap_penalty), (self.alignment_matrix[i][j-1] + self.gap_penalty), (self.alignment_matrix[i-1][j-1] + self.scoring_dict[(self.seq1[i-1].upper(), self.seq2[j-1].upper())]))
                if self.alignment_matrix[i][j] > max_value:
                    max_value = self.alignment_matrix[i][j]
                    self.max_Rindex = i
                    self.max_Cindex = j
                if self.alignment_matrix[i][j] == self.alignment_matrix[i-1][j] -1:
                    self.direction_matrix[i][j] = -1
                elif self.alignment_matrix[i][j] == self.alignment_matrix[i][j-1] - 1:
                    self.direction_matrix[i][j] = 0
                else:
                    self.direction_matrix[i][j] = 1
        return (self.alignment_matrix[self.max_Rindex][self.max_Cindex] / len(self.seq2)) * 100
    def trace_back(self):
        top_string = ""
        bottom_string = ""
        alignment_string = ""
        boolean = True
        row_index = self.max_Rindex
        col_index = self.max_Cindex
        while boolean:
            value = self.direction_matrix[row_index][col_index]
            if value == -1 :
                bottom_string += "-"
                top_string += self.seq1[row_index -1]
                alignment_string += " "
                row_index = row_index - 1
            if value == 0 :
                top_string += "-"
                bottom_string += self.seq2[col_index - 1]
                col_index = col_index - 1
                alignment_string += " "
            if value == 1:
                bottom_string += self.seq2[col_index -1]
                top_string += self.seq1[row_index - 1]
                if(self.seq1[row_index - 1] == self.seq2[col_index -1]):
                    alignment_string += "|"
                else:
                    alignment_string += "/"
                col_index= col_index - 1
                row_index = row_index - 1
            if self.alignment_matrix[row_index][col_index] == 0:
                boolean = False
        self.final_top_seq=(self.reverse_str(top_string))
        self.final_bottom_seq=(self.reverse_str(bottom_string))
        self.final_alignment_seq = (self.reverse_str(alignment_string))
    def local_align(self):
        self.trace_back()
        print(self.final_top_seq)
        print(self.final_bottom_seq)
        print(self.alignment_matrix[self.max_Rindex][self.max_Cindex] / len(self.seq2) * 100)
    def reverse_str(self, string):
        new_str = ""
        for i in range (len(string) - 1, -1, -1):
            new_str+=string[i]
        return new_str
                    
