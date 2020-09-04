from cx_Freeze import setup, Executable

base = None

executables = [Executable("sternberg_test.pyw", base=base),
               Executable("hicks_test.pyw", base=base),
               Executable("maze_test.pyw", base=base)]

packages = ["os"]
options = {
    'build_exe': {
        'packages':packages,
        "excludes": ["tkinter"]
    },
}

setup(
    name = "CognitiveLoadTests",
    options = options,
    version = "2",
    description = 'CognitiveLoadTests app',
    executables = executables
)