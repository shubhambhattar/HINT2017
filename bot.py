import sys, csv, time, json
import telepot

blood_data = []

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)


    if content_type != 'text':
        bot.sendMessage(chat_id, "I don't understand.")
        return

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
                if attributes[j] == 'Contact':
                    temp += attributes[j] + ': \n'
                    numbers = bloodbank[attributes[j]].split(',')
                    for value in numbers:
                        temp += '<a href="tel:' + str(value) + '">' + str(value) + '</a>\n'
                        # temp += '<a href="http://www.github.com/">Github</a>\n'
                        # temp += '<a href="tel:18888888888">8888888888</a>\n'
                elif attributes[j] == 'Address':
                    temp += attributes[j] + ': ' + bloodbank['Address'] + '\n\n'
                    add = '%20'.join((bloodbank['Name'] + ' ' + bloodbank['Address'] + ' ' + bloodbank['City']).split(' '))
                    temp += '<a href="http://maps.google.com/?q=' + str(add) + '">' + 'Find in Google Maps' + '</a>\n\n'
                else:
                    temp += attributes[j] + ': ' + bloodbank[attributes[j]] + '\n\n'

            bot.sendMessage(chat_id, temp, parse_mode='HTML')
            found = True
    if not found:
        bot.sendMessage(chat_id, 'Sorry, no Blood Banks found.')

TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print('Listening...')

with open('data/bloodbank.csv', 'rb') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        blood_data.append(tuple(row))

del blood_data[0]
while True:
    time.sleep(10)
