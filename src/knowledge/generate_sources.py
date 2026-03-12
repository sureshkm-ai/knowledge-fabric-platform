from pathlib import Path


def generate_docs(output_dir: str = "data/knowledge") -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    docs = {
        "approval_policy.md": "# Approval Policy\nAll allocation overrides above 12% require regional director approval.",
        "allocation_override_sop.md": "# Allocation Override SOP\nStep 1 validate inventory status. Step 2 submit request.",
        "promotion_planning_playbook.md": "# Promotion Planning\nUse lift baselines by category and region.",
        "basket_size_analysis_guide.md": "# Basket Size Guide\nSegment by mission type and income clusters.",
        "inventory_remediation_sop.md": "# Inventory Remediation\nEscalate risk SKUs under 7 days cover.",
        "analyst_note_tx_snack_decline.md": "# Analyst Note\nTexas snack sales declined 8% post promo exhaustion.",
        "metric_dictionary_narrative.md": "# Metrics Narrative\nReturn rate and net sales definitions are governed by Finance Analytics.",
    }
    for name, content in docs.items():
        (out / name).write_text(content)


if __name__ == "__main__":
    generate_docs()
