import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sinupy",
    version="0.1.1",
    author="Wenyin Wei",
    author_email="wenyin.wei@ipp.ac.cn",
    description="The sinupy package make it convenient to analyze the characteristic sinusoidal waves propagating in various kinds of medium. Typical waves in plasma have been given in the code to demonstrate how the package works and other users are free to follow the steps to research on their medium or charcteristic waves of interest.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WenyinWei/sinupy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)