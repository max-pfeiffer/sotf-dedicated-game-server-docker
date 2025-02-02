"""Config creator for Sons of the Forest"""
# ruff: noqa: D400

import json
import os
from typing import Any, Callable


def check_value(key: str, allowed_values: list, error_message: str) -> None:
    """
    Check if the value is valid

    :param key:
    :param allowed_values:
    :param error_message:
    :return:
    """
    value = os.getenv(key)
    if value not in allowed_values:
        raise ValueError(f"Wrong Value! {key} needs {error_message}")


def check_bool_value(key: str, default: bool = False) -> bool:
    """
    Check bool value

    :param key:
    :param default:
    :return:
    """
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ["true"] if value else False


def check_int_value(key: str, default: int = 0) -> int:
    """
    Check int value

    :param key:
    :param default:
    :return:
    """
    value = os.getenv(key)
    if value is None:
        return default
    return int(value) if value else default


def check_float_value(key: str, default: float = 1.0) -> float:
    """
    Check float value

    :param key:
    :param default:
    :return:
    """
    value = os.getenv(key)
    if value is None:
        return default
    return float(value) if value else default


def set_game_setting(
    config: dict[str, Any],
    env_var: str,
    setting_key: str,
    value_check: [type | Callable],
) -> None:
    """
    Process game settings and custom game settings

    :param config:
    :param env_var:
    :param setting_key:
    :param value_check:
    :return:
    """
    if env_var in os.environ:
        value = os.getenv(env_var)
        if value_check is bool:
            value = check_bool_value(key=env_var)
        elif value_check is int:
            value = check_int_value(key=env_var)
        elif value_check is float:
            value = check_float_value(key=env_var)
        elif callable(value_check):
            value_check(value)
        config[setting_key] = value


