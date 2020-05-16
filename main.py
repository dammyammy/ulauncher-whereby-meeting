from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesEvent, PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

import logging
import re
import sys

logger = logging.getLogger(__name__)
shortcuts = {}

def updateShortcuts(shortcutString):
    shortcuts.clear
    logger.info("Updating Shortcuts - %s" % (shortcutString))
    shortcutPairs = shortcutString
    for pair in shortcutPairs.split(';'):
        keyValue = pair.split(':')
        shortcuts[keyValue[0]] = keyValue[1]
        logger.debug("Shortcut %s for %s" % (keyValue[0], keyValue[1]))

def checkForShortcut(string):
    if string in shortcuts:
        logger.info("Shortcut found!  %s converted to %s" % (string, shortcuts[string]))
        return shortcuts[string]
    else:
        return string

class WherebyJoinMeeting(Extension):
    def __init__(self):
        super(WherebyJoinMeeting, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesEvent, PreferencesLoadListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateListener())

class PreferencesLoadListener(EventListener):
    def on_event(self, event, extension):
        updateShortcuts(event.preferences['shortcuts'])

class PreferencesUpdateListener(EventListener):
    def on_event(self, event, extension):
        if event.id == 'shortcuts':
            updateShortcuts(event.new_value)


class KeywordQueryEventListener(EventListener):
    def determineLinkType(self, wherebyId):
        logger.info("determineLinkType for %s" % (wherebyId))
        chatType = ''

        # Whereby offers two types of links:
        #  1) Meeting ID which is only numbers ('j')
        #  2) Personal Link which is 5-40 characters, start with a letter, and contain only a-z, 0-9, and '.' ('my')
        if re.match('^\d+$', wherebyId):
            chatType = 'j'
        elif re.match('^[a-z][a-z0-9.]{4,39}$', wherebyId):
            chatType = 'my'

        logger.info("Found that %s is %s" % (wherebyId, chatType))
        return chatType

    def on_event(self, event, extension):
        baseUri = extension.preferences['base_uri']


        userInputs = event.get_query().split()
        logger.info("User Inputs: " + "--".join(userInputs))

        error = 1

        chatId = checkForShortcut(userInputs[1])


        resultItem = None
        if error and len(chatId):
            resultItem = ExtensionResultItem(
                icon = 'images/error_icon.png',
                name = 'Unable to verify Whereby ID: ' + chatId
            )
        elif len(chatId):
            fullUri = "https://" + baseUri + '/' + chatId
            resultItem = ExtensionResultItem(
                icon = 'images/whereby_icon.png',
                name = 'Open Whereby for: ' + fullUri,
                on_enter = OpenUrlAction(fullUri)
            )

        return RenderResultListAction([resultItem])

if __name__ == '__main__':
    WherebyJoinMeeting().run()
