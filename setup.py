from setuptools import setup, find_packages

setup(
    name="storage-allocation-manager",
    version="0.1.0",
    description="An inventory management system with warehouse tracking",
    author="S.A.M",
    packages=find_packages(),
    install_requires=[
        "dnspython==2.7.0",
        "flet==0.25.1",
        "flet-desktop==0.25.1",
        "h11==0.14.0",
        "httpcore==1.0.7",
        "httpx==0.28.0",
        "idna==3.10",
        "oauthlib==3.2.2",
        "pymongo==4.10.1",
        "python-dotenv==1.0.1"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
) 