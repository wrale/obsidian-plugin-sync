from setuptools import setup

setup(
    name="obsidian-plugin-sync",
    version="0.1.0",
    description="A tool for syncing Obsidian plugin development files to your Obsidian vault",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Joshua M. Dotson",
    author_email="contact@jmdots.com",
    url="https://github.com/wrale/obsidian-plugin-sync",
    py_modules=["obsidian_plugin_sync"],
    entry_points={
        "console_scripts": [
            "obsidian-plugin-sync=obsidian_plugin_sync:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires=">=3.6",
    extras_require={
        "watch": ["watchdog"],
    },
)
