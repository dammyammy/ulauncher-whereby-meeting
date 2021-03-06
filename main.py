from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesEvent, PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

import logging

room = ""

logger = logging.getLogger(__name__)

def updateRoom(roomString):
    logger.info("Updating Room - %s" % (roomString))
    room = roomString


def checkForRoom(string):
    if room == string:
        return room
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
        updateRoom(event.preferences['default_room'])

class PreferencesUpdateListener(EventListener):
    def on_event(self, event, extension):
        if event.id == 'default_room':
            updateRoom(event.new_value)

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        base_uri = extension.preferences['base_uri']

        default_room = extension.preferences['default_room']

        updateRoom(default_room)

        logger.info("User Room: " + "--".join(event.get_argument()))

        if event.get_argument() in ['default', 'room', 'd', 'open']:
            chat_id = checkForRoom(default_room)
        else:
            chat_id = checkForRoom(event.get_argument())

        full_uri = "https://" + base_uri + '/' + chat_id

        resultItem = ExtensionResultItem(
            icon = 'images/whereby_icon.png',
            name = 'Open ' + chat_id + ' Whereby Room.',
            on_enter = OpenUrlAction(full_uri)
        )

        return RenderResultListAction([resultItem])

if __name__ == '__main__':
    WherebyJoinMeeting().run()
