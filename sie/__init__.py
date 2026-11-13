"""Stock Intelligence Engine core package.

Imports are lazy so dependency-light subpackages (including the investment
research core) remain usable without the optional dashboard/data dependencies.
"""

__all__ = ["analyze_watchlist", "run_report"]


def __getattr__(name):
    if name in __all__:
        from sie import analyzer
        return getattr(analyzer, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
