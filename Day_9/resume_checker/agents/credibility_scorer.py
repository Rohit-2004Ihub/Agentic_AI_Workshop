def score_resume(entities, company_check, timeline_flags):
    score = 100
    flags = []

    for company, status in company_check.items():
        if status != "Exists":
            score -= 15
            flags.append(f"Company '{company}' not found")

    for flag in timeline_flags:
        score -= 10
        flags.append(flag)

    if len(entities.get("work_experience", [])) < 2:
        score -= 20
        flags.append("Insufficient experience entries")

    return {"score": max(score, 0), "flags": flags}
