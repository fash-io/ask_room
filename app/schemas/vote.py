from pydantic import BaseModel, validator
from uuid import UUID
from enum import Enum
from typing import Optional


class VoteValue(str, Enum):
    down = "down"
    up = "up"


class VoteCreate(BaseModel):
    question_id: Optional[UUID] = None
    answer_id: Optional[UUID] = None
    vote_value: VoteValue

    @validator("question_id", "answer_id")
    def validate_ids(cls, v, values, **kwargs):
        # Ensure at least one ID is provided
        field = kwargs.get("field")
        if field.name == "answer_id" and not v and not values.get("question_id"):
            raise ValueError("Either question_id or answer_id must be provided")
        if field.name == "question_id" and not v and not values.get("answer_id"):
            raise ValueError("Either question_id or answer_id must be provided")
        return v

    class Config:
        from_attributes = True

        @classmethod
        def __call__(cls, request):
            # This is a dependency that extracts vote data from path parameters
            question_id = request.path_params.get("question_id")
            answer_id = request.path_params.get("answer_id")

            # Get vote_value from request body
            body = request.json()
            vote_value = body.get("vote_value", "up")  # Default to upvote

            return cls(
                question_id=question_id if question_id != "None" else None,
                answer_id=answer_id if answer_id != "None" else None,
                vote_value=vote_value,
            )


class VoteOut(BaseModel):
    user_id: UUID
    vote_value: VoteValue

    class Config:
        from_attributes = True



class VoteOutList(BaseModel):
    votes: list[VoteOut]
