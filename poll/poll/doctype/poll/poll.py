# -*- coding: utf-8 -*-
# Copyright (c) 2013, Web Notes Technologies
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator

from frappe import _dict as pydict


class DuplicateVoteError(frappe.ValidationError):
    pass


class InactivePollStatusError(frappe.ValidationError):
    pass


class Poll(WebsiteGenerator):
    website = pydict(
        template="templates/generators/poll.html",
        condition_field="published",
        page_title_field="title"
    )

    def validate(self):
        self.page_name = self.name
        self.parent_website_route = "polls"

        self.route = "poll/{page_name}" \
            .format(page_name=self.page_name)

    def get_context(self, context):
        context.maxvotes = max(
            [(d.previous_votes or 0) + (d.votes or 0) for d in self.poll_options])
        context.sorted_options = sorted(self.poll_options,
                                        key=lambda d: ((d.previous_votes or 0) + (d.votes or 0), -d.idx), reverse=True)
        context.status = frappe.db.get_value(
            "Poll", {"name": self.name}, fieldname="poll_status")
        context.parents = [
            {'route': self.parent_website_route, 'title': 'Polls'}]
        return context

    no_cache = 1
    no_sitemap = 1
    page_name = ""
    route = ""
    poll_options = []
    parent_website_route = ""


def insert_vote(option_name):
    vote = frappe.new_doc("Poll Vote")
    vote.option_name = option_name
    vote.poll = frappe.db.get_value("Poll Option", option_name, "parent")
    vote.insert(ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def add_vote(option_name):
    try:
        insert_vote(option_name)
        return "Thank you for voting. Your vote has been registered!"
    except DuplicateVoteError:
        return "You have already voted on this poll"
    except InactivePollStatusError:
        return "This Poll is Inactive. You cannot vote on this Poll!"


# def get_list_context(context=None):
#     context.update({
#         "doctype": "Poll",
#         "show_sidebar": True,
#         "show_search": True,
#         'no_breadcrumbs': True,
#         "title": _("Newsletter"),
#         "get_list": get_newsletter_list,
#         "row_template": "templates/pages/polls.html",
#     })


# def get_newsletter_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by="modified"):
#     return frappe.db.sql('''select * from `tabUser` n
#         where  n.published=1
#         order by n.modified desc limit {0}, {1}
#         '''.format(limit_start, limit_page_length), as_dict=1)
