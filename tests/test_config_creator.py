"""Test config_creator.py"""
# ruff: noqa: D400

import json
import os

import pytest

from build.config.config_creator import (
    check_bool_value,
    check_float_value,
    check_int_value,
    check_value,
    main,
    set_game_setting,
)


def test_check_value_valid(monkeypatch):
    """
    Test check value method with valid values

    :param monkeypatch:
    :return:
    """
    monkeypatch.setenv("FOO", "BAR")
    check_value("FOO", ["BAR", "BAR2"], "BAR or BAR2")


def test_check_value_invalid(monkeypatch):
    """
    Test check value method with invalid values

    :param monkeypatch:
    :return:
    """
    monkeypatch.setenv("FOO", "BAR")
    with pytest.raises(ValueError, match="Wrong Value! FOO needs Bar or Bar2"):
        check_value("FOO", ["Bar", "Bar2"], "Bar or Bar2")


def test_check_bool_value_true(monkeypatch):
    """
    Test check bool method with true boolean

    :param monkeypatch:
    :return:
    """
    monkeypatch.setenv("FOO", "true")
    assert check_bool_value("FOO") is True


def test_check_bool_value_false(monkeypatch):
    """
    Test check bool method with false boolean

    :param monkeypatch:
    :return:
    """
    monkeypatch.setenv("FOO", "false")
    assert check_bool_value("FOO") is False


def test_check_bool_value_default(monkeypatch):
    """
    Test check bool method with default value

    :param monkeypatch:
    :return:
    """
    if "FOO" in os.environ:
        monkeypatch.delenv("FOO", raising=False)
    assert check_bool_value("FOO") is False


def test_check_int_value_valid(monkeypatch):
    """
    Test check int method with valid value

    :param monkeypatch:
    :return:
    """
    monkeypatch.setenv("FOO", "42")
    assert check_int_value("FOO", 0) == 42


def test_check_int_value_default(monkeypatch):
    """
    Test check int method with default value

    :param monkeypatch:
    :return:
    """
    if "FOO" in os.environ:
        monkeypatch.delenv("FOO", raising=False)
    assert check_int_value("FOO", 0) == 0


def test_check_float_value_valid(monkeypatch):
    """
    Test check float method with valid value

    :param monkeypatch:
    :return:
    """
    monkeypatch.setenv("FOO", "4.2")
    assert check_float_value("FOO", 2.4) == 4.2


def test_check_float_value_default(monkeypatch):
    """
    Test check float method with default value

    :param monkeypatch:
    :return:
    """
    if "FOO" in os.environ:
        monkeypatch.delenv("FOO", raising=False)
    assert check_float_value("FOO", 0.0) == 0.0


test_data = [
    ("true", True, bool),
    ("false", False, bool),
    ("42", 42, int),
    ("4.2", 4.2, float),
    ("BAR", "BAR", lambda x: check_value("FOO", ["BAR"], "BAR")),
    ("BOO", ValueError, lambda x: check_value("FOO", ["BAR"], "BAR")),
    (None, True, bool),
]


@pytest.mark.parametrize("val, expected, types", test_data)
def test_game_setting(val, expected, types, monkeypatch):
    """
    Test set game settings method

    :param val:
    :param expected:
    :param types:
    :param monkeypatch:
    :return:
    """
    config = {}
    if val is not None:
        monkeypatch.setenv("FOO", val)
        if expected is not ValueError:
            set_game_setting(
                config=config, env_var="FOO", setting_key="test", value_check=types
            )
            assert config["test"] == expected
        else:
            with pytest.raises(ValueError, match="Wrong Value! FOO needs BAR"):
                set_game_setting(
                    config=config, env_var="FOO", setting_key="test", value_check=types
                )
    else:
        monkeypatch.delenv("FOO", raising=False)
        set_game_setting(
            config=config, env_var="FOO", setting_key="test", value_check=types
        )
        assert "test" not in config


