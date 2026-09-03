import frappe


def get_context(context):
    context.title = "Service Request"
    context.no_cache = True
    context.requests = frappe.get_list(
        "Service Request",
        fields=["name"],
        page_length=20,
    )
