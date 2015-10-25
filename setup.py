import setuptools

setuptools.setup(
    name='peacock',
    version='0.1',
    description="""Simple forgetful image viewer.""",
    author='Tim Simpson',
    url='http://border-town.com',
    require='PIL',
    py_modules=[],
    entry_points={
        'console_scripts': [
            'peacock-create = peacock.cmds.create:main',
        ]
    }
)
