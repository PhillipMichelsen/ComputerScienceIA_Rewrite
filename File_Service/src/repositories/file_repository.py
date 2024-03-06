import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.models.files import Base, Files


class FileRepository:
    def __init__(self, database_url):
        self.engine = create_engine(database_url, pool_size=10, max_overflow=20)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.ScopedSession = scoped_session(self.session_factory)
        logging.info("Connected to postgres database, file_repository initialized.")

    def add_file(
        self,
        file_name,
        uuid,
        bucket_name,
        paragraph_count,
        embedded_paragraph_count,
        status,
    ):
        session = self.ScopedSession()
        try:
            new_file = Files(
                file_name=file_name,
                uuid=uuid,
                bucket_name=bucket_name,
                paragraph_count=paragraph_count,
                embedded_paragraph_count=embedded_paragraph_count,
                status=status,
            )
            session.add(new_file)
            session.commit()
            return new_file
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.ScopedSession.remove()

    def increment_embedded_paragraph_count_by_file_name(self, file_name, count):
        session = self.ScopedSession()
        try:
            session.query(Files).filter(Files.file_name == file_name).update(
                {Files.embedded_paragraph_count: Files.embedded_paragraph_count + count}
            )

            session.query(Files).filter(Files.file_name == file_name).filter(
                Files.embedded_paragraph_count == Files.paragraph_count
            ).update({Files.status: "completed"})

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.ScopedSession.remove()

    def set_paragraph_count_by_file_name(self, file_name, count):
        session = self.ScopedSession()
        try:
            session.query(Files).filter(Files.file_name == file_name).update(
                {Files.paragraph_count: count}
            )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.ScopedSession.remove()

    def get_all_files(self):
        session = self.ScopedSession()
        try:
            return session.query(Files).all()
        finally:
            self.ScopedSession.remove()

    def get_file_by_id(self, file_id):
        session = self.ScopedSession()
        try:
            return session.query(Files).filter(Files.id == file_id).first()
        finally:
            self.ScopedSession.remove()

    def get_file_by_object_name(self, object_name):
        session = self.ScopedSession()
        try:
            return session.query(Files).filter(Files.object_name == object_name).first()
        finally:
            self.ScopedSession.remove()

    def get_file_by_file_name(self, file_name):
        session = self.ScopedSession()
        try:
            return session.query(Files).filter(Files.file_name == file_name).first()
        finally:
            self.ScopedSession.remove()

    def remove_file_by_id(self, file_id):
        session = self.ScopedSession()
        try:
            session.query(Files).filter(Files.id == file_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.ScopedSession.remove()
