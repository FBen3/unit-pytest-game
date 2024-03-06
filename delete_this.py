import pytest


def some_other_func():
    print("Hello")

def return_my_name(name="Ben"):
    some_other_func()
    return name

def test_return_my_name(monkeypatch, capsys):
    monkeypatch.setattr(
        'delete_this.some_other_func',
        lambda: None
    )
    val = return_my_name()

    out, err = capsys.readouterr()

    assert out == ""
    assert val == "Ben"



