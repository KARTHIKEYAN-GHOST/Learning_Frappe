import frappe
from frappe.rate_limiter import rate_limit
from frappe.utils import getdate, today


@frappe.whitelist()
def todoo_task():
    doc = frappe.get_list(
        "ToDoo",
        fields={"name", "description", "owner"},
        order_by="creation desc",
        limit_page_length=5,
    )

    for todoo in doc:
        todoo.owner_email = frappe.db.get_value("User", todoo.owner, "email")

    todoo = frappe.qb.DocType("ToDoo")
    user = frappe.qb.DocType("User")

    rows1 = (
        frappe.qb.from_(todoo)
        .left_join(user)
        .on(todoo.owner == user.name)
        .select(todoo.name, todoo.description, user.email)
        .limit(5)
    ).run(as_dict=True)

    doc = frappe.get_doc("ToDoo")
    if not doc.description:
        doc.description = "Default Description."
    doc.save(ignore_permissions=True)

    if getdate(doc.due_date) < getdate(today()):
        frappe.db.set_value(status="Closed")

    rows2 = frappe.db.sql(
        """
			select name, description
            from `tabToDoo`
            order by creation desc
            limit %(limit)s
		""",
        {"limit": 5},
        as_dict=True,
    )

    return {"success": True, "doc": doc, "rows1": rows1, "date": frappe.utils.now()}


@frappe.whitelist(methods=["POST"])
def create_service_request(subject="Created using POST API"):
    if not subject:
        frappe.throw("Subject is required.")

    doc = frappe.new_doc("Service Request")
    doc.subject = subject
    doc.customer_name = frappe.session.user
    doc.append("items", {"item_code": "SERVICE-HOUR", "qty": 5, "rate": 800})
    doc.insert(ignore_permissions=True)
    return {"success": True, "doc": doc.name}


# curl -X GET 'http://learning.site:8000/api/method/learning_frappe.learning_frappe.events.api.limited_greeting'
@frappe.whitelist(allow_guest=True, methods=["GET"])
@rate_limit(key="limited_greeting", limit=5, seconds=60)
def limited_greeting():
    frappe.logger("learning_frappe.api").info("Limited Greeting Called")
    return {"message": "Hello, Greeting from Rate Limit."}


@frappe.whitelist()
def add_new_service_request(subject, customer_name):
    doc = frappe.new_doc("Service Request")
    doc.subject = subject
    doc.customer_name = customer_name
    doc.append("items", {"item_code": "SERVICE-HOUR", "qty": 5, "rate": 800})
    doc.insert(ignore_permissions=True)
    return {"doc": doc.name}
