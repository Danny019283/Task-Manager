from dataclasses import dataclass
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateTaskDTO(BaseModel):
    description: str
    date_limit: datetime
    
class UpdateTaskDTO(BaseModel):
    id: int
    description: Optional[str] = None
    date_limit: Optional[datetime] = None
    is_completed: Optional[bool] = None
    
class CompleteTaskDTO(BaseModel):
    id: int
    is_completed: bool = True
    
class DeleteTaskDTO(BaseModel):
    id: int
    
class TaskResponseDTO(BaseModel):
    id: int
    description: str
    date_limit: datetime
    is_completed: bool