def test_main_without_extra_settings_valid(monkeypatch, capsys):
    """
    Test main method with valid values

    :param monkeypatch:
    :param capsys:
    :return:
    """
    monkeypatch.setenv("IPADDRESS", "127.0.0.1")
    monkeypatch.setenv("GAMEPORT", "8766")
    monkeypatch.setenv("QUERYPORT", "27016")
    monkeypatch.setenv("BLOBSYNCPORT", "9700")
    monkeypatch.setenv("SERVERNAME", "Test Server")
    monkeypatch.setenv("MAXPLAYERS", "10")
    monkeypatch.setenv("PASSWORD", "LETMEIN")
    monkeypatch.setenv("LANONLY", "true")
    monkeypatch.setenv("SAVESLOT", "2")
    monkeypatch.setenv("SAVEMODE", "New")
    monkeypatch.setenv("GAMEMODE", "Hard")
    monkeypatch.setenv("SAVEINTERVAL", "300")
    monkeypatch.setenv("IDLEDAYCYCLESPEED", "1.0")
    monkeypatch.setenv("IDLETARGETFRAMERATE", "10")
    monkeypatch.setenv("ACTIVETARGETFRAMERATE", "60")
    monkeypatch.setenv("LOGFILESENABLED", "true")
    monkeypatch.setenv("TIMESTAMPLOGFILENAMES", "true")
    monkeypatch.setenv("TIMESTAMPLOGENTRIES", "true")
    monkeypatch.setenv("SKIPNETWORKACCESSIBILITYTEST", "false")

    main()

    captured = capsys.readouterr()
    config = json.loads(captured.out)
    assert config["IpAddress"] == "127.0.0.1"
    assert config["GamePort"] == 8766
    assert config["QueryPort"] == 27016
    assert config["BlobSyncPort"] == 9700
    assert config["ServerName"] == "Test Server"
    assert config["MaxPlayers"] == 10
    assert config["Password"] == "LETMEIN"
    assert config["LanOnly"] is True
    assert config["SaveSlot"] == 2
    assert config["SaveMode"] == "New"
    assert config["GameMode"] == "Hard"
    assert config["SaveInterval"] == 300
    assert config["IdleDayCycleSpeed"] == 1.0
    assert config["IdleTargetFramerate"] == 10
    assert config["ActiveTargetFramerate"] == 60
    assert config["LogFilesEnabled"] is True
    assert config["TimestampLogFilenames"] is True
    assert config["TimestampLogEntries"] is True
    assert config["SkipNetworkAccessibilityTest"] is False
    assert "Structure.Damage" not in config["GameSettings"]
    assert "Gameplay.TreeRegrowth" not in config["GameSettings"]


def test_main_without_extra_settings_invalid(monkeypatch):
    """
    Test main method with invalid values

    :param monkeypatch:
    :return:
    """
    monkeypatch.setenv("GAMEMODE", "FOOBAR")
    with pytest.raises(SystemExit) as info:
        main()
        assert info.value.code == 1


def test_main_with_extra_settings_valid(monkeypatch, capsys):
    """
    Test main method with extra settings and valid values

    :param monkeypatch:
    :param capsys:
    :return:
    """
    monkeypatch.setenv("CREATIVEMODE", "true")
    monkeypatch.setenv("TREEREGROWTH", "true")

    main()

    captured = capsys.readouterr()
    config = json.loads(captured.out)
    assert config["IpAddress"] == "0.0.0.0"
    assert config["GamePort"] == 8766
    assert config["QueryPort"] == 27016
    assert config["BlobSyncPort"] == 9700
    assert config["ServerName"] == "My Sotf Server"
    assert config["MaxPlayers"] == 8
    assert config["Password"] == ""
    assert config["LanOnly"] is False
    assert config["SaveSlot"] == 1
    assert config["SaveMode"] == "Continue"
    assert config["GameMode"] == "Normal"
    assert config["SaveInterval"] == 600
    assert config["IdleDayCycleSpeed"] == 0.0
    assert config["IdleTargetFramerate"] == 5
    assert config["ActiveTargetFramerate"] == 60
    assert config["LogFilesEnabled"] is True
    assert config["TimestampLogFilenames"] is True
    assert config["TimestampLogEntries"] is True
    assert config["SkipNetworkAccessibilityTest"] is False
    assert config["GameSettings"]["Gameplay.TreeRegrowth"] is True
    assert config["CustomGameModeSettings"]["GameSetting.Survival.CreativeMode"] is True
    assert "Structure.Damage" not in config["GameSettings"]
    assert (
        "GameSetting.Environment.PrecipitationFrequency"
        not in config["CustomGameModeSettings"]
    )
