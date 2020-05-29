import json
import logging
import os
import typing as tp

try:
    from _jsonnet import evaluate_file
except ImportError:

    def evaluate_file(filename: str, **_kwargs) -> str:
        logger.warning(
            "error loading _jsonnet (this is expected on Windows), "
            "treating %s as plain json", filename)
        with open(filename, "r") as evaluation_file:
            return evaluation_file.read()


logger = logging.getLogger(__name__)


def _is_encodable(value: str) -> bool:
    return (value == "") or (value.encode("utf-8", "ignore") != b"")


def _environment_variables() -> tp.Dict[str, str]:
    return {
        key: value
        for key, value in os.environ.items() if _is_encodable(value)
    }


def load_jsonnet(path: str) -> tp.Dict[str, tp.Any]:
    ext_vars = _environment_variables()
    jsondict = json.loads(evaluate_file(str(path), ext_vars=ext_vars))
    return tp.cast(tp.Dict[str, tp.Any], jsondict)
