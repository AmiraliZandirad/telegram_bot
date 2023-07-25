import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

# Replace YOUR_BOT_TOKEN with the API token you obtained from the BotFather
bot = telegram.Bot(token='YOUR_BOT_TOKEN')

# Define a dictionary to store the spam counter for each user
spam_counter = {}

# Define a dictionary to store the known users
known_users = {}

def add_user(update, context):
    # Get the user who sent the command
    user = update.message.from_user

    # Check if the user is already in the known users list
    if user.id in known_users:
        message = f'{user.first_name} is already in the known users list.'
    else:
        # Add the user to the known users list
        known_users[user.id] = user
        message = f'{user.first_name} has been added to the known users list.'

    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def remove_user(update, context):
    # Get the user who sent the command
    user = update.message.from_user

    # Check if the user is in the known users list
    if user.id in known_users:
        # Remove the user from the known users list
        del known_users[user.id]
        message = f'{user.first_name} has been removed from the known users list.'
    else:
        message = f'{user.first_name} is not in the known users list.'

    context.bot.send_message(chat_id=update.message.chat_id, text=message)

def handle_message(update, context):
    # Get the incoming message and the user who sent it
    message = update.message
    user = message.from_user

    # Check if the user is known or unknown
    if user.id in known_users:
        # Greet the user
        greeting = f'Hello {user.first_name}! How are you doing?'
        context.bot.send_message(chat_id=message.chat_id, text=greeting)
    else:
        # Check if the user has sent more than 3 messages
        if user.id in spam_counter:
            spam_counter[user.id] += 1
            if spam_counter[user.id] >= 3:
                # Block the user
                context.bot.block_user(user_id=user.id)
                del spam_counter[user.id]
                return
        else:
            spam_counter[user.id] = 1

        # Send a warning not to spam
        warning = 'Please do not spam me. This is your first warning.'
        context.bot.send_message(chat_id=message.chat_id, text=warning)

# Create the Updater and pass it the bot's token.
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Add the message handler to the dispatcher
dispatcher.add_handler(MessageHandler(filters.ALL, handle_message))

# Start the bot
updater.start_polling()
