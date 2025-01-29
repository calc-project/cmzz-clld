from pathlib import Path

from clld.web.assets import environment

import cmzz


environment.append_path(
    Path(cmzz.__file__).parent.joinpath('static').as_posix(),
    url='/cmzz:static/')
environment.load_path = list(reversed(environment.load_path))
