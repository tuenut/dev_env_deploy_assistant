from setuptools import setup, find_packages


setup(
    name="tuenut-deploy-assistant",
    maintainer="tuenut",
    maintainer_email="unnetu@gmail.com",
    version="0.0.1",
    description="Helper to manage local dev environment with docker images "
                "and docker-compose",
    packages=find_packages("src", exclude=["tests", ]),
    package_dir={"": "src"},
    install_requires=[
        "loguru",
        "semantic-version==2.9.0"
    ],
    entry_points={
        "console_scripts": [
            "deploy-assist = deploy_assistant:run_assistant"
        ]
    }
)
