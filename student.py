from dataclasses import dataclass
from typing import List


@dataclass
class Student:
    id: int
    hw_id: int
    first_name: str
    last_name: str
    email: str
    grades: List[int] = None

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}\n{"="*(len(self.first_name + self.last_name)+1)}\nid: {self.id}\nhw_id: {self.hw_id}\nemail: {self.email}'

    def score(self):
        N = len(self.grades)
        return (sum(self.grades) - min(self.grades))/((N-1)*10)
