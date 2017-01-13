
// frappe.ready(function() {
// 	// update user
// 	$("#item-add-to-cart button").on("click", function() {
// 			console.log(23123);
// 		});
// });
$(document).ready(function(){

	setTimeout(function(){ 
		$("#item-add-to-cart button").on("click", function() {
			console.log($(this).attr("data-get-itemcode"));
			var me = $(this);
			var itemQty = parseInt(me.parent().parent().parent().parent().find("input").val());
			//console.log(parseInt(me.parent().parent().parent().find("input").val()));
			shopping_cart.update_cart({
				item_code: me.attr("data-get-itemcode"),
				qty: itemQty,
				callback: function(r) {
					if(!r.exc) {
						toggle_update_cart(1);
						qty = 1;
					}
					me.parent().parent().parent().parent().find(".addToCart").css("display","none");
					me.parent().parent().parent().parent().find(".goToCart").css("display","block");
				},
				btn: this,
			});
		}); 
	}, 3000);
	
});

var toggle_update_cart = function(qty) {
	$("#item-add-to-cart").toggle(qty ? false : true);
	$("#item-update-cart")
		.toggle(qty ? true : false)
		.find("input").val(qty);
}