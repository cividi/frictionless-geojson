from pytest_cov.embed import cleanup_on_sigterm

# Cleanups

cleanup_on_sigterm()

# Settings


def pytest_addoption(parser):
    parser.addoption(
        "--ci",
        action="store_true",
        dest="ci",
        default=False,
        help="enable integrational tests",
    )


def pytest_configure(config):
    if not config.option.ci:
        expr = getattr(config.option, "markexpr")
        setattr(config.option, "markexpr",
                "{expr} and not ci" if expr else "not ci")
