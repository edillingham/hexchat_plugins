import hexchat
import pushbullet

__module_name__ = "pushbullet"
__module_version__ = "1.0"
__module_description__ = "Send messages via Pushbullet"

CONFIG_APIKEY = 'pushbullet_api_key'


def pushb(word, word_eol, userdata):
    """ Hook for /pushb command in HexChat"""
    api_key = hexchat.get_pluginpref(CONFIG_APIKEY)

    if word[1] == 'CONFIG':
        if len(word_eol) > 2:
            set_config(word_eol[2])
        else:
            hexchat.prnt('Pushbullet API key currently set to "{}"'
                         .format(api_key))
        return hexchat.EAT_HEXCHAT

    if not api_key:
        hexchat.prnt('\037\00304Pushbullet API key not specified.',
                     ' Use /pushb CONFIG <api_key> to set one.')
        return hexchat.EAT_HEXCHAT

    try:
        pb = pushbullet.Pushbullet(api_key)
    except pushbullet.errors.InvalidKeyError:
        hexchat.prnt('\037\00304Invalid API key!')
        return hexchat.EAT_HEXCHAT

    push(word, word_eol)

    return hexchat.EAT_HEXCHAT


def push(word, word_eol):
    """ "push" function """
    title = "IRC Message from {}".format(hexchat.get_info('nick'))
    text = word_eol[1]

    if text.startswith('http'):
        pb.push_link(title, text)
    else:
        pb.push_note(title, text)
    hexchat.prnt('Pushed!')


def set_config(api_key):
    """ Sets API key in plugin preferences. """
    if hexchat.set_pluginpref(CONFIG_APIKEY, api_key):
        hexchat.prnt('Pushbullet API key set.')
    else:
        hexchat.prnt('\037\00304Failed to configure Pushbullet plugin!')


hexchat.prnt('Pushbullet plugin loaded.  Use /pushb to send a message.')
hexchat.hook_command('pushb', pushb)
