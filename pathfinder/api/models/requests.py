"""Inbound request models for PathFinder API."""

from pydantic import BaseModel, Field

from schemas.models import StudentSnapshot


class RoadmapRequest(BaseModel):
    snapshot: StudentSnapshot
    max_retries: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Maximum self-correction attempts for the Validation Agent",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "snapshot": {
                        "trees": "weak",
                        "dp": "very weak",
                        "arrays": "strong",
                        "graphs": "medium",
                        "recursion": "medium",
                        "binary_search": "medium",
                        "sorting": "strong",
                        "time_available_hours": 20,
                    },
                    "max_retries": 3,
                }
            ]
        }
    }
