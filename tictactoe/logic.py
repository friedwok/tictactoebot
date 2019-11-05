import re
import messages
import random


field = '''
 ---
| | | |
 ---
| | | |
 ---
| | | |
 ---
'''


class Field:

    def __init__(self):
        global field
        self.field = field
        self.bot_symbol = ''
        self.player_symbol = ''
        self.pattern = r'[A-C] [1-3]'

    def check_point(self, message, bot):
        if not re.fullmatch(self.pattern, message.text):
            bot.send_message(message.chat.id, messages.message_3)
            return 0

        text = message.text.replace(' ', '')
        point_x = ord(text[0]) - ord('A')
        point_y = int(text[1]) - 1
        if self.field[self._get_offset((point_x, point_y))] != ' ':
            bot.send_message(message.chat.id, messages.message_4)
            bot.send_message(message.chat.id, self.field)
            return 0

        return 1

    def cross_or_zero(self):
        if random.randint(0, 1):
            self.bot_symbol = 'x'
            self.player_symbol = 'o'
        else:
            self.bot_symbol = 'o'
            self.player_symbol = 'x'

    def _get_offset(self, pos):
        x = 2 * (1 + int(pos[0]))
        y = 8 * int(pos[1]) + 5 * (int(pos[1]) + 1)
        offset = x + y
        return offset

    def put_point_on_field(self, pos, sym):
        offset = self._get_offset(pos)
        self.field = self.field[0:offset] + sym + self.field[(offset + 1):]

    def check_who_win(self):
        for i in range(3):
            for j in range(3):
                offset = self._get_offset((i, j))
                if self.field[offset] != ' ':
                    line = [(i, j)]
                    if self.check_lines(line):
                        if self.field[self._get_offset(line[0])] == self.bot_symbol:
                            return self.bot_symbol
                        elif self.field[self._get_offset(line[0])] == self.player_symbol:
                            return self.player_symbol

        for i in range(3):
            for j in range(3):
                offset = self._get_offset((i, j))
                if self.field[offset] == ' ':
                    return 0

        return 1

    def check_lines(self, line):
        # print(line)
        x = line[0][0]
        y = line[0][1]

        for i in range(3):
            offset = self._get_offset((x, i))
            if self.field[offset] == self.field[self._get_offset((x, y))] and i != y:
                line.append((x, i))
        if self._check_line(line):
            return 1

        for i in range(3):
            offset = self._get_offset((i, y))
            if self.field[offset] == self.field[self._get_offset((x, y))] and i != x:
                line.append((i, y))
        if self._check_line(line):
            return 1

        if x == y:
            for i in range(3):
                offset = self._get_offset((i, i))
                if self.field[offset] == self.field[self._get_offset((x, y))] and (i != x):
                    line.append((i, i))
            if self._check_line(line):
                return 1

            for i in range(3):
                offset = self._get_offset((i, 2-i))
                if self.field[offset] == self.field[self._get_offset((x, y))] and (i != 2-i):
                    line.append((i, 2-i))
            if self._check_line(line):
                return 1

        for i in range(3):
            for j in range(3):
                if self.field[self._get_offset((i, j))] == ' ':
                    return 0

        return 1

    def _check_line(self, line):
        if len(line) == 3:
            return 1
        elif len(line) == 2:
            line.pop()
        return 0

    def bot_step(self):
        while True:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            offset = self._get_offset((x, y))
            if self.field[offset] == ' ':
                self.field = self.field[0:offset] + self.bot_symbol + self.field[(offset + 1):]
                break
