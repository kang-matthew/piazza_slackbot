

class PiazzaPost:
    """Constructs the new Piazza post message and stores the state of completed Slack actions."""

    OPENING_BLOCK = {
	"type": "section",
	"text": {
	    "type": "plain_text",
	    "text": ":mega: New Question Posted on Piazza! :piazza:",
	    "emoji": True
	}
    }

    POST_LINK_BUTTON_BLOCK = {
	"type": "section",
	"text": {
	    "type": "mrkdwn",
	    "text": "*@1: _Sample Subject Title Here_*"
	},
	"accessory": {
	    "type": "button",
	    "text": {
		"type": "plain_text",
		"text": "Link :link:",
		"emoji": True
	    },
	    "value": "click_me_123",
	    "url": "https://google.com",
	    "action_id": "button-action"
	}
    }

    # !!! Add interactivity TODO
    ACTIONS_BLOCK = {
	"type": "actions",
	"elements": [
	    {
		"type": "button",
		"text": {
		    "type": "plain_text",
		    "text": "I'm on it! :hand:",
		    "emoji": True
		},
		"value": "click_me_123",
		"action_id": "actionId-0"
	    },
	    {
		"type": "button",
		"text": {
		    "type": "plain_text",
		    "text": "Hand-in",
		    "emoji": True
		},
		"value": "click_me_123",
		"action_id": "actionId-1"
	    },
	    {
		"type": "button",
		"text": {
		    "type": "plain_text",
		    "text": "Admin",
		    "emoji": True
		},
		"value": "click_me_123",
		"action_id": "actionId-2"
	    }
	]
    }

    def __init__(self, subject, post_id, config):
        self.subject = subject
        self.post_id = post_id
        self.config = config

    def get_message_payload(self):
        return {
            "text": "New Post on Piazza!", # fallback
            "channel": self.config.SLACK_CHANNEL,
            "username": self.config.SLACK_BOT_NAME,
            "unfurl_links": False,
	    "unfurl_media": False,
            "blocks": [
                self.OPENING_BLOCK,
                self._get_post_link_block(),
                {"type": "divider"}
            ],
        }

    def _get_post_link_block(self):
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<https://piazza.com/class/{self.config.PIAZZA_ID}/post/{self.post_id}|*@{self.post_id}: _{self.subject}_*>"
            }
        }
