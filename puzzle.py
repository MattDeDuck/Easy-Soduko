from bs4 import BeautifulSoup
import requests

def get_Puzzle():

    req = requests.get("http://www.menneske.no/sudoku/eng/random.html?diff=3")
    c = req.content
    soup = BeautifulSoup(c, 'html.parser')

    grid_txt = soup.find_all('div', {'class':'grid'})[0].text
    puzzle_no = grid_txt[str.find(grid_txt, 'Showing puzzle')+23:str.find(grid_txt, 'Puzzletype')]

    puzzle = []

    rows = soup.findAll('tr', {'class': "grid"})

    for row in rows:
        cols = row.find_all('td')
        for col in cols:
            txt = col.text
            puzzle.append(0) if txt == '\xa0' else puzzle.append(txt)

    puzzleNew = [puzzle[i:i+9] for i in range(0,len(puzzle),9)]

    spaces = sum([i.count(0) for i in puzzleNew])

    return puzzleNew, puzzle_no, spaces

def get_Puzzle_solution(number):
    
    req = requests.get(f"http://www.menneske.no/sudoku/eng/solution.html?number={number}")
    c = req.content
    soup = BeautifulSoup(c, 'html.parser')

    solution_board = []
    rows = soup.findAll('tr', {'class': "grid"})

    for row in rows:
        cols = row.find_all('td')
        for col in cols:
            txt = col.text
            solution_board.append(txt)

    solution = [solution_board[i:i+9] for i in range(0,len(solution_board),9)]
    
    return solution