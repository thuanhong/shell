#!/usr/bin/env python3
import curses


def get_input(window):
    key = ''
    char = ""
    current_row = 0
    while char != ord('\n'):
        char = window.getch()
        key += chr(char)
        if char == curses.KEY_RIGHT and current_row > 0:
            current_row -= 1
            continue
        elif char == curses.KEY_LEFT and current_row < len(key)-1:
            current_row += 1
            continue

        window.echochar(chr(char))
    return key


def main(window):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    while True:
        window.addstr("hthuan@intek-sh$ ", curses.A_BOLD + curses.color_pair(1))
        get_input(window)
    window.refresh()
    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(main)