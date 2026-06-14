"""Template for a custom ATTACK node.

Contract (see ``formaltrust_platform.interfaces.AttackNode``):
  Reads:  ``state.case.input``.
  Writes: MUST return ``{"prompt": str}``; SHOULD include
          ``{"attack": AttackResult}``. May add ``retrieval_context``.

Register with: ``registry.register(custom_attack_node)``.
"""

from collections.abc import Mapping
from typing import Any

from formaltrust_platform.interfaces import ConfigField, node
from formaltrust_platform.state import AttackResult, FormalTrustState


@node(
    "attack.custom",
    category="attack",
    summary="Example custom attack node that appends a suffix to the input.",
    config_fields=[
        ConfigField("suffix", default="[custom attack suffix]", description="Text appended to the case input."),
    ],
)
def custom_attack_node(state: FormalTrustState, config: Mapping[str, Any]) -> dict[str, Any]:
    prompt = f"{state.case.input}\n{config.get('suffix', '[custom attack suffix]')}"
    return {
        "prompt": prompt,
        "attack": AttackResult(attack_type="custom", prompt=prompt),
    }
