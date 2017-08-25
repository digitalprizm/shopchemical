from __future__ import unicode_literals
import frappe, os, json, json
from frappe import _

@frappe.whitelist(allow_guest=True)
def update_user_location(name=None,lat=None,lon=None):
	user = frappe.get_doc("User", name)
	if user.name:
		user.flags.ignore_permissions = True
		user.latitude = lat
		user.longitude = lon
		user.save(ignore_permissions=True)
		frappe.db.commit()
		return "Location updated for the user " + user.name