def main() -> None:
    """
    Create config

    :return:
    """
    try:
        config: dict[str, Any] = {}

        # Base game configuration
        config["IpAddress"] = os.getenv("IPADDRESS", "0.0.0.0")
        config["GamePort"] = check_int_value("GAMEPORT", 8766)
        config["QueryPort"] = check_int_value("QUERYPORT", 27016)
        config["BlobSyncPort"] = check_int_value("BLOBSYNCPORT", 9700)
        config["ServerName"] = os.getenv("SERVERNAME", "My Sotf Server")
        config["MaxPlayers"] = check_int_value("MAXPLAYERS", 8)
        config["Password"] = os.getenv("PASSWORD", "")
        config["LanOnly"] = check_bool_value("LANONLY")
        config["SaveSlot"] = check_int_value("SAVESLOT", 1)
        check_value("SAVEMODE", [None, "New", "Continue"], "New or Continue")
        config["SaveMode"] = os.getenv("SAVEMODE", "Continue")
        check_value(
            "GAMEMODE",
            [None, "Normal", "Hard", "Hardsurvival", "Peaceful", "Creative", "Custom"],
            "Normal, Hard, Hardsurvival, Peaceful, Creative or Custom",
        )
        config["GameMode"] = os.getenv("GAMEMODE", "Normal")
        config["SaveInterval"] = check_int_value("SAVEINTERVAL", 600)
        config["IdleDayCycleSpeed"] = check_float_value("IDLEDAYCYCLESPEED", 0.0)
        config["IdleTargetFramerate"] = check_int_value("IDLETARGETFRAMERATE", 5)
        config["ActiveTargetFramerate"] = check_int_value("ACTIVETARGETFRAMERATE", 60)
        config["LogFilesEnabled"] = check_bool_value("LOGFILESENABLED", default=True)
        config["TimestampLogFilenames"] = check_bool_value(
            "TIMESTAMPLOGFILENAMES", default=True
        )
        config["TimestampLogEntries"] = check_bool_value(
            "TIMESTAMPLOGENTRIES", default=True
        )
        config["SkipNetworkAccessibilityTest"] = check_bool_value(
            "SKIPNETWORKACCESSIBILITYTEST"
        )

        # Game settings
        config["GameSettings"] = {}
        set_game_setting(
            config["GameSettings"], "TREEREGROWTH", "Gameplay.TreeRegrowth", bool
        )
        set_game_setting(
            config["GameSettings"], "STRUCTUREDAMAGE", "Structure.Damage", bool
        )

        # Custom game settings
        config["CustomGameModeSettings"] = {}
        settings_mapping = {
            "CHEATS": ("GameSetting.Multiplayer.Cheats", bool),
            "ENEMYSPAWN": ("GameSetting.Vail.EnemySpawn", str),
            "ENEMYHEALTH": (
                "GameSetting.Vail.EnemyHealth",
                lambda x: check_value(
                    "ENEMYHEALTH", ["Low", "Normal", "High"], "Low, Normal or High"
                ),
            ),
            "ENEMYDAMAGE": (
                "GameSetting.Vail.EnemyDamage",
                lambda x: check_value(
                    "ENEMYDAMAGE", ["Low", "Normal", "High"], "Low, Normal or High"
                ),
            ),
            "ENEMYARMOUR": (
                "GameSetting.Vail.EnemyArmour",
                lambda x: check_value(
                    "ENEMYARMOUR", ["Low", "Normal", "High"], "Low, Normal or High"
                ),
            ),
            "ENEMYAGGRESSION": (
                "GameSetting.Vail.EnemyAggression",
                lambda x: check_value(
                    "ENEMYAGGRESSION", ["Low", "Normal", "High"], "Low, Normal or High"
                ),
            ),
            "ANIMALSPAWNRATE": (
                "GameSetting.Vail.AnimalSpawnRate",
                lambda x: check_value(
                    "ANIMALSPAWNRATE", ["Low", "Normal", "High"], "Low, Normal or High"
                ),
            ),
            "ENEMYSEARCHPARTIES": (
                "GameSetting.Vail.EnemySearchParties",
                lambda x: check_value(
                    "ENEMYSEARCHPARTIES",
                    ["Low", "Normal", "High"],
                    "Low, Normal or High",
                ),
            ),
            "STARTINGSEASON": (
                "GameSetting.Environment.StartingSeason",
                lambda x: check_value(
                    "STARTINGSEASON",
                    ["Spring", "Summer", "Autumn", "Winter"],
                    "Spring, Summer, Autumn or Winter",
                ),
            ),
            "SEASONLENGTH": (
                "GameSetting.Environment.SeasonLength",
                lambda x: check_value(
                    "SEASONLENGTH",
                    ["Short", "Default", "Long", "Realistic"],
                    "Short, Default, Long or Realistic",
                ),
            ),
            "DAYLENGTH": (
                "GameSetting.Environment.DayLength",
                lambda x: check_value(
                    "DAYLENGTH",
                    ["Short", "Default", "Long", "Realistic"],
                    "Short, Default, Long or Realistic",
                ),
            ),
            "PRECIPITATIONFREQUENCY": (
                "GameSetting.Environment.PrecipitationFrequency",
                lambda x: check_value(
                    "PRECIPITATIONFREQUENCY",
                    ["Low", "Default", "High"],
                    "Low, Default or High",
                ),
            ),
            "CONSUMABLEEFFECTS": (
                "GameSetting.Survival.ConsumableEffects",
                lambda x: check_value(
                    "CONSUMABLEEFFECTS", ["Normal", "Hard"], "Normal or Hard"
                ),
            ),
            "PLAYERSTATSDAMAGE": (
                "GameSetting.Survival.PlayerStatsDamage",
                lambda x: check_value(
                    "PLAYERSTATSDAMAGE",
                    ["Off", "Normal", "Hard"],
                    "Off, Normal or Hard",
                ),
            ),
            "COLDPENALTIES": (
                "GameSetting.Survival.ColdPenalties",
                lambda x: check_value(
                    "COLDPENALTIES", ["Off", "Normal", "Hard"], "Off, Normal or Hard"
                ),
            ),
            "STATREGENERATIONPENALTY": (
                "GameSetting.Survival.StatRegenerationPenalty",
                lambda x: check_value(
                    "STATREGENERATIONPENALTY",
                    ["Off", "Normal", "Hard"],
                    "Off, Normal or Hard",
                ),
            ),
            "REDUCEDFOODINCONTAINERS": (
                "GameSetting.Survival.ReducedFoodInContainers",
                bool,
            ),
            "SINGLEUSECONTAINERS": ("GameSetting.Survival.SingleUseContainers", bool),
            "BUILDINGRESISTANCE": (
                "GameSetting.Survival.BuildingResistance",
                lambda x: check_value(
                    "BUILDINGRESISTANCE",
                    ["Low", "Normal", "High"],
                    "Low, Normal or High",
                ),
            ),
            "CREATIVEMODE": ("GameSetting.Survival.CreativeMode", bool),
            "PLAYERSIMMORTALMODE": ("GameSetting.Survival.PlayersImmortalMode", bool),
            "FORCEPLACEFULLLOAD": ("GameSetting.FreeForm.ForcePlaceFullLoad", bool),
            "NOCUTTINGSSPAWN": ("GameSetting.Construction.NoCuttingsSpawn", bool),
            "ONEHITTOCUTTREE": ("GameSetting.Survival.OneHitToCutTrees", bool),
        }

        for env_var, (setting_key, value_check) in settings_mapping.items():
            set_game_setting(
                config=config["CustomGameModeSettings"],
                env_var=env_var,
                setting_key=setting_key,
                value_check=value_check,
            )

        print(json.dumps(config, indent=4))

    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
