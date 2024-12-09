from dataclasses import dataclass
from typing import Any, Optional
from enum import Enum

class StatusCode(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

@dataclass
class Status:
    """
    A class to represent operation status with success/error information
    
    Attributes:
        code (StatusCode): The status code (SUCCESS or ERROR)
        message (str): A descriptive message about the operation result
        data (Any, optional): Any data that needs to be returned with the status
        error (Exception, optional): The exception object in case of errors
    """
    code: StatusCode
    message: str
    data: Optional[Any] = None
    error: Optional[Exception] = None

    @classmethod
    def success(cls, message: str = "Operation successful", data: Any = None) -> "Status":
        return cls(
            code=StatusCode.SUCCESS,
            message=message,
            data=data
        )

    @classmethod
    def error(cls, message: str = "Operation failed", error: Exception = None) -> "Status":
        return cls(
            code=StatusCode.ERROR,
            message=message,
            error=error
        )

    @property
    def is_success(self) -> bool:
        return self.code == StatusCode.SUCCESS

    @property
    def is_error(self) -> bool:
        return self.code == StatusCode.ERROR 