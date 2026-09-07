"""Add active applicability guidance without rewriting retained modules.

Usage:
  python tools/zyr.py build
  python tools/zyr.py build --check
"""


def engine_addendum(engine: str) -> str:
    return (
        "> **Active applicability (resource profile v1):** Follow "
        "`boot/14_RESOURCE_PROPORTIONAL_EXECUTION_v1.md`. It scopes the blanket "
        "\"any task\" and mandatory companion language retained below. "
        "Select the protocol needed for the requested result; companion lists "
        "are navigation until a distinct obligation requires them. "
        "Local wording does not require a proof audit; mathematical validity "
        "does. Integrated manuscript work retains the relevant global checks. "
        f"Read only the applicable {engine} modules, and preserve their "
        "scientific and output contracts.\n"
    )
