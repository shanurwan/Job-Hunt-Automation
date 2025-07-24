from fpdf import FPDF
from pathlib import Path

def generate_resume_pdf(job_row, template_str, output_dir):
    title = job_row.get("title", "Unknown Role")
    company = job_row.get("company", "Unknown Company")
    skills = job_row.get("top_keywords", [])
    skills_str = ", ".join(skills) if isinstance(skills, list) else str(skills)

    # Fill template placeholders
    filled = template_str.replace("{{job_title}}", title)
    filled = filled.replace("{{company}}", company)
    filled = filled.replace("{{skills_section}}", f"Key Skills: {skills_str}")

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in filled.split("\n"):
        pdf.multi_cell(0, 10, line)

    # Save PDF
    safe_filename = f"{title}-{company}.pdf".replace(" ", "_").replace("/", "-")
    pdf_path = Path(output_dir) / safe_filename
    pdf.output(str(pdf_path))

    return pdf_path
