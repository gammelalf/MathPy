import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gammelmath",
    version="0.0.1",
    author="Wolfgang Fischer",
    author_email="31348226+gammelalf@users.noreply.github.com",
    description="A fun project for parsing arithmetic expressions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gammelalf/gammelmath",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
