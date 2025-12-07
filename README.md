VirtueEngine Framework
Purpose
This document accompanies the virtue_engine.py module and outlines a high‑level design for
incorporating six virtues inspired by Isaiah 11:2 into machine‑decision processes. The goal is to provide
a general framework that can be adopted across different types of agents—such as literature‑review
assistants, conversational bots or task planners—to align their behaviour with values like wisdom,
understanding, planning, strength, knowledge and reverence.
Design Overview
VirtueState
The VirtueState dataclass encapsulates six floating‑point values corresponding to the six virtues.
Each value lies in the range [0, 1] . The normalised method optionally scales the values so that
they sum to one. This normalisation can be useful when treating the virtues as a soft probability
distribution over behavioural emphases.
VirtueEngine (abstract base class)
VirtueEngine is an abstract base class defining two core methods:
1.
2.
evaluate_context(context) -> VirtueState : examines the agent’s context and returns a
VirtueState describing how strongly each virtue should influence behaviour in that situation.
The type of context is left flexible to accommodate different domains.
filter_actions(context, actions, virtue_state) -> List[(str, Any)] : accepts a
list of candidate actions (as (name, payload) tuples) and returns an ordered or filtered list of
actions based on the computed VirtueState . Subclasses can implement domain‑specific
scoring or filtering strategies.
Any agent can integrate a virtue engine by first computing a then passing both the context and its candidate actions through the VirtueState from its current context and
filter_actions method.
Example: ResearchAssistantVirtueEngine
The concrete class ResearchAssistantVirtueEngine demonstrates how VirtueEngine can be
specialised for a literature‑review assistant. It illustrates several key ideas:

Context interpretation: the engine reads keys such as task_stage, deadline_hours and
information_density to adjust virtue weights.
Stage‑dependent emphasis:
During an explore stage, knowledge is prioritised to gather more sources.
During review or synthesis, wisdom and understanding are given greater weight.
As deadlines approach, strength (execution) and counsel (planning) are emphasised.
Heuristic action scoring: the engine assigns scores to candidate actions based on how they relate
to each virtue (e.g. collection actions benefit from high knowledge and understanding; synthesis
actions from wisdom and counsel; drafting from strength). Risky actions (such as uncontrolled
auto‑generation) are penalised when reverence is high.
Although simplistic, this example shows how the six virtues can be mapped to specific behaviours and
how an agent might reorder its actions accordingly.
Usage
To adopt the framework:
Create a subclass of VirtueEngine for your specific agent.
Implement evaluate_context to interpret the agent’s context and return a VirtueState
with appropriate weights.
Implement filter_actions to score or filter candidate actions based on the computed virtue
state. Maintain modularity so that the scoring logic can be reused across agents.
In your agent’s decision loop, invoke these methods:
engine = MyVirtueEngine()
state = engine.evaluate_context(current_context)
allowed_actions = engine.filter_actions(current_context, candidates, state)
next_action = allowed_actions[0] # choose the highest‑ranked action
For a demonstration, run the module directly:
python3 virtue_engine.py
which will output a sample context, the computed virtue state and the ranking of example actions.
