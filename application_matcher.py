def normalize(text):
    if not text:
        return ""

    return text.lower().strip()

def applications_match(
        existing_company,
        existing_position,
        new_company,
        new_position
):
    if not existing_company or not new_company:
        return False

    company_match = (
        normalize(existing_company) == normalize(new_company)
    )

    if not existing_position or not new_position:
        return company_match

    position_match = (
        normalize(existing_position) == normalize(new_position)
    )

    return(
        company_match and position_match
    )