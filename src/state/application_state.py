from typing import TypedDict, Optional

class ApplicationState(TypedDict):
    resume_text: str
    job_description: str
    extracted_skills: list[str]
    missing_skills: list[str]
    recommended_edits: list[str]
    revised_resume: Optional[str]
    cover_letter: Optional[str]
    user_feedback: Optional[str]
    final_approved: bool
