from sqlalchemy import event
from sqlalchemy.sql import expression

from app import db
from wts.db import ModelMixin


class Case(ModelMixin, db.Model):
    """
    Tets layout.

    Test cases.
    Field name required.
    """

    __tablename__ = 'test'
    __bind_key__ = 'test_cases'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    expected = db.Column(db.PickleType)
    input = db.Column(db.PickleType)
    func = db.Column(db.PickleType)
    klass = db.Column(db.PickleType, nullable=False)
    event = db.Column(db.String)
    unique = db.Column(
        db.Boolean, server_default=expression.false(), nullable=False
    )

    @property
    def input_expected(self):
        """
        Quick access to object data.

        Parameters
        ----------


        Returns
        -------
        type: tuple
            Tuple fields input, expected.

        """
        return self.input, self.expected


@event.listens_for(Case.input, 'set')
def validate_input(target, value, oldvalue, initiator):
    """
    Work with key 'html' in value.

    Remove all this symbols begin and end string: \t \n \r \v.

    Example:
        from: ' <div></div> '
        to: '<div></div>'

        from: '\n    <a href="#" class="btn btn-primary">Go somewhere</a>\n  '
        to: '<a href="#" class="btn btn-primary">Go somewhere</a>'

        from: '
            <a href="#" class="btn btn-primary">
                Go somewhere
            </a>
            '
        to: '<a href="#" class="btn btn-primary">Go somewhere</a>'

    Return cleared data.
    """

    if 'html' in value:
        value['html'] = ''.join(
            [line.strip() for line in str(value['html']).splitlines()]
        )

    return value
