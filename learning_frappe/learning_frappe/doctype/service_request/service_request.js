// Copyright (c) 2026, Karthikeyan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Service Request", {
	refresh(frm) {
		if (!frm.is_new()) {
			// frm.add_custom_button("Start Work", async () => {
			// 	await frm.set_value("status", "In Progress");
			// 	await frm.save();
			// });
			frm.add_custom_button("Start Work", () => {
				frm.set_value("status", "In Progress");
				frm.save();
			});
			frm.add_custom_button("Fill Contact", () => {
				get_first_name(frm);
			});
			frm.add_custom_button("Add new Service Request", () => {
				add_new_service_request();
			});
		}
	},

	validate(frm) {
		// crud_op(frm);
		call_enqueue();
	},

	after_save(frm) {
		// create_service_request(frm);
	},
});

function crud_op(frm) {
	const row = frm.add_child("items");
	row.item_code = "SERVICE-HOUR";
	row.qty = 2;
	row.rate = 500;
	row.amount = row.qty * row.rate;
	frm.refresh_field("items");
}

function create_service_request(frm) {
	frappe.call({
		method: "learning_frappe.learning_frappe.events.api.create_service_request",

		callback: function (r) {
			if (r.message.success && r.message.success === true) {
				frappe.msgprint({
					title: "Doc Created",
					message: `${r.message.doc}`,
				});
			}
		},
	});
}
function get_first_name(frm) {
	const dialog = new frappe.ui.Dialog({
		title: "New Contact",
		fields: [{ fieldname: "first_name", label: __("First Name"), fieldtype: "Data", reqd: 1 }],
		primary_action_label: "Continue",
		primary_action(values) {
			dialog.hide();
			frappe.route_options = { first_name: values.first_name };
			frappe.new_doc("Contact");
		},
	});

	dialog.show();
}

function add_new_service_request() {
	const dialog = new frappe.ui.Dialog({
		title: __("Create Service Request"),
		fields: [
			{
				fieldname: "subject",
				label: "Subject",
				fieldtype: "Data",
				reqd: 1,
			},
			{
				fieldname: "customer_name",
				label: "Customer Name",
				fieldtype: "Data",
				reqd: 1,
			},
		],
		primary_action_label: "Create",
		async primary_action(values) {
			const response = await frappe.call({
				method: "learning_frappe.learning_frappe.events.api.add_new_service_request",
				type: "POST",
				args: {
					subject: values.subject,
					customer_name: values.customer_name,
				},
				freeze: true,
				freeze_message: "Creating request...",
			});
			dialog.hide();
			console.log(response);
			console.log(response.message);
			frappe.msgprint({
				title: "Created",
				message: `Service Request ${response.message.doc} was created.`,
				indicator: "green",
			});
		},
	});

	dialog.show();
}

function call_enqueue() {
	frappe.call({
		method: "learning_frappe.utils.scheduler.call_enqueue",
	});
}

frappe.realtime.on("request_recalculated", (data) => {
	frappe.show_alert({ message: __("Updated"), indicator: "green" });
});
