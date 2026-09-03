from abc import ABC, abstractmethod

from evidence.schemas import EvidenceReport

from .schemas import AgentReport


class AnalysisAgent(ABC):
    name: str

    @abstractmethod
    def analyze(self, evidence: EvidenceReport) -> AgentReport:
        raise NotImplementedError