import pytest
from project import create_app


@pytest.fixture
def app():
    application = create_app()

    application.app_context().push()
    # Initialise the DB
    #application.db.create_all()

    return application

@pytest.fixture
def client(app):
    with app.test_client() as c:
        yield c
