from fastapi import HTTPException


class NotFoundError(BaseException):
    pass


class AuthenticationError(BaseException):
    pass


class ExistsError(BaseException):
    pass


class DifferentUuidsError(ValueError):
    def __str__(self):
        return 'Different uuids in path and in schema.'


def try_except_decorator(handler):
    async def wrapper(*args, **kwargs):
        try:
            res = await handler(*args, **kwargs)
        except (ValueError, ExistsError) as ex:
            raise HTTPException(400, detail={
                'data': None,
                'details': str(ex)
            })
        except AuthenticationError as ex:
            raise HTTPException(401, detail={
                'data': None,
                'details': str(ex)
            })
        except PermissionError as ex:
            raise HTTPException(403, detail={
                'data': None,
                'details': str(ex)
            })
        except NotFoundError as ex:
            raise HTTPException(404, detail={
                'data': None,
                'details': str(ex)
            })
        except Exception as ex:
            raise HTTPException(500, detail={
                'data': None,
                'details': str(ex)
            })
        else:
            return res

    # Fix signature of wrapper
    import inspect
    wrapper.__signature__ = inspect.Signature(
        parameters=[
            # Use all parameters from handler
            *inspect.signature(handler).parameters.values(),
            # Skip *args and **kwargs from wrapper parameters:
            *filter(
                lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
                inspect.signature(wrapper).parameters.values()
            )
        ],
        return_annotation=inspect.signature(handler).return_annotation,
    )
    return wrapper
