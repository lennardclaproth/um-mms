import curses


class Input:

    @staticmethod
    def get_component(input_label, area):
        curses.curs_set(2)
        curses.echo(True)
        input = curses.newwin(
            area['height'], area['width'], area['y'], area['x'])
        input.addstr(0, 0, input_label)
        input.refresh()
        value = input.getstr(area['input_y'], 0, 100)
        curses.curs_set(0)
        curses.echo(False)
        return value
