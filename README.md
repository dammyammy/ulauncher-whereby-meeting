# ulauncher Whereby Join Meeting
[Ulauncher](https://ulauncher.io) extension allowing for joining whereby meetings

## Use
With auto type selection (see Settings)
> whereby 9995551234

With manual type selection (see settings)
> whereby 9995551234


## Settings
### Whereby Keyword
Keyword to use this extension.  Default is 'whereby', but I like using 'wb'

### Whereby Base URI
This is the your company's whereby URI.

So far I'm working on a sample size of 1 so it seems that this should be in the form of 'corp.whereby.com'

### Auto or Manual link type determination
Whereby offers two types of links:
  1) Meeting ID which is only numbers ('j')
  2) Personal Link which is 5-40 characters, start with a letter, and contain only a-z, 0-9, and '.' ('my')

The default is Auto which should work for most (if not all) whereby chat IDs.

If you select Manual you will have to provide the keyword 'my' before the chat ID when it's required. See Use section for examples.

### Shortcuts

At this time it is a string with the following format: name:chat_id;another_name:chat_id...

In either auto or manual mode if a string is entered that matches a name in the shortcut string it will be replaced with the corresponding Chat ID.