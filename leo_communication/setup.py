from setuptools import setup

package_name = 'leo_communication'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ecem',
    description='Simple robot communication',
    entry_points={
        'console_scripts': [
            'sender = leo_communication.sender:main',
            'receiver = leo_communication.receiver:main',
        ],
    },
)