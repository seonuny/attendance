
#!/bin/sh

# telegram configuration
# token
TOKEN='561033107:AAFRKMLeEghQgfZf13a1hHMFo0aJRMGeVe4'
#TOKEN2='593775352:AAE5ct8r4pfrJNE2vRTY8VXHaCNjDPuDWJE'
# CHAT_ID
CHAT_ID="454993046"
URL='https://api.telegram.org/bot'$TOKEN
MSG_URL=$URL'/sendMessage?chat_id='

MSG=$1
curl --data-urlencode "text=${MSG}" "$MSG_URL"$CHAT_ID"&"
