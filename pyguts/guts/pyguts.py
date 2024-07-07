# pylint: disable=too-many-instance-attributes,too-many-public-methods
class PyGuts(
    _ArgumentsManager,
    _MessageStateHandler,
    reporters.ReportsHandlerMixIn,
    checkers.BaseChecker,
):
    """Checks Python modules using external checkers.

    This is the main checker controlling the other ones and the reports
    generation. It is itself both a raw checker and an astroid checker in order
    to:
    * handle message activation / deactivation at the module level
    * handle some basic but necessary stats' data (number of classes, methods...)

    This class needs to support pickling for parallel gutsing to work. The exception
    is reporter member; see check_parallel function for more details.
    """