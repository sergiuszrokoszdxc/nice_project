from unittest.mock import AsyncMock, Mock

import pytest

import mastermind.game
from mastermind.game import Game
from mastermind.mongo_backend import (get_game_by_id, get_game_cursor, schedule_deletion)

def test_game_init():
        g = Game(foo="foo", bar="bar")
        assert hasattr(g, "foo")
        assert g.foo == "foo" # pylint: disable=no-member
        assert hasattr(g, "bar")
        assert g.bar == "bar" # pylint: disable=no-member
        assert g._set_attributes == ["foo", "bar"]

def test_game_repr():
        g = Game(foo="foo", bar="bar")
        assert repr(g) == "Game(foo=foo, bar=bar)"

@pytest.fixture
def model_mock():
    model_mock = Mock()
    model_mock.__name__ = "MockModel"
    model_mock.__fields__ = ["foo", "bar"]
    return model_mock

def test_game_serialize(model_mock):
    g = Game(foo="foo", bar="bar", foobar="foobar")
    ser = g.serialize(model_mock)
    assert ser == {"foo": "foo", "bar": "bar"}
    g.db_model = model_mock
    model_mock.__fields__ = ["foo"]
    ser = g.serialize()
    assert ser == {"foo": "foo"}
    model_mock.__fields__ = ["foo", "id_"]
    ser = g.serialize()
    assert ser == {"foo": "foo"}
    g = Game(foo="foo", bar="bar", foobar="foobar", id_="id_")
    g.db_model = model_mock
    ser = g.serialize()
    assert ser == {"foo": "foo", "id_": "id_"}
    model_mock.__fields__ = ["foo", "id_", "foobar2"]
    with pytest.raises(AttributeError):
        g.serialize()

@pytest.mark.asyncio
async def test_game_new_game(monkeypatch, model_mock):
    coroutine_mock = AsyncMock(return_value={"foobar": "foobar"})
    monkeypatch.setattr(mastermind.game, "save_game", coroutine_mock)
    Game.db_model = model_mock
    return_value = await Game.new_game({"foo": "foo", "bar": "bar", "foobar": "foobar"})
    coroutine_mock.assert_awaited_with({"foo": "foo", "bar": "bar"})
    assert type(return_value) == Game
    assert return_value.foobar == "foobar"
    assert return_value._set_attributes == ["foobar"]

@pytest.mark.asyncio
async def test_game_schedule_deletion(monkeypatch, model_mock):
    coroutine_mock = AsyncMock(return_value={"foobar": "foobar"})
    monkeypatch.setattr(mastermind.game, "schedule_deletion", coroutine_mock)
    Game.db_model = model_mock
    Game.schedule_deletion("id123", "tomorrow")
    coroutine_mock.assert_called_with("id123", "tomorrow")

@pytest.mark.asyncio
async def test_game_get_game_by_id(monkeypatch, model_mock):
    coroutine_mock = AsyncMock(return_value={"foobar": "foobar"})
    monkeypatch.setattr(mastermind.game, "get_game_by_id", coroutine_mock)
    Game.db_model = model_mock
    return_value = await Game.get_game_by_id("id123")
    coroutine_mock.assert_awaited_with("id123")
    assert type(return_value) == Game
    assert return_value.foobar == "foobar"
    assert return_value._set_attributes == ["foobar"]

@pytest.mark.asyncio
async def test_game_get_games(monkeypatch, model_mock):
    coroutine_mock = AsyncMock(side_effect=[{"foobar": "bar"}, {"foobar": "foo"}])
    coroutine_mock.__aiter__ = lambda x: x
    coroutine_mock.__anext__ = lambda x: x()
    get_game_cursor_mock = Mock(return_value=coroutine_mock)
    monkeypatch.setattr(mastermind.game, "get_game_cursor", get_game_cursor_mock)
    Game.db_model = model_mock
    return_value = await Game.get_games({"query": "query"})
    get_game_cursor_mock.assert_called_with({"query": "query"})
    game1, game2 = return_value
    assert type(game1) == Game
    assert game1.foobar == "bar"
    assert game1._set_attributes == ["foobar"]
    assert type(game2) == Game
    assert game2.foobar == "foo"
    assert game2._set_attributes == ["foobar"]

@pytest.mark.asyncio
async def test_game_get_all(monkeypatch, model_mock):
    coroutine_mock = AsyncMock(side_effect=[{"foobar": "bar"}, {"foobar": "foo"}])
    coroutine_mock.__aiter__ = lambda x: x
    coroutine_mock.__anext__ = lambda x: x()
    get_game_cursor_mock = Mock(return_value=coroutine_mock)
    monkeypatch.setattr(mastermind.game, "get_game_cursor", get_game_cursor_mock)
    Game.db_model = model_mock
    return_value = await Game.get_all()
    get_game_cursor_mock.assert_called_with({})
    game1, game2 = return_value
    assert type(game1) == Game
    assert game1.foobar == "bar"
    assert game1._set_attributes == ["foobar"]
    assert type(game2) == Game
    assert game2.foobar == "foo"
    assert game2._set_attributes == ["foobar"]


# TODO: test mixins