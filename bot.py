import sys, csv, time, json
import telepot

# store the data from CSV file to this variable as a list of tuples
blood_data = []

# To Do:
# Solve Wrong Query address issue of S.M.S. Hospital Jaipur
def get_address(bloodbank):
    name, address, city = bloodbank['Name'], bloodbank['Address'], bloodbank['City']
    query_address = name

    if address != 'NA':
        query_address += ', ' + address

    query_address += ', ' + city
    return '%20'.join(query_address.split(' '))

def handle(msg):

    # find the basic information from Message object
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    # if the content_type is not text, then we can safely ignore the request
    if content_type != 'text':
        bot.sendMessage(chat_id, "I don't understand.")
        return

    # boolean value to check whether the variable is found or not
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

        # check whether the given city is in the database or not
        if blood_data[i][2] == msg['text']:

            # indexes of the required attributes from the `data/bloodbanks.csv`
            indexes = [4, 5, 2, 1, 6, 7]
            attributes = ['Name', 'Address', 'City', 'State', 'Pincode', 'Contact']
            temp = ''

            for j in range(6):
                bloodbank[attributes[j]] = blood_data[i][indexes[j]]
                if attributes[j] == 'Contact':
                    temp += attributes[j] + ': \n'

                    # split in different lines if there are multiple contact numbers
                    numbers = bloodbank[attributes[j]].split(',')
                    for value in numbers:
                        temp += '<a href="tel//:' + str(''.join(value.split(' '))) + '/">' + str(value) + '</a>\n'
                elif attributes[j] == 'Address':
                    temp += attributes[j] + ': ' + bloodbank['Address'] + '\n\n'
                    query_address = get_address(bloodbank)
                    temp += '<a href="http://maps.google.com/?q=' + query_address + '">Find in Google Maps</a>\n\n'
                else:
                    temp += attributes[j] + ': ' + bloodbank[attributes[j]] + '\n\n'

            # send the message and set the parse_mode to `HTML` to correctly
            # format hyperlinks - Google Maps and Contact details
            bot.sendMessage(chat_id, temp, parse_mode='HTML')
            found = True

    # send an appropriate response if not found
    if not found:
        bot.sendMessage(chat_id, 'Sorry, no Blood Banks found.')

# extract data from `data/bloodbank.csv` and store it in `blood_data`
with open('data/bloodbank.csv', 'rb') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        blood_data.append(tuple(row))

# delete the first row that contains metadata
del blood_data[0]

# get TOKEN of Telegram bot from command line
TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print('Listening...')

while True:
    time.sleep(10)
