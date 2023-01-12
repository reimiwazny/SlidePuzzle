import PySimpleGUI as sg
from random import choice

sg.theme('DarkPurple7')

active_color = '#B1B7C5'
disabled_color = '#191930'

def initialize_tiles():
	tiles = [	[sg.Button('1', size=(6,2), pad=0, key=(3,0)), sg.Button('2', size=(6,2), pad=0, key=(3,1)), sg.Button('3', size=(6,2), pad=0, key=(3,2)), sg.Button('4', size=(6,2), pad=0, key=(3,3))],
				[sg.Button('5', size=(6,2), pad=0, key=(2,0)), sg.Button('6', size=(6,2), pad=0, key=(2,1)), sg.Button('7', size=(6,2), pad=0, key=(2,2)), sg.Button('8', size=(6,2), pad=0, key=(2,3))],
				[sg.Button('9', size=(6,2), pad=0, key=(1,0)), sg.Button('10', size=(6,2), pad=0, key=(1,1)), sg.Button('11', size=(6,2), pad=0, key=(1,2)), sg.Button('12', size=(6,2), pad=0, key=(1,3))],
				[sg.Button('13', size=(6,2), pad=0, key=(0,0)), sg.Button('14', size=(6,2), pad=0, key=(0,1)), sg.Button('15', size=(6,2), pad=0, key=(0,2)), sg.Button(' ', size=(6,2), pad=0, key=(0,3), button_color = ('#191930'))]]
	ids = [x.key for row in tiles for x in row]
	return tiles, ids

def randomize_tiles(button_ids, empty_key):
	for x in range(100):
		below = (empty_key[0], empty_key[1]-1)
		above = (empty_key[0], empty_key[1]+1)
		left = (empty_key[0]-1, empty_key[1])
		right = (empty_key[0]+1, empty_key[1])
		adjacent = [x for x in [below, above, left, right] if all(elem >= 0 and elem <= 3 for elem in x)]
		target = choice(adjacent)
		targ_num = window[target].get_text()
		window[target].update(text = ' ', button_color = disabled_color)
		window[empty_key].update(text=targ_num, button_color=active_color)
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
			if window[block].ButtonColor[1] == disabled_color:
				valid = True
				empty_key = block
	if valid:
		window[empty_key].update(button_color = active_color)
		window[empty_key].update(block_num)
		window[block_key].update(button_color = disabled_color)
		window[block_key].update(' ')

def check_win(button_ids):
	for x in range(15):
		target = x + 1
		cur_button = button_ids[x]
		if window[cur_button].get_text() == ' ':
			return False
		if int(window[cur_button].get_text()) != target:
			return False
	return True

tiles_grid, button_ids = initialize_tiles()


window = sg.Window('Slide Puzzle', tiles_grid, font=('any', 20), finalize=True)
randomize_tiles(button_ids, button_ids[-1])

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		break
	if event in button_ids and window[event].get_text() != ' ':
		slide_tile(event)
		if check_win(button_ids):
			sg.popup_ok("You win!", font=('any', 20))
			randomize_tiles(button_ids, button_ids[-1])	

window.close()