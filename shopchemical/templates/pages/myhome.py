# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from __future__ import unicode_literals
import frappe
import urllib
from frappe.utils import nowdate, cint, cstr, nowdate
from frappe.utils.nestedset import NestedSet
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.render import clear_cache
from frappe.website.doctype.website_slideshow.website_slideshow import get_slideshow
from erpnext.setup.doctype.item_group.item_group import get_item_for_list_in_html

no_cache = 1
no_sitemap = 1

def get_context(context):
	context.show_search = True

def sc_get_item_for_list_in_html(context):
	# add missing absolute link in files
	# user may forget it during upload
	if (context.get("website_image") or "").startswith("files/"):
		context["website_image"] = "/" + urllib.quote(context["website_image"])

	products_template = 'templates/includes/schome.html'
	if cint(frappe.db.get_single_value('Products Settings', 'products_as_list')):
		products_template = 'templates/include/my_product_list.html'

	print "\nsc_get_item_for_list_in_html"
	print products_template
	print context
	return frappe.get_template(products_template).render(context)

@frappe.whitelist(allow_guest=True)
def get_product_list(search=None, start=0, limit=12):
	# limit = 12 because we show 12 items in the grid view
	print "\n\nhi2"

	# base query
	query = """select name, item_name, item_code, route, website_image, thumbnail, item_group,
			description, web_long_description as website_description
		from `tabItem`
		where show_in_website = 1
			and disabled=0
			and (end_of_life is null or end_of_life='0000-00-00' or end_of_life > %(today)s)
			and (variant_of is null or variant_of = '')"""

	# search term condition
	if search:
		query += """ and (web_long_description like %(search)s
				or description like %(search)s
				or item_name like %(search)s
				or name like %(search)s)"""
		search = "%" + cstr(search) + "%"

	# order by
	query += """ order by weightage desc, idx desc, modified desc limit %s, %s""" % (start, limit)

	data = frappe.db.sql(query, {
		"search": search,
		"today": nowdate()
	}, as_dict=1)

	return [sc_get_item_for_list_in_html(r) for r in data]

