
from typing import Sequence

def form_score(structure_unchanged: bool = True) -> float:
    """형태가 유지되면 1.0, 아니면 0.0 (단순 버전)"""
    return 1.0 if structure_unchanged else 0.0

def material_score(original_flags: Sequence[bool], core_ids=None, core_weight: float = 3.0) -> float:
    """원부품 보존율. 핵심부품은 가중치 부여(옵션)."""
    n = len(original_flags)
    if n == 0:
        return 0.0
    core_ids = set(core_ids or [])
    total_w = 0.0
    kept_w = 0.0
    for i, flag in enumerate(original_flags):
        w = core_weight if i in core_ids else 1.0
        total_w += w
        if flag:
            kept_w += w
    return kept_w / total_w

def continuity_score(discontinuities: int) -> float:
    """불연속 이벤트(일괄 교체)가 많을수록 감점. 간단히 1/(1+d)."""
    return 1.0 / (1.0 + discontinuities)

def identity_score(form: float, material: float, continuity: float,
                   alpha: float = 0.4, beta: float = 0.3, gamma: float = 0.3) -> float:
    return alpha*form + beta*material + gamma*continuity
