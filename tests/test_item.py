from mincrawler.item import Item


def test_item():
    item = Item("123", {})

    item["foo"] = {"x": 123}
    item["bar"] = {"y": 456}
    item["bar"]["y"] = 789

    assert item.id == "123"
    assert len(item) == 2
    assert item["foo"]["x"] == 123
    assert item["bar"]["y"] == 789
