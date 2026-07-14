from dataclasses import dataclass

@dataclass
class Job:
    """Represents a normalized job listing."""
    company: str
    role: str
    location: str
    apply_url: str
    source: str
