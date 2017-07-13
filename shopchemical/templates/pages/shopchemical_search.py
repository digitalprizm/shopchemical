# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, nowdate
from erpnext.setup.doctype.item_group.item_group import get_item_for_list_in_html

no_cache = 1
no_sitemap = 1

def get_context(context):
	context.show_search=True
	context.page_length = 6
	context.search_link = '/qa_product_search'

@frappe.whitelist(allow_guest=True)
def all_product():
	# return  frappe.db.get_list("Item",filters = {"show_in_website": 1},
	# 	fields = ("name", "description", "website_image"))
	price_list_name = frappe.db.sql("""select value from tabSingles where doctype='Shopping Cart Settings' and field='price_list'""",as_dict=1)
	price_list_name=price_list_name[0]['value']
	# price_list_rate = frappe.db.sql("""select price_list_rate from `tabItem Price` 
	# 	where price_list='{0}' and item_code='{1}'""".format(price_list_name,item_code),as_dict=1)

	item_list = frappe.db.sql("""select i.name,i.item_code,i.item_group,i.website_image,i.image,i.thumbnail,
		i.route as item_route, REPLACE(delivery_time,0,'-') AS delivery_time,ig.route as group_route,i.show_get_quote,i.msds,i.brand, i.stock_uom,
		case 
			WHEN 1 = 1 THEN 
				(select FORMAT(price_list_rate,2) from `tabItem Price` where price_list='{0}' and item_code=i.item_code)
		else
			""
		END AS price_list_rate,
		CASE
			WHEN 1=1 THEN
			(select FORMAT(sum(actual_qty),2) as available_qty from tabBin where item_code=i.item_code)
		else
			""
		END AS available_qty
		 from tabItem i, `tabItem Group` ig where i.show_in_website=1 and i.item_group = ig.name""".format(price_list_name),as_dict=1)
	
	print "\n\n\nHiiiiiiiii"
	print item_list,"item_list	"
	return item_list


@frappe.whitelist(allow_guest=True)
def get_product_list(search=None, start=0, limit=12):
	# limit = 12 because we show 12 items in the grid view

	# base query
	# query = """select name, item_name, item_code, route, website_image, thumbnail, item_group,
	# 		description, web_long_description as website_description, brand
	# 	from `tabItem`
	# 	where (show_in_website = 1 or show_variant_in_website = 1)
	# 		and disabled=0
	# 		and (end_of_life is null or end_of_life='0000-00-00' or end_of_life > %(today)s)"""
	price_list_name = frappe.db.sql("""select value from tabSingles where doctype='Shopping Cart Settings' and field='price_list'""",as_dict=1)
	price_list_name=price_list_name[0]['value']		
	query = """select i.name as item_name,i.item_code,i.item_group,i.website_image,i.image,i.thumbnail,
			i.route as item_route, REPLACE(delivery_time,0,'-') AS delivery_time,ig.route as group_route,i.show_get_quote,i.msds,i.brand, i.stock_uom,
			case 
				WHEN 1 = 1 THEN 
					(select FORMAT(price_list_rate,2) from `tabItem Price` where price_list='{0}' and item_code=i.item_code)
			else
				""
			END AS price_list_rate,
			CASE
				WHEN 1=1 THEN
				(select FORMAT(sum(actual_qty),2) as available_qty from tabBin where item_code=i.item_code)
			else
				""
			END AS available_qty
			 from tabItem i, `tabItem Group` ig where i.show_in_website=1 
			 and i.item_group = ig.name desc limit '{1}', '{2}'""".format(price_list_name,start, limit)
	
	# search term condition
	if search:
		query = """select i.name as item_name,i.item_code,i.item_group,i.website_image,i.image,i.thumbnail,
			i.route as item_route, REPLACE(delivery_time,0,'-') AS delivery_time,ig.route as group_route,i.show_get_quote,i.msds,i.brand, i.stock_uom,
			case 
				WHEN 1 = 1 THEN 
					(select FORMAT(price_list_rate,2) from `tabItem Price` where price_list='{0}' and item_code=i.item_code)
			else
				""
			END AS price_list_rate,
			CASE
				WHEN 1=1 THEN
				(select FORMAT(sum(actual_qty),2) as available_qty from tabBin where item_code=i.item_code)
			else
				""
			END AS available_qty
			 from tabItem i, `tabItem Group` ig where i.show_in_website=1 
			 and i.item_group = ig.name and (i.item_name like '%{1}%' or i.name like '%{1}%' or i.description like '%{1}%')""".format(price_list_name, search)
		# query += """ and (web_long_description like '{0}'
		# 		or description like '{0}'
		# 		or item_name like '{0}'
		# 		or name like '{0}')""".format(search)
		# search = "%" + cstr(search) + "%"
	data = frappe.db.sql(query, as_dict=1,debug=1)
	# frappe.msgprint("hi")
	# order by
	# query += """ order by weightage desc, idx desc, modified desc limit %s, %s""" % (start, limit)
	# print "\n\n\nnnn",query

	# data = frappe.db.sql(query, {
	# 	"search": search,
	# 	"today": nowdate()
	# }, as_dict=1,debug=1)
	return [cs_get_item_for_list_in_html(r) for r in data]

# @frappe.whitelist(allow_guest=True)
# def get_product_list(search=None, start=0, limit=12):
# 	# limit = 12 because we show 12 items in the grid view

# 	# base query
# 	query = """select name, item_name, item_code, route, website_image, thumbnail, item_group,
# 			description, web_long_description as website_description, brand
# 		from `tabItem`
# 		where (show_in_website = 1 or show_variant_in_website = 1)
# 			and disabled=0
# 			and (end_of_life is null or end_of_life='0000-00-00' or end_of_life > %(today)s)"""

# 	# search term condition
# 	if search:
# 		query += """ and (web_long_description like %(search)s
# 				or description like %(search)s
# 				or item_name like %(search)s
# 				or name like %(search)s)"""
# 		search = "%" + cstr(search) + "%"

# 	# order by
# 	query += """ order by weightage desc, idx desc, modified desc limit %s, %s""" % (start, limit)

# 	data = frappe.db.sql(query, {
# 		"search": search,
# 		"today": nowdate()
# 	}, as_dict=1)

# 	return [cs_get_item_for_list_in_html(r) for r in data]

def cs_get_item_for_list_in_html(context):
	# add missing absolute link in files
	# user may forget it during upload
	if (context.get("website_image") or "").startswith("files/"):
		context["website_image"] = "/" + urllib.quote(context["website_image"])

	# products_template = 'templates/includes/products_as_grid.html'
	# if cint(frappe.db.get_single_value('Products Settings', 'products_as_list')):
	products_template = 'templates/includes/qa_product_as_list.html'

	return frappe.get_template(products_template).render(context)
