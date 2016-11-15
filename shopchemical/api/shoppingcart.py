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
	brand_list = frappe.db.sql("""select name,description,brand_image from tabBrand""",as_dict=1)
	return  brand_list

@frappe.whitelist(allow_guest=True)
def get_all_product():
    # return  frappe.db.get_list("Item",filters = {"show_in_website": 1},
    # 	fields = ("name", "description", "website_image"))
	item_list = frappe.db.sql("""select i.name,i.item_code,i.item_group,i.website_image,i.image,i.thumbnail,
		i.route as item_route,ig.route as group_route,i.show_get_quote,i.msds,i.brand from tabItem i, `tabItem Group` ig where i.show_in_website=1 and i.item_group = ig.name""",as_dict=1)
	return item_list

@frappe.whitelist(allow_guest=True)
def get_brandwise_item(brand):
	item_list = frappe.db.sql("""select name,item_code,item_group,website_image,image,thumbnail,
		route as item_route,show_get_quote,msds,brand from tabItem where show_in_website=1 and 
		brand='{0}'""".format(brand),as_dict=1)
	return item_list

@frappe.whitelist(allow_guest=True)
def get_item_detail(item_code):
	item_list = frappe.db.sql("""select name,item_code,item_group,website_image,image,thumbnail,
		route as item_route,show_get_quote,msds,brand from tabItem where item_code='{0}'""".format(item_code),as_dict=1)
	return item_list

@frappe.whitelist(allow_guest=True)
def get_item_price(item_code):
	price_list_name = frappe.db.sql("""select value from tabSingles where doctype='Shopping Cart Settings' and field='price_list'""",as_dict=1)
	price_list_name=price_list_name[0]['value']
	price_list_rate = frappe.db.sql("""select price_list_rate from `tabItem Price` 
		where price_list='{0}' and item_code='{1}'""".format(price_list_name,item_code),as_dict=1)
	return price_list_rate

@frappe.whitelist(allow_guest=True)
def get_available_qty(item_code):
	available_qty = frappe.db.sql("""select item_code,sum(actual_qty) as available_qty,stock_uom from tabBin 
		where item_code='{0}'""".format(item_code),as_dict=1)
	return available_qty

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
