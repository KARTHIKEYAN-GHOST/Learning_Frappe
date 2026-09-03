// Copyright (c) 2026, Karthikeyan and contributors
// For license information, please see license.txt

frappe.ui.form.on("ToDoo", {
	before_validate(frm) {
		todoo_task(frm);
	},
});

function todoo_task(frm) {
	frappe.call({
		method: "learning_frappe.learning_frappe.events.api.todoo_task",
		callback(r) {
			if(r.message.success && r.message.success === true){
			console.log(r.message.doc);
			}
		},
	});
}