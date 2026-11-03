import frappe
from frappe.utils import now_datetime


def get_context(context):
    context.no_cache = 1
    context.cache_buster = int(now_datetime().timestamp())