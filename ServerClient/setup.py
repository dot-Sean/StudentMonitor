from cx_Freeze import setup, Executable

setup(name="ServerSM", version="1.0", description="", executables=[Executable("web_app/run.py")],)