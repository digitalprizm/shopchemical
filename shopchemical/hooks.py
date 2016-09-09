# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "shopchemical"
app_title = "shopchemical"
app_publisher = "SBK"
app_description = "app to manage shop chemical"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "kolate.sambhaji@gmail.com"
app_license = "mit"

fixtures = ['Website Settings','Web Page','Contact Us Settings']

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/shopchemical/css/shopchemical.css"
# app_include_js = "/assets/shopchemical/js/shopchemical.js"

# include js, css files in header of web template
# web_include_css = "/assets/shopchemical/css/shopchemical.css"
# web_include_js = "/assets/shopchemical/js/shopchemical.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "shopchemical.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "shopchemical.install.before_install"
# after_install = "shopchemical.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "shopchemical.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"shopchemical.tasks.all"
# 	],
# 	"daily": [
# 		"shopchemical.tasks.daily"
# 	],
# 	"hourly": [
# 		"shopchemical.tasks.hourly"
# 	],
# 	"weekly": [
# 		"shopchemical.tasks.weekly"
# 	]
# 	"monthly": [
# 		"shopchemical.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "shopchemical.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "shopchemical.event.get_events"
# }

