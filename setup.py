import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swiveling_arcs_screensaver",
    version="0.0.1",
    description="A very simple Python framework for making screen savers for Windows. Uses the Arcade library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SirGnip/swiveling_arcs_screensaver",

    # Code is in "src/", an un-importable directory (at least not easily or accidentally)
    # Helps reduce confusion around whether code from repo or site-packages is being used.
    # https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
    # https://hynek.me/articles/testing-packaging/
    # https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],

    python_requires='>=3.7',
    install_requires=[
        # 3rd party dependencies
        "arcade>=2.4.3",
        "arcade-curtains>=0.2.1",
        # personal dependencies
        "arcade_screensaver_framework @ http://github.com/SirGnip/arcade_screensaver_framework/tarball/5ed8e2d903750a0577b029292aa7518a78cd9954",
        "arcade_examples @ http://github.com/SirGnip/arcade_examples/tarball/9047aedd898a1ae0c870da379880cd584e96aee4",
    ],
)
