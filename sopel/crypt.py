"""Basic rotaton-encryption commands."""

from sopel.module import commands

@commands('encrypt')
def encrypt(bot,trigger):
    text = trigger.group(2)
    last = text.split()[-1]
    try:
        last = int(last)
    except ValueError:
        bot.say("Not an integer!")
    encrypted = []
    for word in text.split()[:-1]:
        try:
            encrypted.append([chr(ord(char) + last) for char in word])
        except UnicodeDecodeError:
            bot.say("Sorry, encryption out of range.")
            pass
    bot.reply(" ".join([''.join(word) for word in encrypted]))
        
        
@commands('decrypt')
def decrypt(bot,trigger):
    text = trigger.group(2)
    last = text.split()[-1]
    try:
        last = int(last)
    except ValueError:
        bot.say("Not an integer!")
    decrypted = []
    for word in text.split()[:-1]:
        try:
            decrypted.append([chr(ord(char) - last) for char in word])
        except UnicodeDecodeError:
            bot.say("Sorry, decryption out of range.")
            pass
    bot.reply(" ".join([''.join(word) for word in decrypted]))


