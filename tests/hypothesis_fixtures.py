import os

from hypothesis import Verbosity, settings

settings.register_profile(
    "ci",
    max_examples=100,
    deadline=None,
)
settings.register_profile(
    "dev",
    max_examples=10,
    deadline=None,
    verbosity=Verbosity.verbose,
)
settings.load_profile(os.getenv("TOOLBOX_HYPOTHESIS_PROFILE", "dev"))
