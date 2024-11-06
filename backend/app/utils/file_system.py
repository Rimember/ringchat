"""
File System Utilities Module

This module provides file system-related utility functions 
such as file and directory path management, creation and deletion  
"""

import os


def find_project_root():
    """프로젝트 루트 디렉토리를 찾기 위한 함수."""
    current_path = os.path.abspath(os.path.dirname(__file__))
    while current_path:
        # 여기서 'pyproject.toml', 'setup.py', 또는 '.git' 등 프로젝트의 root임을 식별할 수 있는 파일이나 디렉터리를 확인합니다.
        if 'pyproject.toml' in os.listdir(current_path) or '.git' in os.listdir(current_path):
            return current_path
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:  # 루트 디렉토리에 도달했거나 더 이상 올라갈 곳이 없는 경우
            break
        current_path = parent_path
    return None  # 만약 프로젝트 루트를 찾지 못하면 None을 반환


PROJECT_ROOT = find_project_root()


def get_relative_path(relative_path):
    """프로젝트 루트를 기준으로 상대 경로를 절대 경로로 변환."""
    if not PROJECT_ROOT:
        raise EnvironmentError("프로젝트 루트를 찾을 수 없습니다.")
    return os.path.join(PROJECT_ROOT, relative_path)


def get_current_module_path():
    """현재 이 모듈이 위치한 경로를 반환."""
    return os.path.dirname(os.path.abspath(__file__))


def combine_relative_path(*args):
    """여러 경로를 결합하고, 상대 경로를 절대 경로로 변환."""
    return os.path.abspath(os.path.join(*args))


def ensure_dir(path):
    """디렉토리가 존재하지 않으면 생성."""
    os.makedirs(path, exist_ok=True)
    return path


def is_path_within_project(path):
    """주어진 경로가 프로젝트 경로 내에 있는지 확인."""
    return os.path.commonpath([PROJECT_ROOT, os.path.abspath(path)]) == PROJECT_ROOT

