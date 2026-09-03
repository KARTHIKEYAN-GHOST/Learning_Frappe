# Copyright (c) 2026, Karthikeyan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceRequest(Document):

    def before_insert(self):
        if not self.description:
            self.description = "Default Description."

    def before_validate(self):
        if not self.items:
            frappe.throw("Add atleast One Item in Items.")

    def validate(self):
        # self.subject = "Printer maintenance"
        # self.customer_name = "Sample Customer"
        # self.append(
        #     "items",
        #     {
        #         "item_code": "SERVICE-HOUR",
        #         "qty": 2,
        #         "rate": 1000,
        #     },
        # )

        # first_row = self.get("items")[0]
        # first_row.qty = 3

        self.calculate_amount()

        # if self.status == "In Progress":
        #     create_doc()

    def calculate_amount(self):
        total = 0
        for item in self.items:
            item.amount = item.qty * item.rate
            total += item.amount
        self.total_amount = total


def create_doc():
    doc = frappe.new_doc("Service Request")
    doc.subject = "Progressing Doc"
    doc.customer_name = "Sample Customer"
    doc.append("items", {"item_code": "SERVICE-HOUR", "qty": 5, "rate": 800})
    doc.insert(ignore_permissions=True)
