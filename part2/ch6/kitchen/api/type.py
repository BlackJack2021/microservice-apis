from typing import TypedDict, Literal, List
from datetime import datetime

# order の定義
class EachOrder(TypedDict):
    product: str
    quantity: int # 本当は1以上の整数だが、型ヒントではそこまで制約をかけられない
    size: Literal['small', 'medium', 'big']

# schedule の型を定義
class Schedule(TypedDict):
    id: str
    scheduled: datetime
    status: Literal["pending", "progress", "cancelled", "finished"]
    order: List[EachOrder]
    
class ScheduleOrder(TypedDict):
    order: List[EachOrder]