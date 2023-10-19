import json

from django.test import TestCase

from invite.models import Invite
from oauth.tools.wxwork_tools import WXWorkApi
invite = Invite.objects.all()[1]
api = WXWorkApi()
api.send_markdown_msg(1000003, invite)

