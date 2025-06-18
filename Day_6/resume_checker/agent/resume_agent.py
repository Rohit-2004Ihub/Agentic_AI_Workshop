import json
from tools.extractor import extract_resume_entities
from tools.company_verifier import verify_companies
from tools.timeline_validator import validate_timeline
from tools.scorer import score_resume

def clean_json_string(text: str) -> str:
    """Clean LLM output that may contain markdown (```json ... ```) and return pure JSON."""
    text = text.strip()

    # Remove markdown ```json or ```
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return text

def extract_company_list(json_str: str) -> str:
    """
    Extracts unique company names from a list of job experiences.
    Returns: JSON string like: [{"company": "Google"}, {"company": "OpenAI"}]
    """
    try:
        data = json.loads(json_str)

        # ✅ Ensure the format is a list
        if not isinstance(data, list):
            return json.dumps({"error": "Expected a list of company objects."})

        companies = set()
        for exp in data:
            company = exp.get("company")
            if company:
                companies.add(company.strip())

        return json.dumps([{"company": c} for c in companies])

    except Exception as e:
        return json.dumps({"error": f"Company extraction failed: {str(e)}"})

def run_resume_validation(resume_text: str):
    # Step 1: Extract Entities
    extracted_entities = extract_resume_entities.invoke(resume_text)
    extracted_entities = clean_json_string(extracted_entities)

    # Step 2: Extract and verify company list
    company_list_json = extract_company_list(extracted_entities)
    company_verification = verify_companies.invoke(company_list_json)
    company_verification = clean_json_string(company_verification)

    # Step 3: Validate Timeline
    timeline_validation = validate_timeline.invoke(extracted_entities)
    timeline_validation = clean_json_string(timeline_validation)

    # Step 4: Score Resume
    final_score_report = score_resume.invoke({
        "extracted_entities": extracted_entities,
        "company_check": company_verification,
        "timeline_report": timeline_validation
    })

    return extracted_entities, company_verification, timeline_validation, final_score_report
