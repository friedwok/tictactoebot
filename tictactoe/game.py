import telebot
import messages
import random
import logic

token = '990131926:AAFTzAJO0Vw0vqfB_w6Y_ReNh0rAlF0kTuM'
bot = telebot.TeleBot(token)
game_started = 0
field = logic.Field()


@bot.message_handler(commands=['start'])
def start_message(message):
    global game_started
    game_started = 0

    bot_start = random.randint(0, 1)
    field.cross_or_zero()

    if bot_start:
        point_coordinates = (random.randint(0, 2), random.randint(0, 2))
        field.put_point_on_field(point_coordinates, field.bot_symbol)

    bot.send_message(message.chat.id, field.field[1:])
    bot.send_message(message.chat.id, messages.message_3)
    game_started = 1


@bot.message_handler(content_types=['text'])
def start_game(message):
    # pdb.set_trace()
    global game_started
    global field
    if not game_started:
        bot.send_message(message.chat.id, messages.message_2)
        return

    if game_started and field.check_point(message, bot):
        text = message.text.replace(' ', '')
        point_x = ord(text[0]) - ord('A')
        point_y = int(text[1]) - 1
        field.put_point_on_field((point_x, point_y), field.player_symbol)
        bot.send_message(message.chat.id, field.field[1:])
        r = field.check_who_win()
        if r == field.bot_symbol:
            bot.send_message(message.chat.id, messages.message_5)
        elif r == field.player_symbol:
            bot.send_message(message.chat.id, messages.message_6)
        elif r == 1:
            bot.send_message(message.chat.id, messages.message_7)
        if r:   # if r returns 'x', 'o', or 1
            game_started = 0
            field = logic.Field()
            bot.send_message(message.chat.id, messages.message_2)

        if game_started:
            field.bot_step()
            bot.send_message(message.chat.id, field.field[1:])
            r = field.check_who_win()
            if r == field.bot_symbol:
                bot.send_message(message.chat.id, messages.message_5)
                game_started = 0
                field = logic.Field()
            elif r == 1:
                bot.send_message(message.chat.id, messages.message_7)
                game_started = 0
                field = logic.Field()
            elif r == 0:
                bot.send_message(message.chat.id, messages.message_3)


def main():
    bot.polling()


if __name__ == '__main__':
    main()
