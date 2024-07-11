#!/usr/bin/env python
# -*- coding: utf-8 -*-
# /backend/utils/yaml_control.py

import os
import yaml
from backend.utils.log_control import logger
from backend.core.config import ensure_path_sep


def get_yaml_data(filepath) -> dict:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            _data = yaml.safe_load(f)  # yaml.load是不安全的
            return _data
    else:
        logger.error(f"{filepath}文件路径不存在")
        raise FileNotFoundError(f"{filepath}文件路径不存在")


def read_config(key: str) -> str:
    try:
        config = ensure_path_sep('\\config\\setting.yaml')
        data = get_yaml_data(config)
        return data[key]
    except KeyError:
        logger.error(f"config不包含 {key} 键名")
        raise KeyError(f"config不包含 {key} 键名")
