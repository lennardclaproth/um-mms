import curses
import curses.ascii


class Screen(object):
    UP = -1
    DOWN = 1

    def __init__(self, items, size, grid_col, width=50, should_truncate=False):
        self.window = None
        self.exception_inputs = []
        self.width = width
        self.should_truncate = should_truncate

        self.init_curses(size, grid_col)
        self.items = items

        self.max_lines = size[0]-8
        self.top = 0
        self.bottom = len(self.items)
        self.current = 0
        self.page = self.bottom // self.max_lines

    def init_curses(self, size, grid_col):
        """Setup the curses"""
        cols = int(size[1]//12) * grid_col
        self.window = curses.newwin(size[0]-8, self.width, 4, cols)
        self.window.keypad(True)

        self.current = curses.color_pair(3)

    def run(self):
        """Continue running the TUI until get interrupted"""
        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass
        finally:
            return self.current

    def input_stream(self):
        """Waiting an input and run a proper method according to type of input"""
        while True:
            self.display()

            ch = self.window.getch()
            if ch == curses.KEY_UP:
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif ch == curses.KEY_LEFT:
                self.paging(self.UP)
            elif ch == curses.KEY_RIGHT:
                self.paging(self.DOWN)
            elif ch == curses.ascii.LF:
                self.current = str(self.current + 1)
                break
            elif chr(ch) == 'm' or chr(ch) == 'q':
                self.current = chr(ch)
                break

            for input in self.exception_inputs:
                if chr(ch) == input:
                    self.current = chr(ch)
                    return

    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""
        # next cursor position after scrolling
        next_line = self.current + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        if (direction == self.DOWN) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom):
            self.top += direction
            return
        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        # Scroll down
        # next cursor position is above max lines, and absolute position of next cursor could not touch the bottom
        if (direction == self.DOWN) and (next_line < self.max_lines) and (self.top + next_line < self.bottom):
            self.current = next_line
            return

    def paging(self, direction):
        """Paging the window when pressing left/right arrow keys"""
        current_page = (self.top + self.current) // self.max_lines
        next_page = current_page + direction
        # The last page may have fewer items than max lines,
        # so we should adjust the current cursor position as maximum item count on last page
        if next_page == self.page:
            self.current = min(self.current, self.bottom % self.max_lines - 1)

        # Page up
        # if current page is not a first page, page up is possible
        # top position can not be negative, so if top position is going to be negative, we should set it as 0
        if (direction == self.UP) and (current_page > 0):
            self.top = max(0, self.top - self.max_lines)
            return
        # Page down
        # if current page is not a last page, page down is possible
        if (direction == self.DOWN) and (current_page < self.page):
            self.top += self.max_lines
            return

    def display(self):
        """Display the items on window"""
        self.window.erase()
        for idx, item in enumerate(self.items[self.top:self.top + self.max_lines]):
            # Truncate the text to fit within the window width
            if self.should_truncate == True:
                if len(item) > self.width:
                    item = item[:self.width - 4] + '...'
            # Highlight the current cursor line
            if idx == self.current:
                self.window.addstr(idx, 0, item,
                                   curses.color_pair(3))
            else:
                self.window.addstr(idx, 0, item,
                                   curses.color_pair(4))
        self.window.refresh()
