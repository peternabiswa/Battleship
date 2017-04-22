#!/usr/bin/env python
# -*- coding: utf-8 -*-
# indent scheme: 2 tab characters
'''
	Welcome to:
		██████╗  █████╗ ████████╗████████╗██╗     ███████╗███████╗██╗  ██╗██╗██████╗ 
		██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝██╔════╝██║  ██║██║██╔══██╗
		██████╔╝███████║   ██║      ██║   ██║     █████╗  ███████╗███████║██║██████╔╝
		██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝  ╚════██║██╔══██║██║██╔═══╝ 
		██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗███████║██║  ██║██║██║     
		╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝      
	Authors:    
		Peter Nabiswa
		Timothy Bassler
	Course:
		Fall 2015
		CSCI 220
		Programming Languages
	Assingment:
		Battleship (Python)
	Due Date:
		Preliminary: Fri 09/25/15
		Final:       Fri 10/02/15
	Project Description:
		This program will run a console-based version of the board game
		battleship.  The user will play against the computer, having the
		option to either manually select their ships' placement or have
		the ships auto-deployed.  The computer will be semi-intelligent,
		tracking hits until they generate sinks, and otherwise firing
		randomly on the board.  Each player has 5 ships: a carrier that
		is 5 spaces long, a battleship that is 4 spaces long, a destroyer
		and a submarine that are 3 spaces long each, and a patrol boat
		that is 2 spaces long.  The game is over when one player has had
		every ship sunk, making the other player the winner.
'''

import os
import random
from random import randint
import time

# MAIN DATA POOL

debugMode = None

#Computer data
                # 1(0)  2(1)  3(2)  4(3)  5(4)  6(5)  7(6)  8(7)  9(8)  10(9) Control(10)    X-axis: position(index)
