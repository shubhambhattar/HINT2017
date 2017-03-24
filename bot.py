import sys, csv, time, json
import telepot

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    found = False
    bloodbank = {
        'Name': '',
        'Address': '',
        'City': '',
        'State': '',
        'Pincode': '',
        'Contact': ''
    }
    bot.sendMessage(chat_id, 'Retrieving Blood Banks in ' + msg['text'])
    for i in range(len(blood_data)):
        if blood_data[i][2] == msg['text']:

            temp = ''
            indexes = [4, 5, 2, 1, 6, 7]
            attributes = ['Name', 'Address', 'City', 'State', 'Pincode', 'Contact']
            for j in range(6):
                bloodbank[attributes[j]] = blood_data[i][indexes[j]]
                temp += attributes[j] + ': ' + bloodbank[attributes[j]] + '\n'

            # values = []
            # for j in [4, 5, 3, 2, 1, 6, 7]:
                # values.append(str(blood_data[i][j]))
            # temp = ''
            # for j in range(7):
                # temp += attributes[j] + ': ' + values[j] + '\n'
            bot.sendMessage(chat_id, temp)
            found = True
    if not found:
        bot.sendMessage(chat_id, 'Sorry, no Blood Banks found.')

TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print('Listening...')

blood_data = []
with open('data/bloodbank.csv', 'rb') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        blood_data.append(tuple(row))

del blood_data[0]

while True:
    time.sleep(10)
