#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import curses
from curses import textpad

def food_create(snake, game_scene):
    ''' a function for create random foods on the game screen
    using random module to create food's y and x axis from game_scene 
    variable which is defined in main function '''
    
    food = None
    while food is None:
        food = [random.randint(game_scene[0][0]+1,game_scene[1][0]-1),
                random.randint(game_scene[0][1]+1,game_scene[1][1]-1)]
        if food in snake:
            food = None
    return food

def display_score(stdscr, score):
    ''' a simple function for displayin score above game screen
    on the terminal 
    sh: screen height
    sw: screen width '''
    
    sh, sw = stdscr.getmaxyx()
    stdscr.addstr(sh//2-11, sw//2-len("Score"), "Score : {}".format(score))
    stdscr.refresh()
    
menu = ["Play","Skin","Exit"]

def print_menu(stdscr, selected_index):
    ''' a function for display centered menu with black and white color pair'''
    
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for index, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + index
        if index == selected_index:
           stdscr.attron(curses.color_pair(1))  
           stdscr.addstr(y,x,row)
           stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y,x,row)
 
    stdscr.refresh()
    

def main(stdscr):
    ''' main function written for two purposes:
        1 - navigating up and down the menu and changing 
            the color of the option you are on
        2 - play game under the menu options with conditions '''
    
    # initialized values and settings
    current_index = 0
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    print_menu(stdscr, current_index)
    
    while True:
        
        key = stdscr.getch()
        stdscr.clear()
        
        # define up and down navigation in menu
        if key == curses.KEY_UP and current_index > 0:
            current_index -= 1
        elif key == curses.KEY_DOWN and current_index < len(menu)-1:
            current_index += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            
            # Play option on the menu 
            if current_index == 0:
                # initial settings for the non_blocked .getch() function
                stdscr.nodelay(1)  
                stdscr.timeout(150) 
                
                # create a game scene
                sh, sw = stdscr.getmaxyx()
                textpad.rectangle(stdscr, 3, 3, sh-3, sw-3)
                stdscr.refresh()
                stdscr.getch()
                
                # define the game scene
                game_scene = [[3,3],[sh-3, sw-3]]
                
                # initialize the snake
                snake = [[sh//2,sw//2+1],[sh//2,sw//2],[sh//2,sw//2-1]]
                direction = curses.KEY_RIGHT
                
                # create the food
                food = food_create(snake, game_scene)
                stdscr.addstr(food[0],food[1], "#")
                
                # draw the snake with defined coordinates
                for y,x in snake:
                    stdscr.addstr(y,x,"0")
                
                # display the score
                score = 0
                display_score(stdscr, score)
                
                # define directions
                directions = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]
                opposites = {curses.KEY_RIGHT: curses.KEY_LEFT, curses.KEY_LEFT: curses.KEY_RIGHT,
            		   curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP}
                
                while True:
                    
                    key = stdscr.getch()
                    head = snake[0]
                    
                    # define new direction with key input
                    if key in directions:
                        # if direction in opposites, snake can goes on opposite sides
                        if direction != opposites[key]: 
                           direction = key
                        
                    if direction == curses.KEY_RIGHT:
                        new_head = [head[0],head[1]+1]
                    elif direction == curses.KEY_LEFT:
                        new_head = [head[0],head[1]-1]
                    elif direction == curses.KEY_UP:
                        new_head = [head[0]-1,head[1]]
                    elif direction == curses.KEY_DOWN:
                        new_head = [head[0]+1,head[1]]
                        
                    # insert and print new head for snake's movement functionality
                    snake.insert(0, new_head) 
                    stdscr.addstr(new_head[0], new_head[1], "0") 
                    
                    # if snake's head on food
                    if snake[0] == food:
                        # increase the score and add new food
                        food = food_create(snake, game_scene)
                        stdscr.addstr(food[0],food[1], "#")
                        score += 1
                        display_score(stdscr,score)
                        stdscr.refresh()
                        
                    # else snake's head is not on food
                    else:
                       # update the snake and shift the tail
                       stdscr.addstr(snake[-1][0],snake[-1][1]," ")
                       snake.pop()
                    
                    # game over conditions 
                    if (snake[0][0] in (3, sh-3) or
                        snake[0][1] in (3, sw-3) or 
                        snake[0] in snake[1:]):
                        # display game over and break
                        over = "Game Over!"
                        stdscr.addstr(sh//2, sw//2 - len(over)//2, over)
                        stdscr.nodelay(0)
                        stdscr.getch()
                        break
                        
                    stdscr.refresh()
            
            stdscr.refresh()
            stdscr.getch()
            
            # Skin option on the menu
            if current_index == 1:
                skins_input = "Press a character key to set a new skin then press enter"
                stdscr.refresh()
                legits = '''            Available skins
                          ---------------------------
                          +"!'^+%&/()=?*-_ 1234567890
                          ASDFGHJKLQWERTYUIOPZXCVBNM
                          asdfghjkliqwertyuopzxcvbnm'''       
                h, w = stdscr.getmaxyx()
                stdscr.addstr(h//2, w//2-len(skins_input)//2, skins_input)
                stdscr.addstr(h//2+3, w//2-20, legits)
                stdscr.refresh()
                # Get skin character as str for change
                skin = stdscr.getstr()
                stdscr.clear()
                # if the skin is a character, play the game using that character as the skin
                if len(skin) == 1:
                   stdscr.clear()
                # else give error and exit the game
                else:
                       error_message = "Please choose available and just one character"
                       stdscr.addstr(h//2, w//2-len(error_message)//2,error_message)
                       stdscr.refresh()
                       time.sleep(3)
                       stdscr.clear()
                       break
                       stdscr.refresh()
                stdscr.refresh()
                # initial settings for the curs and .getch() function
                curses.curs_set(0)
                stdscr.nodelay(1)  
                stdscr.timeout(150) 
                
                # initialize the terminal screen for create a game scene
                sh, sw = stdscr.getmaxyx()
                textpad.rectangle(stdscr, 3, 3, sh-3, sw-3)
                stdscr.refresh()
                stdscr.getch()
                
                # define the game scene
                game_scene = [[3,3],[sh-3, sw-3]]
                
                # initialize the snake
                snake = [[sh//2,sw//2+1],[sh//2,sw//2],[sh//2,sw//2-1]]
                direction = curses.KEY_RIGHT
                
                # create the food
                food = food_create(snake, game_scene)
                stdscr.addstr(food[0],food[1], "#")
                
                # draw the snake with defined coordinates and choosed skin
                for y,x in snake:
                    stdscr.addstr(y,x,skin)
                
                # display the score
                score = 0
                display_score(stdscr, score)
                
                # define directions
                directions = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]
                opposites = {curses.KEY_RIGHT: curses.KEY_LEFT, curses.KEY_LEFT: curses.KEY_RIGHT,
            		   curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP}
                
                while True:
                    
                    key = stdscr.getch()
                    head = snake[0]
                    
                    # define new direction with key input
                    if key in directions:
                        # if direction in opposites, snake can goes on opposite sides
                        if direction != opposites[key]: 
                           direction = key
                        
                    if direction == curses.KEY_RIGHT:
                        new_head = [head[0],head[1]+1]
                    elif direction == curses.KEY_LEFT:
                        new_head = [head[0],head[1]-1]
                    elif direction == curses.KEY_UP:
                        new_head = [head[0]-1,head[1]]
                    elif direction == curses.KEY_DOWN:
                        new_head = [head[0]+1,head[1]]
                        
                    # insert and print new head for snake's movement functionality
                    snake.insert(0, new_head) 
                    stdscr.addstr(new_head[0], new_head[1],skin) 
                    
                    # if snake's head on food
                    if snake[0] == food:
                        # increase the score and add new food
                        food = food_create(snake, game_scene)
                        stdscr.addstr(food[0],food[1], "#")
                        score += 1
                        display_score(stdscr,score)
                        stdscr.refresh()
                        
                    # else snake's head is not on food
                    else:
                       # update the snake and shift the tail
                       stdscr.addstr(snake[-1][0],snake[-1][1]," ")
                       snake.pop()
                    
                    # game over conditions 
                    if (snake[0][0] in (3, sh-3) or
                        snake[0][1] in (3, sw-3) or 
                        snake[0] in snake[1:]):
                        # display game over and break
                        over = "Game Over!"
                        stdscr.addstr(sh//2, sw//2 - len(over)//2, over)
                        stdscr.nodelay(0)
                        stdscr.getch()
                        break
                        
                    stdscr.refresh()
            
            stdscr.refresh()
            stdscr.getch()
            # Exit option on the menu
            if current_index == len(menu)-1:
               break
        print_menu(stdscr, current_index)
        stdscr.refresh()
curses.wrapper(main)
