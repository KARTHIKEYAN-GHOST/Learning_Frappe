import frappe


def validate_todoo(doc, method = None):
    if not doc.description:
        frappe.throw("Fill the Description Field.")
