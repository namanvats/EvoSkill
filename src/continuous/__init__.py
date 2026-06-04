"""Continuous evolution: learn skills from real agent usage traces.

Phase 0 surface — trace ingestion:

* `TaskEpisode` / `ActionStep` / `ToolCall` — normalized usage unit.
* `OutcomeSignal` / `Outcome` / `SignalKind` — how an attempt's success is judged.
* Readers: `HarborTrajectoryReader` (primary, ATIF), `GooseRawReader` (fallback),
  `JsonlReader` (generic).
* `TraceCollector` + `TraceCursor` — dedup + watermark across continuous ticks.

See `plan.md` for the full continuous-evolution design.
"""

from .episode import (
    ActionStep,
    Outcome,
    OutcomeSignal,
    SignalKind,
    TaskEpisode,
    ToolCall,
)
from .signals import clamp01, no_signal, signal_from_reward
from .collector import (
    GooseRawReader,
    HarborTrajectoryReader,
    JsonlReader,
    TraceCollector,
    TraceCursor,
    TraceReader,
    TraceReadError,
    parse_atif_trajectory,
    read_reward_file,
)
from .cluster import EpisodeCluster, cluster_episodes
from .candidates import Candidate, CandidateStore, make_candidate_id
from .harvest import (
    HarvestResult,
    build_distiller_query,
    build_readers,
    harvest,
    slugify_skill_name,
)

__all__ = [
    # episode model
    "ActionStep",
    "Outcome",
    "OutcomeSignal",
    "SignalKind",
    "TaskEpisode",
    "ToolCall",
    # signals
    "clamp01",
    "no_signal",
    "signal_from_reward",
    # collector
    "GooseRawReader",
    "HarborTrajectoryReader",
    "JsonlReader",
    "TraceCollector",
    "TraceCursor",
    "TraceReader",
    "TraceReadError",
    "parse_atif_trajectory",
    "read_reward_file",
    # clustering
    "EpisodeCluster",
    "cluster_episodes",
    # candidates
    "Candidate",
    "CandidateStore",
    "make_candidate_id",
    # harvest
    "HarvestResult",
    "build_distiller_query",
    "build_readers",
    "harvest",
    "slugify_skill_name",
]
