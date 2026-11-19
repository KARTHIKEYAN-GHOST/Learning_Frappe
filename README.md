# Learning Frappe

`learning_frappe` is a Frappe Framework application used to explore framework concepts through small DocTypes, controller hooks, whitelisted methods, query examples, and website pages. It is a learning codebase rather than a packaged end-user product.

## What is included

The app defines a `Learning Frappe` module with examples including:

- **Item** — a simple DocType with an item code.
- **Service Request** — a request record with subject, customer, status, requested date, description, item rows, and total amount.
- **Service Request Item** — child-table fields for item code, description, quantity, rate, and amount.
- **ToDoo** — a small task-like DocType with description, due date, and status.
- **Print format and report** — a Service Request print format and report definition.
- **Website page** — a request page that loads Service Request records.
- **Document event example** — validation for ToDoo descriptions.
- **API examples** — whitelisted methods for creating service requests, querying ToDoo records, and a rate-limited guest greeting.

The API module also demonstrates several Frappe access patterns, including `frappe.get_list`, `frappe.get_doc`, `frappe.new_doc`, query builder joins, and SQL queries. Some snippets are deliberately experimental and should be reviewed before use in a real application.

## Technology

- Frappe Framework v16 app structure
- Python
- Frappe DocTypes, hooks, website routes, reports, and print formats
- JavaScript for DocType client scripts
- `flit_core` build backend
- Ruff, ESLint, Prettier, and pre-commit configuration

The `pyproject.toml` specifies Python `>=3.14`; Frappe itself is expected to be installed and managed by Bench.

## Install into an existing Frappe bench

Prerequisites: a working Frappe v16 bench and a site on that bench.

```bash
cd /path/to/frappe-bench
bench get-app https://github.com/KARTHIKEYAN-GHOST/Learning_Frappe.git --branch version-16
bench --site your-site-name install-app learning_frappe
bench --site your-site-name migrate
```

Replace `your-site-name` with the actual site name. If the repository branch differs, use the branch that matches the Frappe version in your bench.

## Development

```bash
cd /path/to/frappe-bench
bench start
```

For code-quality hooks, install the configured pre-commit hooks from the app directory:

```bash
cd apps/learning_frappe
pre-commit install
```

## API examples

Frappe whitelisted methods are exposed through the standard `/api/method/...` route. For example, the rate-limited greeting is declared in `learning_frappe.learning_frappe.events.api.limited_greeting`. A guest GET request can be made against:

```text
/api/method/learning_frappe.learning_frappe.events.api.limited_greeting
```

The `create_service_request` method is restricted to POST in its decorator. Review permissions and the `ignore_permissions=True` calls before exposing write operations.

## Important notes

This repository contains learning experiments, not a hardened production app. Review the SQL example, permissions, document creation behavior, and any experimental snippets before deploying.
