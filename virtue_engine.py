"""
virtue_engine.py
=================

This module defines a framework for incorporating values inspired by the six
“spirits” (or virtues) described in Isaiah 11:2 into decision-making
agents.  The goal of this framework is to help AI systems align their
behaviour with human‑centric values such as wisdom, understanding, good
planning (counsel), strength, knowledge, and reverence.  The module is
organised around three main constructs:

* **VirtueState** – a simple data container capturing the degree to which
  each virtue is expressed in a given situation.
* **VirtueEngine** – an abstract base class that defines the interface for
  computing a VirtueState from context and filtering candidate actions
  according to that state.
* **Example implementations** – a reference implementation of a concrete
  VirtueEngine and a simple demonstration applying the engine to
  hypothetical research‑assistant actions.  These examples are not meant to
  be production‑ready but illustrate how the abstract interface can be
  extended.

The emphasis of this design is on modularity and reusability.  Any AI
agent, regardless of its domain, can integrate a VirtueEngine to shape
its behaviour.  A specific agent (e.g. a literature‑review assistant) can
provide a specialised subclass of VirtueEngine to handle its own context
and actions while still adhering to the common interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List, Tuple
from abc import ABC, abstractmethod


@dataclass
class VirtueState:
    """Represents the degree to which each virtue is activated in the current context.

    Each attribute is a float in the range [0.0, 1.0], where higher values
    indicate greater influence of the corresponding virtue on decision making.
    """

    wisdom: float
    understanding: float
    counsel: float
    strength: float
    knowledge: float
    reverence: float

    def normalised(self) -> "VirtueState":
        """Return a new VirtueState with values normalised to sum to 1.0.

        If all values are zero the original state is returned unchanged.
        """
        total = (
            self.wisdom
            + self.understanding
            + self.counsel
            + self.strength
            + self.knowledge
            + self.reverence
        )
        if total == 0:
            return self
        return VirtueState(
            wisdom=self.wisdom / total,
            understanding=self.understanding / total,
            counsel=self.counsel / total,
            strength=self.strength / total,
            knowledge=self.knowledge / total,
            reverence=self.reverence / total,
        )


class VirtueEngine(ABC):
    """Abstract base class for all virtue engines.

    A VirtueEngine analyses the current context and candidate actions of an
    agent and returns a filtered list of actions that align with the engine's
    virtues.  Subclasses must implement methods to evaluate the context
    (producing a VirtueState) and to filter actions in light of that state.
    """

    @abstractmethod
    def evaluate_context(self, context: Any) -> VirtueState:
        """Analyse the context and return a VirtueState.

        Subclasses should inspect the context (which can be of any type
        appropriate to the agent) and determine how strongly each virtue
        should influence decision‑making.  The returned VirtueState may be
        normalised if desirable.
        """
        raise NotImplementedError

    @abstractmethod
    def filter_actions(
        self,
        context: Any,
        actions: Iterable[Tuple[str, Any]],
        virtue_state: VirtueState,
    ) -> List[Tuple[str, Any]]:
        """Filter or rank candidate actions based on the virtue state.

        Args:
            context: The same context passed to evaluate_context().
            actions: An iterable of (action_name, action_payload) pairs
                representing the possible actions the agent might take.
            virtue_state: The VirtueState returned by evaluate_context().

        Returns:
            A list of (action_name, action_payload) pairs representing the
            allowed or recommended actions, potentially ordered by preference.
        """
        raise NotImplementedError


class ResearchAssistantVirtueEngine(VirtueEngine):
    """Example VirtueEngine for a literature‑review assistant.

    This implementation demonstrates one way to map a research context to
    virtue activation and how to filter actions accordingly.  It is not
    exhaustive: real systems would incorporate far more sophisticated
    heuristics and machine learning.
    """

    def evaluate_context(self, context: dict) -> VirtueState:
        """Compute the VirtueState for a research assistant.

        The context is expected to be a dictionary with at least the
        following keys:

        * ``task_stage``: A string indicating the current phase of
          research (e.g. "explore", "review", "synthesise").
        * ``deadline_hours``: Hours remaining until a deadline for the current
          deliverable (float or int).  Smaller values increase the
          importance of strength (execution) and counsel (planning).
        * ``information_density``: A float in [0, 1] measuring how much
          relevant information has already been gathered (1.0 means fully
          saturated).  Low values boost knowledge and exploration; high
          values boost wisdom (synthesis) and reverence (caution against
          overload).
        """
        stage = context.get("task_stage", "explore")
        deadline_hours = float(context.get("deadline_hours", 24.0))
        info_density = float(context.get("information_density", 0.0))

        # Base levels for each virtue
        base = VirtueState(
            wisdom=0.1,
            understanding=0.1,
            counsel=0.1,
            strength=0.1,
            knowledge=0.1,
            reverence=0.1,
        )

        # Adjust for stage of research
        if stage == "explore":
            base.knowledge += 0.3  # gather more information
            base.understanding += 0.1
        elif stage == "review":
            base.wisdom += 0.3  # synthesize patterns
            base.knowledge += 0.1
            base.understanding += 0.2
        elif stage == "synthesise":
            base.wisdom += 0.4
            base.counsel += 0.1
            base.reverence += 0.1

        # Adjust for deadlines (imminent deadlines favour strength and counsel)
        if deadline_hours < 1:
            base.strength += 0.4
            base.counsel += 0.3
        elif deadline_hours < 8:
            base.strength += 0.2
            base.counsel += 0.2

        # Adjust for information density (how saturated is the field)
        # When little information is available, push exploration (knowledge).  When
        # much information has been gathered, increase wisdom and reverence to
        # avoid overfitting and maintain critical thinking.
        base.knowledge += max(0.0, 0.3 * (1 - info_density))
        base.wisdom += max(0.0, 0.2 * info_density)
        base.reverence += max(0.0, 0.2 * info_density)

        return base.normalised()

    def filter_actions(
        self,
        context: dict,
        actions: Iterable[Tuple[str, Any]],
        virtue_state: VirtueState,
    ) -> List[Tuple[str, Any]]:
        """Filter and rank actions for a research assistant.

        This implementation uses simple heuristics based on virtue weights:

        * Actions related to **collecting new sources** are boosted by the
          knowledge and understanding virtues.
        * Actions that involve **planning or summarising** are boosted by the
          wisdom and counsel virtues.
        * Actions that require **fast execution** (e.g. generating a draft)
          are boosted by strength.
        * Actions are penalised (or suppressed) if they conflict with
          reverence (e.g. suggesting questionable sources or unethical
          shortcuts).

        Returns a sorted list of actions by score.
        """
        scored: List[Tuple[float, Tuple[str, Any]]] = []
        for name, payload in actions:
            score = 0.0
            lname = name.lower()

            # Assign heuristics: this is intentionally simplistic and serves
            # illustrative purposes.  Real systems might use ML models to
            # score actions based on historical outcomes.
            if "collect" in lname or "search" in lname:
                score += virtue_state.knowledge * 0.6
                score += virtue_state.understanding * 0.4
            if "summarise" in lname or "synthesize" in lname:
                score += virtue_state.wisdom * 0.5
                score += virtue_state.counsel * 0.3
                score += virtue_state.understanding * 0.2
            if "plan" in lname or "decide" in lname:
                score += virtue_state.counsel * 0.5
                score += virtue_state.wisdom * 0.3
            if "draft" in lname or "write" in lname:
                score += virtue_state.strength * 0.6
                score += virtue_state.wisdom * 0.4

            # Penalise risky actions if reverence is high
            if "auto" in lname or "unstable" in lname:
                score -= virtue_state.reverence * 0.5
            # Always ensure score is non‑negative
            score = max(0.0, score)
            scored.append((score, (name, payload)))

        # Sort by descending score; preserve input order for tie breaking
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [pair for _, pair in scored]


def demo() -> None:
    """Demonstration of the ResearchAssistantVirtueEngine in action.

    This function constructs a hypothetical research context and a list of
    candidate actions and shows how the virtue engine scores and orders
    them.  Run this function directly to see sample output.
    """
    context = {
        "task_stage": "review",
        "deadline_hours": 5,
        "information_density": 0.7,
    }
    actions = [
        ("collect_more_papers", None),
        ("summarise_current_findings", None),
        ("plan_next_steps", None),
        ("write_draft_outline", None),
        ("auto_generate_full_paper", None),
    ]
    engine = ResearchAssistantVirtueEngine()
    state = engine.evaluate_context(context)
    ordered = engine.filter_actions(context, actions, state)

    print("Context:")
    print(context)
    print("\nComputed virtue state:")
    print(state)
    print("\nAction rankings:")
    for i, (name, _) in enumerate(ordered, start=1):
        print(f"{i}. {name}")


if __name__ == "__main__":
    demo()
