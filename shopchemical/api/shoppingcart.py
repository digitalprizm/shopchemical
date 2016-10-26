from __future__ import unicode_literals
import frappe
import logging
import string
import datetime
import re
import json

from frappe.utils import getdate, flt,validate_email_add, cint
from frappe.model.naming import make_autoname
from frappe import throw, _, msgprint
import frappe.permissions
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

_logger = logging.getLogger(frappe.__name__)

@frappe.whitelist(allow_guest=True)
def ping():
    return 'pong'

@frappe.whitelist(allow_guest=True)
def get_brand():
	brand_list = frappe.db.sql("""select name,description,brand_image from tabItem where show_in_website=1""",as_dict=1)
    return  frappe.db.get_list("Brand",fields = ("name", "description", "brand_image"))

@frappe.whitelist(allow_guest=True)
def get_all_product():
    # return  frappe.db.get_list("Item",filters = {"show_in_website": 1},
    # 	fields = ("name", "description", "website_image"))
	item_list = frappe.db.sql("""select name,item_code,description,website_image from tabItem where show_in_website=1""",as_dict=1)
	print item_list
	return item_list


@frappe.whitelist(allow_guest=True)
def get_all_product2():
    return  frappe.db.get_list("Item",filters = {"show_in_website": 1},
    	fields = ("name", "description", "website_image"))
	# item_list = frappe.db.sql("""select name,item_code,description,website_image from tabItem""")
	# print item_list
	# return item_list

# frappe.db.get_list("Activity Cost", filters = {"show_in_website": ""},
# 		fields = ("name", "activity_type", "costing_rate", "billing_rate")):


def share_doc_with_owner(doc, method):
	customer_owner = frappe.db.get_value("Customer",doc.customer,"owner")
	if doc.owner != customer_owner:
		frappe.share.add(doc.doctype, doc.name, customer_owner,write=1)
		# frappe.msgprint(frappe.share.get_shared("Quotation", 't@t.com'))

def validate_share(doc,method):
	if not doc.get("__islocal") :	
		customer_owner = frappe.db.get_value("Customer",doc.customer,"owner")	
		if doc.owner != customer_owner:
			frappe.share.add(doc.doctype, doc.name, customer_owner,write=1)