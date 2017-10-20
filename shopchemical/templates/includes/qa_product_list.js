// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

window.get_product_list = function() {
	$(".more-btn .btn").click(function() {
		window.get_product_list()
	});

	if(window.start==undefined) {
		throw "product list not initialized (no start)"
	};
	   	
	$.ajax({
		method: "GET",
		url: "/",
		dataType: "json",
		data: {
				cmd: "shopchemical.templates.pages.shopchemical_search.get_product_list",
				start: window.start,
				search: "%"
				// item_group: window.item_group,
				// brand: window.brand,
				// product_group: window.product_group
			},
		dataType: "json",
		success: function(data) {
			$(".item-search").hide();
			window.render_product_list(data.message || []);
			    setTimeout(function(){ 
				$.getScript( "http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.0/jquery.dataTables.min.js", function( data, textStatus, jqxhr ) {

				  	 $('#example').DataTable({
						"iDisplayLength": 100,
				  	 	"oSearch": {"sSearch": get_url_arg("search")},
				  	 	"oLanguage": { "sSearch": "" } 
				  	 });

					setTimeout(function(){ 
						$('input[aria-controls="example"]').attr("placeholder", "  Product Name, Brand, Item Group");
						$('#example_filter').append('<img src="/assets/shopchemical/images/magnifier.png" style=" height: 25px; margin-left: 10px; ">')

					},100);
	             	 // $('input[aria-controls="example"]').val("hcl")

				});
	            frappe.require(['/assets/shopchemical/js/jquery.dataTables.min.js',
	              '/assets/shopchemical/js/dataTables.bootstrap.min.css'], function() {
	              /*$('#patientTable').DataTable();*/
	              // $('#example').DataTable( {
	              // 	"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
	              //     responsive: true
	              // });
	              // $('#example').DataTable();
	            });
	          },500);
		}
	})
}

window.render_product_list = function(data) {
	var table = $("#search-list .table");
	if(data.length) {
		if(!table.length)
			var table = $("<table class='table table-bordered' id='example'><thead><tr><th>Product Name </th><th>Brand</th><th>Item Group</th><th>Available Stock</th><th>Price</th></tr></thead>").appendTo("#search-list");

		$.each(data, function(i, d) {
			$(d).appendTo(table);
		});
	}
	// if(data.length < 10) {
	// 	if(!table) {
	// 		$(".more-btn")
	// 			.replaceWith("<div class='alert alert-warning'>No products found.</div>");
	// 	} else {
	// 		$(".more-btn")
	// 			.replaceWith("<div class='text-muted'>Nothing more to show.</div>");
	// 	}
	// } else {
	// 	$(".more-btn").toggle(true)
	// }
	window.start += (data.length || 0);
}
