"""Template for adding a custom attack node."""

from collections.abc import Mapping
from typing import Any

from formaltrust_platform.state import AttackResult, FormalTrustState


def custom_attack_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    prompt = f"{state.case.input}\n{config.get('suffix', '[custom attack suffix]')}"
    return {
        "prompt": prompt,
        "attack": AttackResult(attack_type="custom", prompt=prompt),
    }

