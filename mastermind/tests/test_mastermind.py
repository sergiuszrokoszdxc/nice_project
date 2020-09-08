from unittest.mock import AsyncMock, Mock

import pytest

from mastermind.mastermind import Mastermind
import mastermind.mastermind
import mastermind.game

def test_mastermind_init():
    m = Mastermind(n_colours=3, n_positions=4)
    assert len(m.sequence) == 4 # pylint: disable=no-member
    # TODO: assert that min == 0, max == n_positions
    m = Mastermind(n_colours=3, n_positions=4, sequence=[0, 1, 2, 2], foo="bar", history=[])
    assert m.sequence == [0, 1, 2, 2] # pylint: disable=no-member
    assert m.foo == "bar" # pylint: disable=no-member

def test_mastermind_n_tries():
    m = Mastermind(n_colours=3, n_positions=4)
    m.history = [0, 0, 0]
    assert m.n_tries == 3

def test_mastermind_has_ended():
    m = Mastermind(n_colours=3, n_positions=4, max_tries=3)
    result = {"hint": (0, 0)}
    m.history = [result, result]
    assert m.has_ended is False
    m.history.append(result)
    assert m.has_ended is True
    m = Mastermind(n_colours=3, n_positions=4, max_tries=3)
    result = {"hint": (4, 0)}
    m.history = [result]
    assert m.has_ended is True

def test_mastermind_if_win():
    m = Mastermind(n_colours=3, n_positions=4, max_tries=3)
    hint = (3, 0)
    assert m._if_win(hint) is False
    hint = (4, 0)
    assert m._if_win(hint) is True

@pytest.mark.asyncio
async def test_mastermind_play(monkeypatch):
    # schedule_deletion_mock = AsyncMock()
    # monkeypatch.setattr(mastermind.game, "schedule_deletion", schedule_deletion_mock)
    update_game_mock = AsyncMock()
    monkeypatch.setattr(mastermind.mastermind, "update_game", update_game_mock)
    m = Mastermind(n_colours=3, n_positions=4, max_tries=3, sequence=[0, 1, 2, 2], history=[])
    assert await m.play([0, 0, 0, 0]) is False
    assert update_game_mock.called_with(m.serialize())
    assert m.history == [{"guess": [0, 0, 0, 0], "hint": (1, 0)}]
    assert await m.play([0, 0, 1, 0]) is False
    assert update_game_mock.called_with(m.serialize())
    assert m.history[-1] == {"guess": [0, 0, 1, 0], "hint": (1, 1)}
    assert await m.play([0, 1, 2, 2]) is True
    assert update_game_mock.called_with(m.serialize())
    assert m.history[-1] == {"guess": [0, 1, 2, 2], "hint": (4, 0)}
    assert m.n_tries == 3
    # TODO: assert schedule_deletion_mock.called_with()
    assert await m.play([0, 1, 2, 2]) is False
    assert update_game_mock.called_with(m.serialize())
    assert m.history[-1] == {"guess": [0, 1, 2, 2], "hint": (4, 0)}
    assert m.n_tries == 3

def test_mastermind_guess():
    m = Mastermind(n_colours=5, n_positions=4, sequence=[0, 1, 2, 3], history=[])
    assert m._guess([4, 4, 4, 4]) == (0, 0)
    assert m._guess([3, 2, 1, 0]) == (0, 4)
    assert m._guess([0, 1, 2, 3]) == (4, 0)

@pytest.mark.asyncio
async def test_mastermind_save_guess_result(monkeypatch):
    m = Mastermind(n_colours=5, n_positions=2, sequence=[0, 1, 2, 3], history=[])
    update_game_mock = AsyncMock()
    monkeypatch.setattr(mastermind.mastermind, "update_game", update_game_mock)
    await m._save_guess_result({"foo": "bar"})
    assert update_game_mock.called_with(m.serialize())
    assert m.history == [{"foo": "bar"}]