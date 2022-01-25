# wordle_assist
A basic and hastily written but effective Wordle assist with Python 3.X.

Files:
  1) words_alpha.txt - List of English words - not all are valid for wordle
  2) wordle_solve_vscode.py - Program

Has two functions:
  1) Recommend likely words and show an estimated probability
  2) Recommend words that would increase the estimated probability by the largest amount

Notes:
  Not all words are on Wordle's 'valid' list and won't work.
  
Usage:
  1) Run program
  2) Enter length of word to guess
  3) Receive suggestions
  4) Enter your guess word
  5) Enter the results
      x = wrong letter
      ? = right letter, wrong spot
      1 = right letter, right spot
  6) Repeat through step 3 until solved
