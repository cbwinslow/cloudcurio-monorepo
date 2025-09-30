"""
CloudCurio - AI-Powered Development Platform
Setup file for PyPI distribution
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements from requirements files
def read_requirements():
    requirements = []
    
    # Read core requirements
    with open('crew/requirements.txt', 'r') as f:
        requirements.extend(f.read().splitlines())
    
    # Read config editor requirements
    with open('config_editor/requirements.txt', 'r') as f:
        config_reqs = f.read().splitlines()
        # Filter out requirements already included
        for req in config_reqs:
            if req not in requirements and req.strip() and not req.startswith('#'):
                requirements.append(req)
    
    return requirements

setup(
    name="cloudcurio",
    version="2.0.0",
    author="Blaine Winslow",
    author_email="blaine.winslow@gmail.com",
    description="AI-Powered Development Platform for code review, documentation, and vulnerability assessment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cbwinslow/cloudcurio",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    install_requires=read_requirements(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    entry_points={
        'console_scripts': [
            'cloudcurio=cli:main',
            'cloudcurio-mcp=crew.mcp_server.start_server:main',
            'cloudcurio-sysmon=sysmon.cli:main',
            'cloudcurio-config-editor=config_editor.launcher:main',
        ],
    },
    include_package_data=True,
    keywords="ai, crewai, development, automation, code-review, documentation, security",
    project_urls={
        'Bug Reports': 'https://github.com/cbwinslow/cloudcurio/issues',
        'Source': 'https://github.com/cbwinslow/cloudcurio/',
        'Documentation': 'https://github.com/cbwinslow/cloudcurio/docs',
    }
)