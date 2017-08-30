# -*- coding: utf-8 -*-
# Copyright (c) 2015, SBK and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

import json
from datetime import timedelta
# from erpnext.controllers.queries import get_match_cond
from frappe.utils import flt, formatdate, time_diff_in_hours, get_datetime, getdate, today, cint, get_datetime_str,get_time
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, today, getdate
from email.utils import parseaddr
from frappe.model.naming import get_default_naming_series

class GetQuote(Document):
	pass

def get_project_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by="modified"):
	return frappe.db.sql('''select distinct get_quote.*
		from `tabGet Quote` get_quote
		where
			get_quote.owner = %(user)s
			order by get_quote.modified desc
			limit {0}, {1}
		'''.format(limit_start, limit_page_length),
			{'user':frappe.session.user},
			as_dict=True,
			update={'doctype':'Get Quote'},debug=1)

def get_list_context(context=None):
	from erpnext.controllers.website_list_for_contact import get_list_context
	list_context = get_list_context(context)
	list_context.update({
		'show_sidebar': True,
		'show_search': False,
		'no_breadcrumbs': True,
		'title': _('Get Quote'),
		"get_list": get_project_list,
		"row_template": "templates/includes/get_quote_row.html",
	})

	return list_context



@frappe.whitelist()
def create_quote(source_name, target_doc=None):
	def set_missing_values(source, target):
		company_name = frappe.db.get_single_value('Global Defaults', 'default_company')

		# company_name=frappe.db.get_value("Company",{"company_name":source.doctor},"company_name")
		company_cost_center = frappe.db.get_value("Company",{"company_name":company_name},"cost_center")
		# company_income_account = frappe.db.get_value("Company",{"company_name":source.doctor},"default_income_account")
		# company_additional_info = frappe.db.get_value("Company",{"company_name":source.company},"additional_info")
		# customer_name = frappe.db.get_value("Customer",{"customer_name":source.surgeon},"customer_name")
		# print customer_name
		item_description = frappe.db.get_value("Item",source.item_name,"description")
		stock_uom = frappe.db.get_value("Item",source.item_name,"stock_uom")
		price_list_name = frappe.db.sql("""select value from tabSingles where doctype='Shopping Cart Settings' and field='price_list'""",as_dict=1)
		price_list_name=price_list_name[0]['value']
		item_price = frappe.db.get_value("Item Price", {"price_list": price_list_name,
			"item_code": source.item_name})
		email_id = source.owner
		real_name, email_id = parseaddr(email_id)

		customer_contact = frappe.db.get_value("Contact",{ "email_id":source.owner},"name")

		customer_name = frappe.db.sql("""select link_name 
			from `tabDynamic Link` 
			where link_doctype="Customer" and parenttype="Contact" 
			and parent='{0}' limit 1""".format(customer_contact),as_list=1)

		# if frappe.db.get_value("Lead", {"email_id": email_id}):
		# 	lead = frappe.db.get_value("Lead", {"email_id": email_id})
		# else: 
		# 	lead = frappe.get_doc({
		# 		"doctype": "Lead",
		# 		"phone": source.contact_number,
		# 		"email_id": source.owner,
		# 		"lead_name": real_name or source.owner,
		# 		"status": "Lead",
		# 		"naming_series": get_default_naming_series("Lead"),
		# 		"company": frappe.db.get_default("Company"),
		# 		"source": "Website"
		# 	})
		# 	lead.insert()
		# 	lead = lead.name

		# if source.is_surgeon_billable==1:
		# 	target.customer = source.surgeon
		# else:
		# 	target.customer = source.hospital
		# target.doctor = source.doctor
		# target.surgeon = source.surgeon
		# target.surgeon_1 = source.surgeon_1
		# target.surgeon_2 = source.surgeon_2
		# target.patient = source.patient
		# target.case = source.name
		# target.patient_case_no=source.case_no
		target.company = company_name
		target.quotation_to = "Customer"
		target.customer = customer_name[0][0]
		target.due_date = today()
		target.set('items', [])
		k = target.append('items', {})
		# k.name = source.operation_type
		k.item_code = source.item_name
		k.item_name = source.item_name
		# k.description = "Case Fee for Case" + source_name + " and Doctor " + source.doctor + " and Hospial " + source.hospital
		k.cost_center = company_cost_center
		# k.income_account = company_income_account
		# k.additional_info = company_additional_info
		k.uom = "Nos"
		k.conversion_factor = 1
		if stock_uom: 
			k.stock_uom = stock_uom
		else:
			k.stock_uom = "Nos"
		k.qty = 1
		k.description = item_description
		k.rate = item_price
		target.get_quote = source.name
		
	doclist = get_mapped_doc("Get Quote", source_name, {
			"Get Quote": {
				"doctype": "Quotation",
				"validation": {
					"docstatus": ["=", 1]
				},
			}
		}, target_doc, set_missing_values, ignore_permissions=False)
	return doclist


