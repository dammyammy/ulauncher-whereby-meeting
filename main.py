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
        base_uri = extension.preferences['base_uri']

        default_room = extension.preferences['default_room']

        logger.info("User Room: " + "--".join(event.get_argument()))

        if len(event.get_argument()) == 0:
            chat_id = default_room
        else:
            chat_id = event.get_argument()

        full_uri = "https://" + base_uri + '/' + chat_id

        resultItem = ExtensionResultItem(
            icon = 'images/whereby_icon.png',
            name = 'Open Whereby for: ' + full_uri,
            on_enter = OpenUrlAction(full_uri)
        )

        return RenderResultListAction([resultItem])

if __name__ == '__main__':
    WherebyJoinMeeting().run()
