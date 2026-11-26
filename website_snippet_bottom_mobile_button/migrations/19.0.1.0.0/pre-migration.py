# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade

OLD = "website_mobile_button"
NEW = "website_snippet_bottom_mobile_button"


@openupgrade.migrate()
def migrate(env, version):
    # Website-specific views (COW copies and the oe_structure view created
    # when the bar is edited) have no XML-ID, so renaming the module does
    # not update their key.
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_ui_view
        SET key = %(new)s || substr(key, length(%(old)s) + 1)
        WHERE left(key, length(%(old)s) + 1) = %(old)s || '.'
        """,
        {"old": OLD, "new": NEW},
    )
    # In 18.0 this view inherited website.snippet_options, which no longer
    # exists in 19.0 (the options are now a builder plugin).
    openupgrade.delete_records_safely_by_xml_id(env, [f"{NEW}.snippet_options"])
