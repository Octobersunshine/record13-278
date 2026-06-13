import random
from typing import List, Optional, Union


class RandomService:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def randint(self, low: int, high: int) -> int:
        if low > high:
            low, high = high, low
        return random.randint(low, high)

    def uniform(self, low: float, high: float) -> float:
        if low > high:
            low, high = high, low
        return random.uniform(low, high)

    def randrange(self, start: int, stop: Optional[int] = None, step: int = 1) -> int:
        if stop is None:
            return random.randrange(start)
        return random.randrange(start, stop, step)

    def choice(self, seq: List[Union[int, float, str]]) -> Union[int, float, str]:
        if not seq:
            raise ValueError("Cannot choose from an empty sequence")
        return random.choice(seq)

    def sample(self, population: List[Union[int, float, str]], k: int) -> List[Union[int, float, str]]:
        if k > len(population):
            raise ValueError("Sample larger than population or is negative")
        return random.sample(population, k)

    def shuffle(self, seq: List[Union[int, float, str]]) -> List[Union[int, float, str]]:
        shuffled = seq.copy()
        random.shuffle(shuffled)
        return shuffled

    def randints(self, low: int, high: int, count: int) -> List[int]:
        if count < 0:
            raise ValueError("Count cannot be negative")
        return [self.randint(low, high) for _ in range(count)]

    def uniforms(self, low: float, high: float, count: int) -> List[float]:
        if count < 0:
            raise ValueError("Count cannot be negative")
        return [self.uniform(low, high) for _ in range(count)]
