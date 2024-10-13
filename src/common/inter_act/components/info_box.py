import curses
import textwrap


class InfoBox:

    @staticmethod
    def get_component(size, text, grid_cols, model, text_color=curses.COLOR_BLUE):
        # Calculate max width for the content
        max_width = (size[1] // grid_cols) * 4

        wrapped_content = []
        max_line_length = 0

        for key, value in model.items():
            lines = textwrap.wrap(f"{key}: {value}", max_width)
            wrapped_content.extend(lines)
            max_line_length = max(max_line_length, max(len(line)
                                  for line in lines))

        title_size_y = len(wrapped_content) + 2
        title_size_x = max_line_length + 4

        middle_screen_x = (size[1] // 2) - (title_size_x // 2)

        title_box = curses.newwin(
            title_size_y, title_size_x, 3, middle_screen_x)
        title_box.box()

        curses.init_pair(1, text_color, curses.COLOR_BLACK)

        for i, line in enumerate(wrapped_content, start=1):
            title_box.addstr(i, 2, line, curses.color_pair(1)
                             )

        return title_box
