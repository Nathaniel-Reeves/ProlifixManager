from sqlalchemy import Integer, Column, String, Boolean, Enum, JSON, create_engine, select, ForeignKey
import datetime
from enum import Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declared_attr

class ACR(Enum):
    """
    Access Control Roles
    """
    ADMIN = 'admin'
    BATCHER = 'batcher'
    QC_MANAGER = 'qc_manager'
    PRODUCTION_MANAGER = 'production_manager'
    TEAM_LEADER = 'team_leader'
    USER = 'user'

class ACR_Column(Column):
    inherit_cache = True
    def __init__(self, *args, **kwargs):

        self.select_acr = kwargs.pop('select_acr', None)
        self.update_acr = kwargs.pop('update_acr', None)
        self.delete_acr = kwargs.pop('delete_acr', None)
        self.insert_acr = kwargs.pop('insert_acr', None)

        if self.select_acr:
            for acr in self.select_acr:
                if not isinstance(acr, ACR):
                    raise ValueError('select_acr must be of type AccessControlRole')

        if self.update_acr:
            for acr in self.update_acr:
                if not isinstance(acr, ACR):
                    raise ValueError('update_acr must be of type AccessControlRole')

        if self.delete_acr:
            for acr in self.delete_acr:
                if not isinstance(acr, ACR):
                    raise ValueError('delete_acr must be of type AccessControlRole')

        if self.insert_acr:
            for acr in self.insert_acr:
                if not isinstance(acr, ACR):
                    raise ValueError('insert_acr must be of type AccessControlRole')

        super().__init__(*args, **kwargs)

    def get_restricted_acr(self):
        return self.restricted_acr

    def get_allowed_acr(self):
        return self.allowed_acr

class MyMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__ = {'always_refresh': True}

    def as_dict(self):
        """
            Returns a dictionary representation of the object.
            """
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

Base = declarative_base()

class Organizations(Base, MyMixin):
    __tablename__ = 'Organizations'

    organization_id = Column(
        Integer,
        primary_key=True
    )

    date_entered = Column(
        String(100),
        nullable=False,
        default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    website_url = Column(
        String(100),
        nullable=True
    )

    vetted = ACR_Column(
        Boolean,
        nullable=False,
        default=False,
        select_acr=[ACR.ADMIN, ACR.QC_MANAGER],
        update_acr=[ACR.ADMIN, ACR.QC_MANAGER],
        insert_acr=[ACR.ADMIN, ACR.QC_MANAGER],
        delete_acr=[ACR.ADMIN, ACR.QC_MANAGER]
    )

    date_vetted = ACR_Column(
        String(100),
        nullable=False,
        default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        select_acr=[ACR.ADMIN, ACR.QC_MANAGER],
        update_acr=[ACR.ADMIN, ACR.QC_MANAGER],
        insert_acr=[ACR.ADMIN, ACR.QC_MANAGER],
        delete_acr=[ACR.ADMIN, ACR.QC_MANAGER]
    )

    risk_level = ACR_Column(
        String(100),
        default='UNKNOWN',
        select_acr=[ACR.ADMIN, ACR.QC_MANAGER],
        update_acr=[ACR.ADMIN, ACR.QC_MANAGER],
        insert_acr=[ACR.ADMIN, ACR.QC_MANAGER],
        delete_acr=[ACR.ADMIN, ACR.QC_MANAGER]
    )

    supplier = Column(
        Boolean,
        nullable=False,
        default=False
    )

    client = Column(
        Boolean,
        nullable=False,
        default=False
    )

    lab = Column(
        Boolean,
        nullable=False,
        default=False
    )

    courier = Column(
        Boolean,
        nullable=False,
        default=False
    )

    other = Column(
        Boolean,
        nullable=False,
        default=False
    )

    doc = Column(
        JSON,
        nullable=False,
        default=dict()
    )

    notes = Column(
        String(2500),
        nullable=False,
        default=None
    )

    def __init__(self, *args, **kwargs):

        if len(args) == 0:
            self.organization_id = kwargs.pop('organization_id', None)
            self.date_entered = kwargs.pop('date_entered', None)
            self.website_url = kwargs.pop('website_url', None)
            self.vetted = kwargs.pop('vetted', None)
            self.date_vetted = kwargs.pop('date_vetted', None)
            self.risk_level = kwargs.pop('risk_level', None)
            self.supplier = kwargs.pop('supplier', None)
            self.client = kwargs.pop('client', None)
            self.lab = kwargs.pop('lab', None)
            self.courier = kwargs.pop('courier', None)
            self.other = kwargs.pop('other', None)
            self.doc = kwargs.pop('doc', None)
            self.notes = kwargs.pop('notes', None)
        else:
            self.organization_id = args[0]


class Organization_Names(Base, MyMixin):
    __tablename__ = 'Organization_Names'

    name_id = Column(
        Integer,
        primary_key=True
    )

    organization_id = Column(
        Integer,
        ForeignKey('Organizations.organization_id'),
        nullable=False
    )

    organization_name = Column(
        String(200),
        nullable=False
    )

    organization_initial = Column(
        String(10),
        nullable=False
    )

    primary_name = Column(
        Boolean,
        nullable=False,
        default=False
    )

    def __init__(self, name_id, organization_id,
                    organization_name, organization_initial,
                    primary_name
                    ):
        self.name_id = name_id
        self.organization_id = organization_id
        self.organization_name = organization_name
        self.organization_initial = organization_initial
        self.primary_name = primary_name

def sqlalchemy_test():

    user = 'root'
    # user_roles = [ACR.ADMIN]
    password = 'Newspaper5'
    host = '192.168.1.133'
    port = '3306'
    database = 'Organizations'

    # user = 'client'
    user_roles = [ACR.USER]
    # password = 'ClientPassword!5'

    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

    def check_acr(user_roles, tables=[], action="select"):
        query_col = []
        col_names = []
        for table in tables:
            for column in table.__table__.columns:
                if isinstance(column, ACR_Column):
                    col_action = eval("column." + action + "_acr")
                    if isinstance(col_action, type(None)) or \
                            bool(set(col_action) & set(user_roles)):

                        query_col.append(eval(table.__tablename__ + "." + column.name))
                        col_names.append(column.name)
                        continue
                else:
                    query_col.append(eval(table.__tablename__ + "." + column.name))
                    col_names.append(column.name)

        return query_col, col_names

    out, names = check_acr(user_roles, tables=[Organizations, Organization_Names])
    # print(*names)

    statment = select(*out).join_from(
        Organizations,
        Organization_Names
        ).where(
            Organizations.supplier == True
            ).where(
                Organization_Names.primary_name == True)

    with engine.connect() as conn:
        data = conn.execute(statment)

    session = sessionmaker(bind=engine)
    Session = session()
    # populate_existing = True forces the session to query the database instead of looking in cache
    result = Session.get(Organizations, 1, populate_existing=True)
    print(dir(result))
    print(result.as_dict())

    organizations = [row._asdict() for row in data]
    return organizations


if __name__ == '__main__':
    # print(sqlalchemy_test())
    sqlalchemy_test()
