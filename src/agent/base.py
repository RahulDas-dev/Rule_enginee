from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Protocol, runtime_checkable

MemberType = Literal["Actor", "Critique"]


@runtime_checkable
class BaseMember(Protocol):
    """(In preview) A protocol for Agent.

    An agent can communicate with other agents and perform actions.
    Different agents can differ in what actions they perform in the `receive` method.
    """

    @property
    def name(self) -> str:
        """The name of the agent."""
        ...

    def generate_reply(
        self,
        messages: Dict[str, str],
        sender: Optional[str] = None,
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        """Generate a reply based on the received messages.

        Args:
        ----
            messages (list[dict]): a list of messages received from other agents.
                The messages are dictionaries that are JSON-serializable and
                follows the OpenAI's ChatCompletion schema.
            sender: sender of an Agent instance.

        Returns:
        -------
            str or dict or None: the generated reply. If None, no reply is generated.

        """
        ...

    def resolve_task(self, task: str) -> Optional[str]:
        """Resolve a task to a function name.

        Args:
        ----
            task (str): the task to resolve.

        Returns:
        -------
            str or None: the function name corresponding to the task.

        """
        ...

    @property
    def system_message(self) -> str:
        """The system message of this agent."""
        ...

    @property
    def chat_history(self) -> List[Dict[str, str]]:
        """Returns the Chat history"""
        ...

    def reset_chat_history(self) -> None:
        """Reset the Chat history"""
        ...
