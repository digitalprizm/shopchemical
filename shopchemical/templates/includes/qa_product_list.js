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
				search: window.search,
				item_group: window.item_group,
				brand: window.brand,
				product_group: window.product_group
			},
		dataType: "json",
		success: function(data) {
			$(".item-search").hide();
			window.render_product_list(data.message || []);
			    setTimeout(function(){ 
				$.getScript( "http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.0/jquery.dataTables.min.js", function( data, textStatus, jqxhr ) {
				  console.log( data ); // Data returned
				  console.log( textStatus ); // Success
				  console.log( jqxhr.status ); // 200
				  console.log( "Load was performed." );

				  	              $('#example').DataTable();

				});
	            frappe.require(['/assets/shopchemical/js/jquery.dataTables.min.js',
	              '/assets/shopchemical/js/dataTables.bootstrap.min.css'], function() {
	              /*$('#patientTable').DataTable();*/
	              $('#example').DataTable( {
	                  responsive: true
	              });
	              $('#example').DataTable();
	            });
	          },500);
		}
	})
}

window.render_product_list = function(data) {
	var table = $("#search-list .table");
	if(data.length) {
		if(!table.length)
			var table = $("<table class='table' id='example'><thead><tr><th>Product Name </th><th>Brand</th><th>Item Group</th><th>Available Stock</th><th>Price</th></tr></thead>").appendTo("#search-list");

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
