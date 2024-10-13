import curses


class TextBox():

    @staticmethod
    def get_component(size, extra_padding, text, y=0):
        title_size_y = 3
        title_size_x = len(text)+extra_padding
        middle_screen = int(size[1]/2)-int(title_size_x/2)-1
        title_box = curses.newwin(title_size_y, title_size_x, y, middle_screen)
        title_box.box()
        title_box.addstr(1, 1, text)
        return title_box
