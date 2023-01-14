import PySimpleGUI as sg
from random import choice

sg.theme('DarkPurple7')

ACTIVE_COLOR = '#B1B7C5'
DISABLED_COLOR = '#191930'
FONT_SET = ('Arial', 20)
shuffle_factor = 100
total_moves = 0
use_limit = False
move_limit = 0

def initialize_tiles(mode='init'):
	if mode == 'init':
		tiles = [	[sg.Button('1', size=(6,2), pad=0, key=(3,0)), sg.Button('2', size=(6,2), pad=0, key=(3,1)), sg.Button('3', size=(6,2), pad=0, key=(3,2)), sg.Button('4', size=(6,2), pad=0, key=(3,3))],
					[sg.Button('5', size=(6,2), pad=0, key=(2,0)), sg.Button('6', size=(6,2), pad=0, key=(2,1)), sg.Button('7', size=(6,2), pad=0, key=(2,2)), sg.Button('8', size=(6,2), pad=0, key=(2,3))],
					[sg.Button('9', size=(6,2), pad=0, key=(1,0)), sg.Button('10', size=(6,2), pad=0, key=(1,1)), sg.Button('11', size=(6,2), pad=0, key=(1,2)), sg.Button('12', size=(6,2), pad=0, key=(1,3))],
					[sg.Button('13', size=(6,2), pad=0, key=(0,0)), sg.Button('14', size=(6,2), pad=0, key=(0,1)), sg.Button('15', size=(6,2), pad=0, key=(0,2)), sg.Button(' ', size=(6,2), pad=0, key=(0,3), button_color = ('#191930'))]]
		ids = [x.key for row in tiles for x in row]
		return tiles, ids
	else:
		label = 1
		for button in button_ids:
			if label < 16:
				window[button].update(text=label, button_color=ACTIVE_COLOR)
			else:
				window[button].update(text = ' ', button_color=DISABLED_COLOR)
			label +=1

def randomize_tiles(button_ids, empty_key, shuffle_factor):
	for x in range(shuffle_factor):
		below = (empty_key[0], empty_key[1]-1)
		above = (empty_key[0], empty_key[1]+1)
		left = (empty_key[0]-1, empty_key[1])
		right = (empty_key[0]+1, empty_key[1])
		adjacent = [x for x in [below, above, left, right] if all(elem >= 0 and elem <= 3 for elem in x)]
		target = choice(adjacent)
		targ_num = window[target].get_text()
		window[target].update(text = ' ', button_color = DISABLED_COLOR)
		window[empty_key].update(text=targ_num, button_color=ACTIVE_COLOR)
		empty_key = target

def slide_tile(block_key):
	valid = False
	block_num = window[block_key].get_text()
	empty_key = None
	below = (block_key[0], block_key[1]-1)
	above = (block_key[0], block_key[1]+1)
	left = (block_key[0]-1, block_key[1])
	right = (block_key[0]+1, block_key[1])
	adjacent = [left, right, above, below]
	for block in adjacent:
		if all(elem >= 0 and elem <= 3 for elem in block):
			if window[block].ButtonColor[1] == DISABLED_COLOR:
				valid = True
				empty_key = block
	if valid:
		window[empty_key].update(button_color = ACTIVE_COLOR)
		window[empty_key].update(block_num)
		window[block_key].update(button_color = DISABLED_COLOR)
		window[block_key].update(' ')
	return valid

def check_win(button_ids):
	for x in range(15):
		target = x + 1
		cur_button = button_ids[x]
		if window[cur_button].get_text() == ' ':
			return False
		if int(window[cur_button].get_text()) != target:
			return False
	return True

def new_game_menu(font_set=FONT_SET):
	s_factor_tooltip = 'How many \'steps\' the game will take when randomizing the puzzle.\nA low number might make it too easy.\nMinimum: 1 Maximum: 1000'
	limit_tooltip = 'Check this if you want to limit how many moves you have to solve the puzzle.'
	limit_num_tooltip = 'The maximum number of moves to solve the puzzle(Only if \'Use Move Limit\' is enabled).\nMinimum: 1 Maximum: 1000'

	layout = [	[sg.Push(), sg.Text('Game Setup'), sg.Push()],
					[sg.Text('Shuffle Factor:'), sg.Input(size=10, default_text='100', tooltip=s_factor_tooltip, key='SHUFF', enable_events=True)],
					[sg.Text('Use Move Limit?'), sg.Checkbox(text=None,tooltip=limit_tooltip, key='LIMIT')],
					[sg.Text('Max Moves:'), sg.Input(size=10, default_text='100', tooltip=limit_num_tooltip, key='MAXMOVES', enable_events=True)],
					[sg.Button('Play!', key='STARTGAME'), sg.Button('Cancel', key='BACK')]	]

	window = sg.Window(title='Game Setup', layout=layout, font=font_set, modal=True)

	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, 'BACK'):
			window.close()
			return 100, False, 100, False
		if event == 'SHUFF':
			if not values['SHUFF'].isnumeric():
				window['SHUFF'].update(''.join(list(x for x in values['SHUFF'] if x.isnumeric())))
			if window['SHUFF'].get() != '':
				if int(window['SHUFF'].get()) < 1:
					window['SHUFF'].update(1)
				elif int(window['SHUFF'].get()) > 1000:
					window['SHUFF'].update(1000)

		if event == 'MAXMOVES':
			if not values['MAXMOVES'].isnumeric():
				window['MAXMOVES'].update(''.join(list(x for x in values['MAXMOVES'] if x.isnumeric())))
			if window['MAXMOVES'].get() != '':
				if int(window['MAXMOVES'].get()) < 1:
					window['MAXMOVES'].update(1)
				elif int(window['MAXMOVES'].get()) > 1000:
					window['MAXMOVES'].update(1000)

		if event == 'STARTGAME':
			window.close()
			try:
				return int(values['SHUFF']), values['LIMIT'], int(values['MAXMOVES']), True
			except ValueError:
				return 100, False, 100, False
	window.close()

tiles_grid, button_ids = initialize_tiles()

status_window = [	[sg.Text('Total Moves Made:'), sg.Text(0, key='MOVES') ],
							[sg.Button('New Game', key='NEWGAME'), sg.Button('About', key='ABOUT')]	]

layout = [	[sg.Frame(title=None, layout=tiles_grid, border_width=0)], 
				[sg.Frame(title=None, layout=status_window, border_width=0)]	]


window = sg.Window('Slide Puzzle', layout, font=FONT_SET, finalize=True, element_justification='center')
randomize_tiles(button_ids, button_ids[-1], shuffle_factor)

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		break
	if event in button_ids and window[event].get_text() != ' ':
		if slide_tile(event):
			total_moves += 1
			window['MOVES'].update(total_moves)
		if use_limit:
			if total_moves > move_limit:
				sg.popup_ok('Out of moves!', font=FONT_SET)
				initialize_tiles('new')
				total_moves = 0
				window['MOVES'].update(total_moves)
				randomize_tiles(button_ids, button_ids[-1], shuffle_factor)
		if check_win(button_ids):
			sg.popup_ok("You win!", font=FONT_SET)
			initialize_tiles('new')
			total_moves = 0
			window['MOVES'].update(total_moves)
			randomize_tiles(button_ids, button_ids[-1], shuffle_factor)	
	if event == 'NEWGAME':
		shuffle_factor, use_limit, move_limit, is_new = new_game_menu()
		if is_new:
			initialize_tiles('new')
			randomize_tiles(button_ids, button_ids[-1], shuffle_factor)
			total_moves = 0
			window['MOVES'].update(total_moves)


window.close()