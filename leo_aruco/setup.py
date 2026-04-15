from setuptools import setup
import os


package_name = 'leo_aruco'


setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ecem',
    description='RGB camera viewer with ArUco marker detection for Leo Rover',
    data_files=[
        ('share/ament_index/resource_index/packages', [os.path.join('resource', package_name)]),
        (os.path.join('share', package_name), ['package.xml']),
    ],
    entry_points={
        'console_scripts': [
            'aruco_detector = leo_aruco.aruco_detector_node:main',
        ],
    },
)
