// Copyright (c) 2026, Karthikeyan and contributors
// For license information, please see license.txt

frappe.ui.form.on("ToDoo", {
	after_save(frm) {
		todoo_task(frm);
	},
});

function todoo_task(frm) {
	frappe.call({
		method: "learning_frappe.learning_frappe.doctype.todoo.todoo.todoo_task",
		args: {
			doc: frm.doc.name,
		},
		callback(r) {
			console.log(r.message);
		},
	});
}