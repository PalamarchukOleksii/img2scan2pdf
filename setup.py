from setuptools import setup, find_packages

setup(
    name="img2scan2pdf",
    version="0.1.0",
    author="Oleksii Palamarchuk",
    author_email="oleksiypalamarchuck@gmail.com",
    description="A CLI tool to process images and convert them to a PDF.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PalamarchukOleksii/img2scan2pdf",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "img2scan2pdf=img2scan2pdf.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
