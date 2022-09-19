import json 

EXAMPLE1 = [[0,3,4,6,7,8,9,1,2],
                [6,7,2,1,9,5,3,4,8],
                [1,0,8,3,4,2,5,6,7],
                [8,0,9,7,6,1,4,2,3],
                [4,2,6,8,5,3,7,9,1],
                [7,1,3,9,2,4,8,5,6],
                [9,6,1,5,3,7,2,8,4],
                [2,8,7,4,1,9,6,3,5],
                [3,4,5,2,8,6,1,7,9]]

EXAMPLE2 = [[0,0,3,0,2,0,6,0,0],
                [9,0,0,3,0,5,0,0,1],
                [0,0,1,8,0,6,4,0,0],
                [0,0,8,1,0,2,9,0,0],
                [7,0,0,0,0,0,0,0,8],
                [0,0,6,7,0,8,2,0,0],
                [0,0,2,6,0,9,5,0,0],
                [8,0,0,2,0,3,0,0,9],
                [0,0,5,0,1,0,3,0,0]]

puzzles = {1 : EXAMPLE1, 2 : EXAMPLE2}

def write_puzzle(puzzles):
    with open('puzzle.json', 'w+') as f:
        json.dump(puzzles, f)


def read_puzzle():
    with open('puzzle.json', 'r') as f:
        puzzles = json.load(f)
    return puzzles


# write_puzzle(puzzles)

PUZZLES = read_puzzle()