from abc import ABC, abstractmethod
from typing import List
from dj_inspector.utils.constants import SecurityCheckResult


class SecurityChecker(ABC):
    @abstractmethod
    def run_check(self) -> List[SecurityCheckResult]:
        pass
