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

def share_doc_with_owner(doc, method):
	customer_owner = frappe.db.get_value("Customer",doc.customer,"owner")
	if doc.owner != customer_owner:
		frappe.share.add(doc.doctype, doc.name, customer_owner,write=1,flags={"ignore_share_permission": True})
		# frappe.msgprint(frappe.share.get_shared("Quotation", 't@t.com'))

def validate_share(doc,method):
	if not doc.get("__islocal") :	
		customer_owner = frappe.db.get_value("Customer",doc.customer,"owner")	
		if doc.owner != customer_owner:
			frappe.share.add(doc.doctype, doc.name, customer_owner,write=1,flags={"ignore_share_permission": True})

@frappe.whitelist()
def add_interaction(doc):
	"""allow any logged user to post a comment"""
	doc = frappe.get_doc(json.loads(doc))

	if doc.doctype != "Interaction Master":
		frappe.throw(_("This method can only be used to create a Interaction Master"), frappe.PermissionError)

	doc.insert(ignore_permissions = True)

	return doc.as_dict()

@frappe.whitelist()
def create_todo(owner, assigned_by, description, date,reference_name,reference_type):
	"""allow any logged user to post toDo via interaction master"""
	todo = frappe.new_doc("ToDo")
	todo.owner = owner
	todo.assigned_by = assigned_by
	todo.description = description
	todo.date = date
	todo.reference_type = reference_type
	todo.reference_name = reference_name
	todo.insert(ignore_permissions=True)