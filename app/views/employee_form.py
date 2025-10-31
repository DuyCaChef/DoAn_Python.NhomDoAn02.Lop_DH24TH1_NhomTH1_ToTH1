"""Employee form wrapper around `gui/form_employee.py` if present."""
try:
    from ...gui import form_employee as original_form  # type: ignore
except Exception:
    original_form = None


def open_form():
    if original_form and hasattr(original_form, "open_form"):
        return original_form.open_form()
    print("Employee form placeholder - original gui.form_employee.open_form() not found")
