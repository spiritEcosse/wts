"""Base Model."""


class ModelMixin:
    """Base Model with hooks methods."""

    def __repr__(self):
        """View object class."""
        return "<{}(name='{}')>".format(self.__class__.__name__, self.name)

    def save(self):
        """
        Save object to db.

        Return this object.
        """
        self.query.session.add(self)
        self.query.session.commit()
        return self

    def delete(self):
        """
        Delete object from db.

        Return this object.
        """
        self.query.session.delete(self)
        self.query.session.commit()
        return self
