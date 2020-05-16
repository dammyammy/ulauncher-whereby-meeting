from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesEvent, PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

import logging

logger = logging.getLogger(__name__)

class WherebyJoinMeeting(Extension):
    def __init__(self):
        super(WherebyJoinMeeting, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        baseUri = extension.preferences['base_uri']

        defaultRoom = extension.preferences['default_room']

        logger.info("User Inputs: " + "--".join(event.get_argument()))

        chatId = event.get_argument()

        if len(chatId) == 0:
            fullUri = "https://" + baseUri + '/' + defaultRoom
        else:
            fullUri = "https://" + baseUri + '/' + chatId

        resultItem = ExtensionResultItem(
            icon = 'images/whereby_icon.png',
            name = 'Open Whereby for: ' + fullUri,
            on_enter = OpenUrlAction(fullUri)
        )

        return RenderResultListAction([resultItem])

if __name__ == '__main__':
    WherebyJoinMeeting().run()
