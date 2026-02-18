from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import (OperationalError,
                            InterfaceError,
                            InternalError,
                            IntegrityError,
                            DataError,
                            ProgrammingError,
                            SQLAlchemyError)


def init_error_handlers(app: Flask):
    @app.errorhandler(HTTPException)
    def http_exception_handler(exception: HTTPException):
        response_code = exception.code if exception.code else 500
        description = exception.description if exception.description else "Internal Server Error"
        return jsonify({"error": description}), response_code

    @app.errorhandler(OperationalError)
    @app.errorhandler(InterfaceError)
    @app.errorhandler(InternalError)
    @app.errorhandler(IntegrityError)
    @app.errorhandler(DataError)
    @app.errorhandler(ProgrammingError)
    @app.errorhandler(SQLAlchemyError)
    def handle_database_connection_error(exception: OperationalError | InterfaceError):
        return jsonify({"error": exception.__cause__}), 500
