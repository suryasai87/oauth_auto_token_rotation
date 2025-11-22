#!/usr/bin/env python3
"""
Setup script for Databricks OAuth Auto Token Rotation
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="databricks-oauth-rotator",
    version="1.0.0",
    author="Databricks Community",
    author_email="",
    description="Automatic OAuth token rotation for Databricks PostgreSQL (Lakebase) connections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suryasai87/oauth_auto_token_rotation",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'databricks_oauth_rotator': ['templates/*.template'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyJWT>=2.0.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "databricks-oauth-rotator=databricks_oauth_rotator.cli:main",
            "databricks-oauth-install=databricks_oauth_rotator.install:install_command",
            "databricks-oauth-uninstall=databricks_oauth_rotator.install:uninstall_command",
            "databricks-oauth-status=databricks_oauth_rotator.install:status_command",
            "databricks-oauth-restart=databricks_oauth_rotator.install:restart_command",
        ],
    },
    keywords="databricks oauth token rotation postgresql lakebase automation",
    project_urls={
        "Bug Reports": "https://github.com/suryasai87/oauth_auto_token_rotation/issues",
        "Source": "https://github.com/suryasai87/oauth_auto_token_rotation",
        "Documentation": "https://github.com/suryasai87/oauth_auto_token_rotation#readme",
    },
)
