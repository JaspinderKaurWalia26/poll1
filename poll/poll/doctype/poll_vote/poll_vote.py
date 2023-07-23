# Copyright (c) 2013, Web Notes Technologies
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from poll.poll.doctype.poll.poll import DuplicateVoteError
from poll.poll.doctype.poll.poll import InactivePollStatusError

class PollVote(Document):
    def validate(self):
        self.ip = frappe.get_request_header('REMOTE_ADDR', None) or \
                  frappe.get_request_header('X-Forwarded-For') or '127.0.0.1'
        duplicate = frappe.db.get_value("Poll Vote", {"ip": self.ip, "poll": self.poll})
        status = frappe.db.get_value("Poll", {"name": self.poll}, "poll_status")  # Corrected the field name to "poll" instead of "name"

        if duplicate:
            raise DuplicateVoteError("You have already voted in this poll.")

        if status == "Inactive":
            raise InactivePollStatusError("This poll is currently inactive.")

    def on_update(self):
        poll = frappe.get_doc("Poll", self.poll)
        option = next((d for d in poll.poll_options if d.name == self.option_name), None)
        if option:
            option.votes = len(frappe.get_all("Poll Vote", filters={"option_name": self.option_name}))
            poll.save(ignore_permissions=True)
