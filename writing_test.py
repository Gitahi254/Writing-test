# This gives you a writing test and calculates your typing speed in seconds.
#It gives you a sample text for you to write through as fast as you can and gives the response in real time.
#The words you get correct will be in green and when you type a word wrongly it will automatically turn to the color red

#LESS GO!!
 

import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!\n")
    stdscr.addstr("Press any key to begin!")
    stdscr.refresh()
    stdscr.getch()  # Use getch() to get single characters

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target + '\n')  # Add target text with newline
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i] if i < len(target) else ' '  # Handle end of string
        color = curses.color_pair(1) if char == correct_char else curses.color_pair(2)
        stdscr.addstr(0, i, char, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    test_results = []  # List to store results of each sentence test
    stdscr.nodelay(True)

    total_characters = 0
    total_time = 0

    while True:
        target_text = load_text()
        current_text = []
        wpm = 0
        start_time = time.time()

        while True:
            time_elapsed = max(time.time() - start_time, 1)
            wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

            stdscr.clear()
            display_text(stdscr, target_text, current_text, wpm)
            stdscr.refresh()

            if "".join(current_text) == target_text:
                characters_typed = len(current_text)
                test_results.append((target_text, characters_typed, wpm))  # Store result
                total_characters += characters_typed
                total_time += time_elapsed
                break

            try:
                key = stdscr.getch()  # Use getch() to get single characters
            except:
                continue

            if key == 27:  # Check for ESC key press
                break

            if key in (curses.KEY_BACKSPACE, curses.KEY_DC, 127):  # Use curses.KEY_DC for delete key
                if current_text:
                    current_text.pop()
            elif key >= 32 and key <= 126:  # Check if key is printable ASCII character
                current_text.append(chr(key))  # Append character to current text list

        stdscr.clear()
        stdscr.addstr("Test results:\n")
        total_wpm = 0
        for i, result in enumerate(test_results, start=1):
            stdscr.addstr(f"\nTest {i}: Sentence: {result[0]} | Characters Typed: {result[1]} | WPM: {result[2]}")
            total_wpm += result[2]

        total_wpm = round((total_characters / (total_time / 60)) / 5)
        stdscr.addstr(f"\n\nTotal Score: Characters Typed: {total_characters} | Total WPM: {total_wpm}")
        stdscr.addstr("\n\nPress any key to continue to the next test, or press ESC to exit...")
        key = stdscr.getch()
        if key == 27:
            break

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)

wrapper(main)

