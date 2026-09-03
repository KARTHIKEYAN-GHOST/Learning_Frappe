# Copyright (c) 2026, Karthikeyan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ToDoo(Document):
    pass


frappe.whitelist()


def todoo_task(doc):
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
        frappe.qb.fron_(todoo)
        .left_join(user)
        .on(todoo.owner == user.name)
        .select(todoo.name, todoo.description, user.email)
        .limit(5)
    ).run(as_dict=True)

    rows2 = frappe.db.sql(
        """
			select name, description
            from `tabToDoo`
            order by creation desc
            limlit %(limit)s
		""",
        {"limit": 5},
        as_dict=True,
    )

    return{
        doc,
        rows1,
        rows2
	}