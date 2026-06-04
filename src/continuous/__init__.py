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
]
