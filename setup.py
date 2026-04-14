from setuptools import setup

package_name = 'leo_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@example.com',
    description='Basic teleop node for Leo Rover',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'leo_teleop_node = leo_teleop.leo_teleop_node:main',
        ],
    },
)