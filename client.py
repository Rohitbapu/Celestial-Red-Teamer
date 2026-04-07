# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Celestial Red Team2 Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from .models import CelestialRedTeam2Action, CelestialRedTeam2Observation


class CelestialRedTeam2Env(
    EnvClient[CelestialRedTeam2Action, CelestialRedTeam2Observation, State]
):
    """
    Client for the Celestial Red Team2 Environment.

    This client maintains a persistent WebSocket connection to the environment server,
    enabling efficient multi-step interactions with lower latency.
    Each client instance has its own dedicated environment session on the server.

    Example:
        >>> # Connect to a running server
        >>> with CelestialRedTeam2Env(base_url="http://localhost:8000") as client:
        ...     result = client.reset()
        ...     print(result.observation.echoed_message)
        ...
        ...     result = client.step(CelestialRedTeam2Action(message="Hello!"))
        ...     print(result.observation.echoed_message)

    Example with Docker:
        >>> # Automatically start container and connect
        >>> client = CelestialRedTeam2Env.from_docker_image("celestial_red_team2-env:latest")
        >>> try:
        ...     result = client.reset()
        ...     result = client.step(CelestialRedTeam2Action(message="Test"))
        ... finally:
        ...     client.close()
    """

    def _step_payload(self, action: CelestialRedTeam2Action) -> Dict:
        """
        Convert CelestialRedTeam2Action to JSON payload for step message.

        Args:
            action: CelestialRedTeam2Action instance

        Returns:
            Dictionary representation suitable for JSON encoding
        """
        return {
            "message": action.message,
        }

    def _parse_result(self, payload: Dict) -> StepResult[CelestialRedTeam2Observation]:
        """
        Parse server response into StepResult[CelestialRedTeam2Observation].

        Args:
            payload: JSON response data from server

        Returns:
            StepResult with CelestialRedTeam2Observation
        """
        obs_data = payload.get("observation", {})
        observation = CelestialRedTeam2Observation(
            echoed_message=obs_data.get("echoed_message", ""),
            message_length=obs_data.get("message_length", 0),
            done=payload.get("done", False),
            reward=payload.get("reward"),
            metadata=obs_data.get("metadata", {}),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> State:
        """
        Parse server response into State object.

        Args:
            payload: JSON response from state request

        Returns:
            State object with episode_id and step_count
        """
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )
