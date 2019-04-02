import curses

def main(stdscr):
    # ----- INIT -----
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(1)

    # ----- PRINT -----
    text = "Hello world"
    stdscr.addstr(1, 0, text + "\n")
    stdscr.refresh()

    # ----- MAIN LOOP ------
    while 1:
        c = stdscr.getch()
        if c == ord('q'):
            break
        if c == 8 or c == 127 or c == curses.KEY_BACKSPACE:
            stdscr.addstr("\b \b")
        else:
            stdscr.addch(c)

    # ----- RESET TERMINAL -----
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(1)
    curses.endwin()


curses.wrapper(main)