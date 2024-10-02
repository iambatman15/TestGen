def calculate_weightage(total_marks, sections, pyq_weightage):
    """
    Calculate the weightage of PYQs for each section.

    Args:
        total_marks (int): Total marks of the paper.
        sections (list): List of sections with marks and questions.
        pyq_weightage (int): Weightage of PYQs in percentage.

    Returns:
        list: Allocation of PYQs for each section.
    """
    pyq_total_marks = (pyq_weightage / 100) * total_marks
    pyq_total_questions = int((pyq_weightage / 100) * sum(section["num_questions"] for section in sections))

    section_pyq_allocation = []
    remaining_pyq_marks = pyq_total_marks
    remaining_pyq_questions = pyq_total_questions

    for section in sections:
        section_marks = section["marks"] * section["num_questions"]
        section_pyq_marks = (section_marks / total_marks) * pyq_total_marks
        section_pyq_questions = int((section_marks / total_marks) * pyq_total_questions)
        section_pyq_allocation.append({
            "section": section,
            "pyq_marks": section_pyq_marks,
            "pyq_questions": section_pyq_questions
        })
        remaining_pyq_marks -= section_pyq_marks
        remaining_pyq_questions -= section_pyq_questions

    # Adjust allocation to ensure total PYQ marks and questions match requirements
    for allocation in section_pyq_allocation:
        if remaining_pyq_marks > 0:
            allocation["pyq_marks"] += min(remaining_pyq_marks, allocation["pyq_marks"])
            remaining_pyq_marks -= min(remaining_pyq_marks, allocation["pyq_marks"])
        if remaining_pyq_questions > 0:
            allocation["pyq_questions"] += min(remaining_pyq_questions, allocation["pyq_questions"])
            remaining_pyq_questions -= min(remaining_pyq_questions, allocation["pyq_questions"])

    return section_pyq_allocation