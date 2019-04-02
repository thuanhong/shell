#!/usr/bin/env python3
import curses
from time import sleep
import sys


def debug(string):
    f = open('tem', 'w')
    f.write(string)
    f.close()


def get_input(window):
    key = ''
    current = list(window.getyx())
    defaul_pos = current[1]
    char = window.getch()
    while True:
        if char == curses.KEY_RIGHT:
            if current[1] <= defaul_pos + len(key) -1:
                current[1] += 1
                window.move(current[0], current[1])
        elif char == curses.KEY_LEFT:
            if current[1] > defaul_pos:
                current[1] -= 1
                window.move(current[0], current[1])
        elif char == curses.KEY_BACKSPACE:
            if current[1] > defaul_pos:
                key = key[:current[1]-defaul_pos-1] + key[current[1]-defaul_pos:]
                debug(key)
                window.delch(current[0], current[1] - 1)
                current[1] -= 1
        elif char == ord('\n'):
            window.move(current[0], defaul_pos + len(key))
            return key
        else:
            key = key[:current[1]-defaul_pos] + chr(char) + key[current[1]-defaul_pos:]
            window.insstr(current[0], current[1], chr(char))
            current[1] += 1
            window.move(current[0], current[1])
        char = window.getch()
    


def main(window):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    while True:
        window.addstr("hthuan@intek-sh$ ", curses.A_BOLD + curses.color_pair(1))
        temp = get_input(window)
        window.addstr('\n' + temp + '\n')
        
    window.refresh()
    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(main)