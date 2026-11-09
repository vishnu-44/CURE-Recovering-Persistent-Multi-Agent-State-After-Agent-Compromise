"""Minimal queue-driven persistent multi-agent workflow.

There is no turn-count ceiling: execution ends only when the message queue is
empty or the caller/model provider raises an error.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Protocol

from models import AgentState, Record


@dataclass(frozen=True)
class Message:
    receiver: str
    record_ids: tuple[str, ...]


@dataclass(frozen=True)
class Write:
    state_type: str
    text: str


@dataclass(frozen=True)
class Send:
    receiver: str
    text: str


@dataclass(frozen=True)
class Action:
    writes: tuple[Write, ...] = ()
    sends: tuple[Send, ...] = ()


class AgentPolicy(Protocol):
    def __call__(
        self,
        agent_id: str,
        incoming: tuple[Record, ...],
        local_state: tuple[Record, ...],
        candidate_agents: tuple[str, ...],
    ) -> Action: ...


class Workflow:
    def __init__(self, agent_ids: list[str], policy: AgentPolicy) -> None:
        self.states = {agent_id: AgentState(agent_id) for agent_id in agent_ids}
        self.records: dict[str, Record] = {}
        self.queue: deque[Message] = deque()
        self.policy = policy
        self.turns_executed = 0
        self._next_record = 1

    def add_root(self, record: Record, receiver: str) -> None:
        if record.derived_from:
            raise ValueError("A root record cannot have parents")
        self.records[record.record_id] = record
        self.states[receiver].records.append(record)
        self.queue.append(Message(receiver, (record.record_id,)))

    def _store(
        self,
        writer: str,
        state_type: str,
        text: str,
        parents: tuple[str, ...],
    ) -> Record:
        record = Record(
            record_id=f"r{self._next_record}",
            writer=writer,
            state_type=state_type,
            text=text,
            derived_from=parents,
        )
        self._next_record += 1
        self.records[record.record_id] = record
        self.states[writer].records.append(record)
        return record

    def run_until_idle(self) -> None:
        while self.queue:
            message = self.queue.popleft()
            if message.receiver not in self.states:
                raise ValueError(f"Unknown receiver: {message.receiver}")
            incoming = tuple(self.records[item] for item in message.record_ids)
            peers = tuple(agent for agent in self.states if agent != message.receiver)
            action = self.policy(
                message.receiver,
                incoming,
                tuple(self.states[message.receiver].records),
                peers,
            )
            self.turns_executed += 1
            written = tuple(
                self._store(message.receiver, item.state_type, item.text, message.record_ids)
                for item in action.writes
            )
            parents = message.record_ids + tuple(item.record_id for item in written)
            for item in action.sends:
                if item.receiver not in peers:
                    raise ValueError(f"Invalid downstream receiver: {item.receiver}")
                sent = self._store(message.receiver, "memory", item.text, parents)
                self.queue.append(Message(item.receiver, (sent.record_id,)))