computerBoard = [[" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # A, 0
                 [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # B, 1
                 [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # C, 2
                 [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # D, 3
                 [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # E, 4
                 [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # F, 5
                 [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # G, 6
                 [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # H, 7
                 [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # I, 8
                 [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # J, 9
                 [None, None, None, None, None, None, None, None, None, None, None]] # Control, 10
			                                                                         # Y-axis: position(index)
                # Carrier, Battleship, Destroyer, Submarine, PatrolBoat
computerShips = ( 5,       4,          3,         3,         2)
computerHasHit = None

#Player data
             #  1(0)  2(1)  3(2)  4(3)  5(4)  6(5)  7(6)  8(7)  9(8)  10(9) Control(10)    X-axis: position(index)
playerBoard = [[" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # A, 0
               [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # B, 1
               [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # C, 2
               [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # D, 3
               [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # E, 4
               [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # F, 5
               [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # G, 6
               [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # H, 7
               [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # I, 8
               [" ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  " ",  None], # J, 9
               [None, None, None, None, None, None, None, None, None, None, None]] # Control, 10
			                                                                       # Y-axis: position(index)
              # Carrier, Battleship, Destroyer, Submarine, PatrolBoat
playerShips = ( 5,       4,          3,         3,         2)

# END MAIN DATA POOL

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: cls()
#
#   Pre:  None
#
#   Post: The screen has been 'cleared'
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cls():
		os.system('cls' if os.name == 'nt' else 'clear')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: ResetBoards()
#
#   Pre:  Functionality of main data pool has not been revised
#
#   Post: Main data pool has been reset
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ResetBoards():
		for x in range(0, 10): # for all of the values besides the control row
				for y in range(0, 10): # for all of the values besides the control column
						playerBoard[x][y] = " " # reset back to empty
						computerBoard[x][y] = " "
		playerShips = (5, 4, 3, 3, 2) # reset ship hit counters
		computerShips = (5, 4, 3, 3, 2)
		computerHasHit = None # reset the computer's hit tracker

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: validateCoords()
#
#   Pre:  None
#
#   Post: Validated the given coorodinates: x = 1-10, y = A-J (case insensitive)
#             If invalid, returned the original values, followed with None
#             If valid, returned the index equivilants, followed with True
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def validateCoords(x, y):
		try: # attempt to parse x into an int
				tempX = int(x)
		except ValueError: # if it failed, return invalid
				return x, y, None
				
		if 1 <= tempX <= 10: # if x is within acceptable range
				validYValues = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
				for value in validYValues: # for each valid value for y
						if value == y.lower(): # if this value is what y is
								x = tempX - 1 # update x with the index it references
								y = SwitchYCoords(y.lower()) # convert y to the index it references
								return x, y, True # and return valid
				return x, y, None # none of the valid y values returned, therefore invalid
		else: # if x is not within acceptable range, return invalid
				return x, y, None
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: ValidatePosition()
#
#   Pre:  board is a 2 dimentional list 11x11 large, with the last column and
#         last row being all None values and the remainder all single spaces
#         ship is an integer number identifying the length of the ship
#         x and y are coordinates (0-9) on the board where the ship is starting
#         angle is 0 (horizontal) or 1 (vertical), identifying the angle of the ship
#
#   Post: Returned True if the ship could be placed in the given location
#         Returned None if the ship could NOT be placed there (off board/overlap)
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ValidatePosition(board, ship, x, y, angle):
		if ship != 0: # if the ship's length has not been checked already
				if board[y][x] == " ": # if the given position is empty
						if angle == 0: # if the angle is horizontal
								x += 1 # increment the horizontal position
						else: # if the angle is vertical
								y += 1 # increment the vertical position
						return ValidatePosition(board, (ship-1), x, y, angle) # recursively loop for the rest of the ship
				else: # if the given position is not empty (another ship is there or off the map)
						return None # return invalid
		else: # if the whole ship has been validated already
				return True # return valid

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: PlaceShip()
#
#   Pre:  board is a 2 dimentional list 11x11 large, with the last column and
#         last row being all None values and the remainder a combination of
#         single spaces and other single characters
#         ship is an integer number identifying the length of the ship
#         x and y are coordinates (0-9) on the board where the ship is starting
#         angle is 0 (horizontal) or 1 (vertical), identifying the angle of the ship
#         IMPORTANT: ship placement MUST have been validated already using ValidatePosition()
#
#   Post: The ship has been placed, returned the updated board
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def PlaceShip(board, shipType, ship, x, y, angle):
		if ship != 0: # if the whole ship has not yet been placed
				board[y][x] = shipType # assign this position to be part of the ship
				if angle == 0: # if the angle is horizontal
						x += 1 # increment the x axis
				else: # if the angle is vertical
						y += 1 # update the y axis
				PlaceShip(board, shipType, (ship-1), x, y, angle) # recursively loop until the ship has been placed

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: CoordGen()
#
#   Pre:  None
#
#   Post: returned a pair of random numbers between 0 and 9 inclusive
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CoordGen():
		x = randint(0, 9)
		y = randint(0, 9)
		return x, y

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: SwitchShips()
#
#   Pre:  x is a number between 0 and 4 inclusive
#
#   Post: returned the respective ship character for the given number:
#         0 = "C" (Carrier)
#         1 = "B" (Battleship)
#         2 = "D" (Destroyer)
#         3 = "S" (Submarine)
#         4 = "P" (Patrol Boat)
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SwitchShips(x):
		return {
				0: "C",
				1: "B",
				2: "D",
				3: "S",
				4: "P",
		}[x]
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: SwitchShipNames()
#
#   Pre:  x is a number between 0 and 4 inclusive
#
#   Post: returned the respective ship name for the given number:
#         0 = "Carrier"
#         1 = "Battleship"
#         2 = "Destroyer"
#         3 = "Submarine"
#         4 = "Patrol Boat"
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SwitchShipNames(x):
		return {
				0: "Carrier",
				1: "Battleship",
				2: "Destroyer",
				3: "Submarine",
				4: "Patrol Boat",
		}[x]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: SwitchYCoords()
#
#   Pre:  y is a lowercase character between 'a' and 'j' inclusive
#
#   Post: returned the respective index value for the given coordinate:
#         'a' = 0
#         'b' = 1
#         'c' = 2
#         'd' = 3
#         'e' = 4
#         'f' = 5
#         'g' = 6
#         'h' = 7
#         'i' = 8
#         'j' = 9
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SwitchYCoords(y):
		return {
				'a': 0,
				'b': 1,
				'c': 2,
				'd': 3,
				'e': 4,
				'f': 5,
				'g': 6,
				'h': 7,
				'i': 8,
				'j': 9,
		}[y]
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: AutoDeploy()
#
#   Pre:  board is a 2 dimentional list 11x11 large, with the last column and
#         last row being all None values and the remainder all single spaces
#         ships is a list of the length of each ship, eg: (5, 4, 3, 3, 2)
#
#   Post: All ships have been automatically deployed on the board
#         The updated board has been returned
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def AutoDeploy(board, ships):
		shipNumber = 0 # tracked in the loop to identify the ship type
		for ship in ships: # for each ship
				shipType = SwitchShips(shipNumber) # store the character value of this ship
				canPlace = None
				while canPlace == None: # while ValidatePosition has not returned True
						x, y = CoordGen() # generate new coordinates
						angle = randint(0, 1) # random angle value
						canPlace = ValidatePosition(board, ship, x, y, angle) # check if the ship can go here
				PlaceShip(board, shipType, ship, x, y, angle) # once a valid position has been found, place it
				shipNumber += 1 # keep track of which ship is next
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: ManualDeploy()
#
#   Pre:  board is a 2 dimentional list 11x11 large, with the last column and
#         last row being all None values and the remainder all single spaces
#         ships is a list of the length of each ship, eg: (5, 4, 3, 3, 2)
#
#   Post: All ships have been manually deployed on the board
#         The updated board has been returned
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ManualDeploy(board, ships):
		shipNumber = 0 # track which ship is currently being deployed
		for ship in ships: # for each ship
				shipType = SwitchShips(shipNumber) # store the character representing the ship
				shipName = SwitchShipNames(shipNumber) # store the name of the ship
				canPlace = None # loop variable
				while canPlace == None: # until a good ship placement has been given
						cls() # clear the screen
						PrintBoard(board) # print the board
						print "Where would you like to place your", shipName + "? (" + str(ship), "long)"
						print "Input format: Y-axis coordinate, X-axis coordinate, placement angle (v/h)"
						response = raw_input("Example: B, 2, v: ") # prompt the user for a position
						y, x, angle = response.split(", ", 2) # parse the input
						if angle.lower() == 'v' or angle.lower() == 'h': # make sure the angle is an acceptable value
								x, y, success = validateCoords(x, y) # validate the coordinates and store success state
								if success == True: # if the coords were valid
										if angle == 'h': # if horizontal
												angle = 0 # set to the horizontal value for PlaceShip
										else: # if vertical
												angle = 1 # set to the vertical value for PlaceShip
										canPlace = ValidatePosition(board, ship, x, y, angle) # validate the position
										if canPlace == None: # if placement was invalid
												print "Could not place the ship there.  Please select a different location." #complain
												raw_input('Press ENTER to continue...')
								else: # if the coords were invalid
										print "Invalid coordinates:", x, y #complain
										raw_input('Press ENTER to continue...')
						else: # if the angle was not a good value
								print "Invalid input:", response #complain
								raw_input('Press ENTER to continue...')
				PlaceShip(board, shipType, ship, x, y, angle) # everything checks out, place the ship
				shipNumber += 1 # increment the ship id for the next loop
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: PrintBoard()
#
#   Pre:  board is a 2 dimentional list 11x11 large, with the last column and
#         last row being all None values and the remainder a combination of
#         single spaces and other single characters
#
#   Post: board has been printed to the screen with row and column headers
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def PrintBoard(board):
		print "    1   2   3   4   5   6   7   8   9   10" # print column headers
		print "  - - - - - - - - - - - - - - - - - - - - -"
		yPos = "A" # value for row headers
		for y in board: # for each row in the board
				if y[0] != None: # if this isn't the last row
						print yPos, "|", # print row header
						yPos = chr(ord(yPos) + 1) # increment row header for next row
						for x in y: # for each element in the row
								if x != None: # if this isnt the last column
										print x, "|", # print the value without ending the line
								else: # if this is the last column
										print # end the line
						print "  - - - - - - - - - - - - - - - - - - - - -" # print the row seperator
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: WelcomeScreen()
#
#   Pre:  None
#
#   Post: The battleship game welcome screen text has been printed
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def WelcomeScreen():
		print "Welcome to . . ."
		print "                 ____        __  __  __          __    _  "
		print "                / __ )____ _/ /_/ /_/ /__  _____/ /_  (_)___  "
		print "               / __  / __ `/ __/ __/ / _ \\/ ___/ __ \\/ / __ \\  "
		print "              / /_/ / /_/ / /_/ /_/ /  __(__  ) / / / / /_/ /  "
		print "             /_____/\\__,_/\\__/\\__/_/\\___/____/_/ /_/_/ .___/  "
		print "                                                    /_/  "
		print
		print
		print "                                        # #  ( )  "
		print "                                     ___#_#___|__  "
		print "                                 _  |____________|  _  "
		print "                          _=====| | |            | | |==== _  "
		print "                    =====| |.---------------------------. | |====  "
		print "      <--------------------'   .  .  .  .  .  .  .  .   '--------------/  "
		print "        \                                                             /  "
		print "         \___________________________________________________________/  "
		print "     wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww  "
		print "   wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww  "
		print "      wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww  "
		print
		print
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: PrintVictory()
#
#   Pre:  None
#
#   Post: The victory screen has been printed
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def PrintVictory():
		print " __     __  ______   ______   ________  ______   _______   __      __ "
		print "/  |   /  |/      | /      \\ /        |/      \\ /       \\ /  \\    /  |"
		print "$$ |   $$ |$$$$$$/ /$$$$$$  |$$$$$$$$//$$$$$$  |$$$$$$$  |$$  \  /$$/ "
		print "$$ |   $$ |  $$ |  $$ |  $$/    $$ |  $$ |  $$ |$$ |__$$ | $$  \/$$/  "
		print "$$  \\ /$$/   $$ |  $$ |         $$ |  $$ |  $$ |$$    $$<   $$  $$/  "
		print " $$  /$$/    $$ |  $$ |   __    $$ |  $$ |  $$ |$$$$$$$  |   $$$$/  "
		print "  $$ $$/    _$$ |_ $$ \\__/  |   $$ |  $$ \__$$ |$$ |  $$ |    $$ |  "
		print "   $$$/    / $$   |$$    $$/    $$ |  $$    $$/ $$ |  $$ |    $$ |  "
		print "    $/     $$$$$$/  $$$$$$/     $$/    $$$$$$/  $$/   $$/     $$/  "
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: PrintDefeat()
#
#   Pre:  None
#
#   Post: The defeat screen has been printed
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def PrintDefeat():
		print " _______   _______  _______  _______     ___   .___________."
		print "|       \\ |   ____||   ____||   ____|   /   \\  |           |"
		print "|  .--.  ||  |__   |  |__   |  |__     /  ^  \\ `---|  |----`"
		print "|  |  |  ||   __|  |   __|  |   __|   /  /_\\  \\    |  |  "
		print "|  '--'  ||  |____ |  |     |  |____ /  _____  \\   |  |  "
		print "|_______/ |_______||__|     |_______/__/     \\__\\  |__|   =("
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: Menu()
#
#   Pre:  None
#
#   Post: The main menu has been displayed
#		      Returned True if the user wishes to play the game
#			  Returned None if the user wishes to quit the game
#			  If the user entered the debug code, debugging mode has been activated
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Menu():
		WelcomeScreen() # print the welcome screen
		response = raw_input("Type 'quit' to close the program, otherwise press ENTER to continue: ")
		
		if response.lower() == "quit":
				return None # return that the user wishes to quit
		
		global debugMode
		if response.lower() == "debugmode":
				debugMode = True # enable debug mode
		else:
				debugMode = None # ensure that debug mode is disabled
				
		return True # return that the user wishes to play the game

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: Deploy()
#
#   Pre:  None
#
#   Post: The user and computer boards have been populated
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Deploy():
		AutoDeploy(computerBoard, computerShips) # deploy the computer's ships
		if debugMode == True: # if the user enabled debug mode
				PrintBoard(computerBoard) # print out the computer's board
				print "Debugging: this is the computer's board... cheater"
				raw_input('Press ENTER to continue...')
				cls()
		PrintBoard(playerBoard) # print the user's board
		print "Would you like to manually deploy your ships, or have them auto-deployed?"
		validResponse = None # loop variable
		while validResponse == None: # loop until a valid response has been entered
				response = raw_input("Please select manual or automatic (m/a): ")
				if response.lower() == "m": # if manual deploy
						validResponse = True # note that it is valid
						ManualDeploy(playerBoard, playerShips) # enter the manual deploy sequence
						cls() # after the manual deploy, clear the screen
						PrintBoard(playerBoard) # print the user's board again
						raw_input('All ships deployed.  Press ENTER to start playing . . .') # and prompt the user to play
				elif response.lower() == "a": # if auto deploy
						validResponse = True # note that it is valid
						AutoDeploy(playerBoard, playerShips) # autodeploy the user's ship
						cls() # clear the screen
						PrintBoard(playerBoard) # print the user's board
						raw_input('Ships have been auomatically deployed.  Press ENTER to start playing . . .') # and prompt the user to play
				else: # if the user gave a bad response
					print "Invalid response" #complain

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: cls()
#
#   Pre:  The user and computer boards have been populate
#
#   Post: The game has been played
#		      Returned True if the user won
#             Returned None if the computer won
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Play():
		return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: main()
#
#   Pre:  None
#
#   Post: Battleship has been run
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
		while Menu(): # print the main menu
				cls()
				Deploy() # enter the deploy sequence
				if Play(): # enter the play sequence
						cls()
						PrintVictory() # if the user won, print the victory message
						raw_input('Press ENTER to continue...')
				else:
						cls()
						PrintDefeat() # if the user lost, print the defeat message
						raw_input('Press ENTER to continue...')
						
				ResetBoards()
				cls()
						
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Call to run the main program
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__=='__main__':
		random.seed(time.time())
		cls()
		main()
		raw_input('Press ENTER to continue...')
		cls()
