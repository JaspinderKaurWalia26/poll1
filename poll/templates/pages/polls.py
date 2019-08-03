# -*- coding: utf-8 -*-
# Copyright (c) 2013, Web Notes Technologies
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


from frappe import db, get_all

base_template = "templates/pages/polls.html"

no_cache = 1

filters = {
    "published": 1
}

fields = [
    "title",
    "page_name",
    "description",
    "poll_status",
    "parent_website_route"
]


def get_context(context):
    doctype = "Poll"
    context.doctype = doctype
    context.listed_polls = get_all(doctype, fields, filters)

    context.std_footer = db.get_single_value(
        "Poll Settings", "standard_footer")

    context.std_header = db.get_single_value(
        "Poll Settings", "standard_header")

    return context
