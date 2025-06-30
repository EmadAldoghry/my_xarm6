import os
from glob import glob
from setuptools import setup

package_name = 'my_xarm6_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # BEGIN: ADDED SECTION
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'meshes', 'xarm6', 'visual'), glob('meshes/xarm6/visual/*')),
        (os.path.join('share', package_name, 'meshes', 'xarm6', 'collision'), glob('meshes/xarm6/visual/*')), # Note: using visual for collision
        (os.path.join('share', package_name, 'meshes', 'end_tool', 'visual'), glob('meshes/end_tool/visual/*')),
        (os.path.join('share', package_name, 'meshes', 'end_tool', 'collision'), glob('meshes/end_tool/collision/*')),
        # END: ADDED SECTION
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@todo.com',
    description='Simplified description for xArm6',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)