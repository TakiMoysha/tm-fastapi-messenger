from logging import getLogger

logger = getLogger(__name__)


def test_syntax_app_exceptions():
    from app import exceptions as exc

    assert isinstance(exc.BaseAppError(), exc.BaseAppError)
    assert isinstance(exc.BaseAppError(status_code=1), exc.BaseAppError)
    assert isinstance(exc.BaseAppError(detail="test"), exc.BaseAppError)

    assert isinstance(exc.UnauthorizedError(), exc.BaseAppError)
    assert isinstance(exc.UnauthorizedError(status_code=1), exc.BaseAppError)
    assert isinstance(exc.UnauthorizedError(detail="test"), exc.BaseAppError)

    assert isinstance(exc.PermissionDeniedError(), exc.BaseAppError)
    assert isinstance(exc.PermissionDeniedError(status_code=1), exc.BaseAppError)
    assert isinstance(exc.PermissionDeniedError(detail="test"), exc.BaseAppError)

    assert isinstance(exc.WorkInProgressError(), exc.WorkInProgressError)
    assert isinstance(exc.WorkInProgressError(status_code=1), exc.BaseAppError)
    assert isinstance(exc.WorkInProgressError(detail="test"), exc.BaseAppError)
