import frappe


def daily_maintenance():
    frappe.logger("learning_app.scheduler").info("Daily maintenance completed")

@frappe.whitelist()
def call_enqueue():
    frappe.enqueue(
        "learning_frappe.utils.scheduler.recalculate_requests",
        queue="default",
        enqueue_after_commit=True,
        job_name="recalculate-service-requests",
    )

@frappe.whitelist()
def recalculate_requests():
    frappe.logger("learning_app.background_job").info("Enqueue completed")
    frappe.publish_realtime(
        "request_recalculated",
        user=frappe.session.user,
    )
