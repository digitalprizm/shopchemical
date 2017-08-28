// Copyright (c) 2016, SBK and contributors
// For license information, please see license.txt

frappe.ui.form.on('Get Quote', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1) {
			cur_frm.add_custom_button(__("Create Quotation"),
				function() {
					frappe.model.open_mapped_doc({
							method: "shopchemical.shopchemical.doctype.get_quote.get_quote.create_quote",
							frm: cur_frm
					})
				})
			}
	}
});
