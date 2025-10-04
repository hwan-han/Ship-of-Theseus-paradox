from dataclasses import dataclass, field
import random
from typing import List, Set, Dict

@dataclass
class Ship:
    n_parts: int = 100
    core_part_ids: Set[int] = field(default_factory=set)
    seed: int = 42

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        # True = 원래 부품이 남아 있음, False = 교체됨
        self.original_flags: List[bool] = [True] * self.n_parts
        # 간단한 구조 표현(자리 유지 시 형태 보존으로 간주)
        self.structure: List[int] = list(range(self.n_parts))
        # 이력
        self.history: Dict[str, int] = {"discontinuities": 0, "replaced": 0}

    def replace_parts(self, k: int = 1, strategy: str = "random"):
        """k개의 부품을 교체. 간단 버전: 무작위 인덱스 선택"""
        replace_candidates = [i for i, f in enumerate(self.original_flags) if f]
        if k <= 0 or not replace_candidates:
            return []
        k = min(k, len(replace_candidates))
        if strategy == "random":
            picks = self.rng.sample(replace_candidates, k)
        else:
            # 확장 여지: 'cluster' 등
            picks = replace_candidates[:k]

        for idx in picks:
            self.original_flags[idx] = False
        self.history["replaced"] += len(picks)
        return picks

    def wholesale_replace(self):
        """일괄 교체(불연속 이벤트)"""
        replaced = 0
        for i, f in enumerate(self.original_flags):
            if f:
                self.original_flags[i] = False
                replaced += 1
        self.history["replaced"] += replaced
        self.history["discontinuities"] += 1
        return replaced
