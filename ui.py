from prettytable import PrettyTable

class UI():
    colors = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'end': '\033[0m'
    }

    @staticmethod
    def color(string, color):
        return '{}{}{}'.format(UI.colors[color], string, UI.colors['end'])

    @staticmethod
    def print_table(header, items):
        x = PrettyTable()
        x._max_width = {'annotation': 60, 'rule': 50}
        x.field_names = header
        x.add_row(items)
        x.align = 'l'
        print(x)

