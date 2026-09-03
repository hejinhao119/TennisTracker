from evidence.schemas import EvidenceReport

from .biomechanics import BiomechanicsAgent
from .coach import CoachAgent
from .critic import CoachCriticAgent
from .match_analysis import MatchAnalysisAgent
from .schemas import CoachingRun
from .tactical import TacticalAnalysisAgent


def run_coaching_analysis(evidence: EvidenceReport, max_retries: int = 2) -> CoachingRun:
    """Run specialists, synthesize, and critique with a bounded revision budget."""
    reports = (
        MatchAnalysisAgent().analyze(evidence),
        BiomechanicsAgent().analyze(evidence),
        TacticalAnalysisAgent().analyze(evidence),
    )
    coach = CoachAgent()
    critic = CoachCriticAgent()
    attempts = 0
    while True:
        attempts += 1
        coach_report = coach.synthesize(evidence, reports)
        critic_report = critic.review(coach_report)
        if critic_report.approved or attempts > max_retries:
            return CoachingRun(*reports, coach_report, critic_report, attempts)