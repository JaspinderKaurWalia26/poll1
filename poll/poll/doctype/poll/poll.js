frappe.ui.form.on("Poll", "refresh", function (frm) {
	frm.add_custom_button(__('Make Copy'), function() {
		frm.copy_doc();
	});
});
