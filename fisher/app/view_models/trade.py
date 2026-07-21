from app.schemas.trade import TradeItem, TradeListData


class TradeInfo:
    def __init__(self, items):
        self.total = 0
        self.trades: list[TradeItem] = []
        self.__map_to_list(items)

    def __map_to_list(self, items):
        self.total = len(items)
        self.trades = [self.__map_to_item(single) for single in items]

    def __map_to_item(self, single) -> TradeItem:
        # return TradeItem(
        #     id=single.id,
        #     time=single.create_time,
        #     user_id=single.user_id,
        #     email=single.user.email,
        # )
        # 大部分一致，少数要改名/拼装 → 混合
        data = single.model_dump() # 将对象转换为字典
        data["time"] = data.pop("create_time")
        data["email"] = single.user.email if single.user else None
        return TradeItem.model_validate(data)

    def to_schema(self, user_type: int | None = None) -> TradeListData:
        return TradeListData(
            total=self.total,
            trades=self.trades,
            user_type=user_type,
        )
