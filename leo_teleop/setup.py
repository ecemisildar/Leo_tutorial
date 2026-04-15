from setuptools import find_packages, setup

package_name = 'leo_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ecem',
    maintainer_email='you@example.com',
    description='Basic Leo Rover teleop package',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'leo_teleop_node = leo_teleop.leo_teleop_node:main',
        ],
    },
)