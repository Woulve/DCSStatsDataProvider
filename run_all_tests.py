import os, pathlib
import pytest


os.chdir( pathlib.Path.cwd() / 'test' )

pytest.main()