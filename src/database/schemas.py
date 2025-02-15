import uuid
import json
from sqlalchemy import (Column, DateTime, ForeignKey,
                        func, Integer, String,
                        Boolean, Float, ARRAY,
                        Text, LargeBinary, Enum,
                        CheckConstraint, Date,  JSON)
from sqlalchemy.dialects.postgresql import UUID, DATERANGE, TSRANGE, ENUM
from sqlalchemy.orm import declarative_base, relationship
import datetime


#class ChatType(ENUM):
#    name = "Smth"
#    telegram = 'telegram'
#    whatsapp = 'whatsapp'
#    avito = 'avito'
#    vk = 'vk'
#    instagram = 'instagram'
#    facebook = 'facebook'
#    webim = 'webim'


ChatType = ENUM(
    name="Smth",
    telegram='telegram',
    whatsapp = 'whatsapp',
    avito = 'avito',
    vk = 'vk',
    instagram = 'instagram',
    facebook = 'facebook',
    webim = 'webim'
)

Base = declarative_base()


class User(Base):
    """
    The User class represents a user model in the database.

    Attributes:
        id (UUID): Unique user identifier (primary key). Generated automatically.
        username (String): User's username. Required field. Must be unique.
        email (String): User's email address. Required field. Must be unique and in valid email format.
        password (String): User's password. Required field.  Stored as a hash for security.
        created_at (DateTime): Date and time of user account creation. Set automatically.
        is_active (Boolean): Indicates if the user account is active. Default is True.

    Methods:
        __repr__(): Returns a string representation of the User query in JSON format.
        to_dict(): Returns a dictionary, sequentially user data, where the keys are the names of the table columns.

    Table:
        Table name: user
        Schema: Defined by the settings in config.settings.SCHEMA

    Relationships:
        One-to-many relationship with the balance table (one user may have multiple balance records).
        Use `back_populates="user"` in Balance models for two-way relationship.
    """
    __tablename__ = 'users'
    __table_args__ = {'schema': "asclavia_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
    is_active = Column(Boolean, nullable=False, default=True)
    phone_number = Column(String(20), nullable=False)

    chats = relationship("Chat", back_populates="user")
    balances = relationship("Balance", back_populates="user")
    cdrs = relationship("CDR", back_populates="user")
    crms = relationship("CRM", back_populates="user")
    pjsip_endpoints = relationship("PJSIPEndpoint", back_populates="user")
    scenarios = relationship("Scenario", back_populates="user")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Balance(Base):
    """
    The Balance class represents a user balance model in the database.

    Attributes:
        id (UUID): Unique balance identifier (primary key). Generated automatically.
        value (Integer): Balance value. Required field.
        created_at (DateTime): Date and time of record creation. Set automatically.
        user_id (UUID): User identifier that belongs to the balance (foreign key).
    Associated with the users table.
        user (relationships): Relationship with the User model. Provides access to information about the user that belongs to the balance.

    Methods:
        __repr__(): Returns a string representation of the Balance query in JSON format.
        to_dict(): Returns a dictionary, sequentially balance data, where the keys are the names of the table columns.

    Table:
        Table name: balance
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        One-to-many relationship with the users table (one user may have multiple balance records).
        Use `back_populates="balances"` in User models for two-way relationship.
    """
    __tablename__ = "balance"
    __table_args__ = {'schema': "asclavia_schema"}

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    value = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey(f"{"asclavia_schema"}.users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="balances")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Bill(Base):
    """
    The Bill class represents a bill record in the database.

    Attributes:
        id (UUID): Unique bill identifier (primary key). Generated automatically.
        amount (Float): The initial amount of the bill. Required field.
        period (DATERANGE): The billing period represented as a date range.  Required field.
        created_at (DateTime): Date and time of bill creation. Required field.
        user_id (UUID): Foreign key referencing the user who owns the bill.  Links to the `users.id` column. Required field.
          Cascading delete enabled (ondelete="CASCADE").
        count_mins (Integer): The number of minutes used during the billing period. Required field.
        count_messages (Integer): The number of messages sent during the billing period. Required field.
        rates (Float): The rates applied to the bill. Required field.
        total (Float): The total amount of the bill after applying rates. Required field.

    Methods:
        __repr__(): Returns a string representation of the Bill object in JSON format.
        to_dict(): Returns a dictionary representation of the bill, where the keys are the names of the table columns.

    Table:
        Table name: bills
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        One-to-many relationship with the User table (one user may have multiple bills).
        Access bills associated with a user through the `user` attribute (e.g., `bill.user`).
        Users can access their bills through the `bills` backref attribute on the User object (e.g., `user.bills`).
    """
    __tablename__ = "bills"
    __table_args__ = {'schema': "asclavia_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    amount = Column(Float, nullable=False)
    period = Column(DATERANGE, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(f"{"asclavia_schema"}.users.id", ondelete="CASCADE"),
                     nullable=False)
    count_mins = Column(Integer, nullable=False)
    count_messages = Column(Integer, nullable=False)
    rates = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    user = relationship("User", backref="bills")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class CallDescription(Base):
    """
    The CallDescription class represents a call description model in the database.

    Attributes:
        id (UUID): Unique call description identifier (primary key). Generated automatically.
        messages (ARRAY(Text)): An array of text messages describing the call. Required field.

    Methods:
        __repr__(): Returns a string representation of the CallDescription object in JSON format.
        to_dict(): Returns a dictionary representation of the CallDescription object,
                   where keys are column names and values are corresponding attribute values.

    Table:
        Table name: call_description
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        One-to-many relationship with the Call table (one call description may be associated with multiple calls).
        Use `back_populates="description"` in Call models for a two-way relationship.
    """
    __tablename__ = 'call_description'
    __table_args__ = {'schema': "asclavia_schema"}

    id = Column(UUID, primary_key=True, default=uuid.uuid4())
    messages = Column(ARRAY(Text), nullable=False)

    calls = relationship("Call", back_populates="description")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Call(Base):
    """
    The Call class represents a call record in the database.

    Attributes:
        id (UUID): Unique call identifier (primary key). Generated automatically.
        telephone_number (String): The telephone number associated with the call. Required field. Maximum length is 20 characters.
        status (String): The status of the call (e.g., "completed", "failed"). Required field. Maximum length is 255 characters.
        call_time (DateTime): The date and time of the call. Required field. Stores timezone information.
        duration (Float): The duration of the call in seconds. Required field.
        price (Float): The price of the call. Required field.
        result (String): The result of the call. Required field.
        created_at (DateTime): The date and time when the call record was created. Required field. Stores timezone information.
        description_id (UUID): Foreign key referencing the `call_description` table.  Links the call to its description.  Required field.
        income_call (UUID, optional): Foreign key referencing the `telephone_income` table.  Links the call to an incoming call record.  Nullable.
        outcome_call (UUID, optional): Foreign key referencing the `telephone_outcome` table.  Links the call to an outgoing call record. Nullable.

    Relationships:
        description (relationship): One-to-one relationship with the CallDescription model.  `back_populates="calls"` is used in CallDescription model for two-way access.
        telephone_income (relationship): One-to-one relationship with the TelephoneIncome model.  `back_populates="calls"` is used in TelephoneIncome model for two-way access.
        telephone_outcome (relationship): One-to-one relationship with the TelephoneOutcome model. `back_populates="calls"` is used in TelephoneOutcome model for two-way access.

    Methods:
        __repr__(): Returns a string representation of the Call object in JSON format.
        to_dict(): Returns a dictionary representation of the Call object, where keys are column names and values are corresponding attributes.

    Table:
        Table name: calls
        Schema: Defined by the settings in config.'asclavia_schema'

    Foreign Keys:
        description_id: References the id column in the call_description table.  ON DELETE CASCADE behavior.
        income_call: References the id column in the telephone_income table. ON DELETE CASCADE behavior.  Nullable.
        outcome_call: References the id column in the telephone_outcome table. ON DELETE CASCADE behavior.  Nullable.
    """
    __tablename__ = "calls"
    __table_args__ = {'schema': "asclavia_schema"}

    id = Column(UUID, primary_key=True, default=uuid.uuid4())
    telephone_number = Column(String(20), nullable=False)
    status = Column(String(255), nullable=False)
    call_time = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    result = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    description_id = Column(UUID(as_uuid=True),
                            ForeignKey(f"{"asclavia_schema"}.call_description.id", ondelete="CASCADE"),
                            nullable=False)
    income_call = Column(UUID(as_uuid=True),
                         ForeignKey(f"{"asclavia_schema"}.telephone_income.id", ondelete="CASCADE"),
                         nullable=True)
    outcome_call = Column(UUID(as_uuid=True),
                          ForeignKey(f"{"asclavia_schema"}.telephone_outcome.id", ondelete="CASCADE"),
                          nullable=True)

    description = relationship("CallDescription", back_populates="calls")
    telephone_income = relationship("TelephoneIncome", back_populates="calls")
    telephone_outcome = relationship("TelephoneOutcome", back_populates="calls")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CDR(Base):
    """
    The User class represents a user model in the database.

    Attributes:
        id (UUID): Unique user identifier (primary key). Generated automatically.
        username (String): User's username. Required field. Must be unique.
        email (String): User's email address. Required field. Must be unique and in valid email format.
        password (String): User's password. Required field.  Stored as a hash for security.
        created_at (DateTime): Date and time of user account creation. Set automatically.
        is_active (Boolean): Indicates if the user account is active. Default is True.

    Methods:
        __repr__(): Returns a string representation of the User query in JSON format.
        to_dict(): Returns a dictionary, sequentially user data, where the keys are the names of the table columns.

    Table:
        Table name: user
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        One-to-many relationship with the balance table (one user may have multiple balance records).
        Use `back_populates="user"` in Balance models for two-way relationship.
    """
    __tablename__ = 'cdr'
    __table_args__ = {'schema': 'asclavia_schema'}

    id = Column(UUID, primary_key=True, default=uuid.uuid4())
    uniqueid = Column(String(255), nullable=False)
    caller_id = Column(String(255), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    disposition = Column(String(255), nullable=False)
    duration = Column(Integer, nullable=False)
    recording_path = Column(Text, nullable=False)
    transcription_text = Column(Text)
    record = Column(LargeBinary)
    user_id = Column(UUID, ForeignKey(f'{'asclavia_schema'}.users.id'), nullable=False)

    user = relationship("User", back_populates="cdrs")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Chat(Base):
    """
    The Chat class represents a chat model in the database.

    Attributes:
        id (UUID): Unique chat identifier (primary key). Generated automatically.
        scenario_name (String): Name of the scenario associated with the chat. Required field.
        robots_name (String): Name of the robot used in the chat. Required field.
        chat_url (String): URL of the chat. Required field.
        chat_type (ChatType): Type of chat. Required field.
        user_id (UUID): Foreign key referencing the user who owns the chat.  Required field.  Cascades on delete.
        chat_name (String): Name of the chat. Required field.
        token (String): Authentication token for the chat. Required field.

    Methods:
        __repr__(): Returns a string representation of the Chat object in JSON format.
        to_dict(): Returns a dictionary, sequentially chat data, where the keys are the names of the table columns.

    Table:
        Table name: chat
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        One-to-many relationship with the User table (one user may have multiple chats).
        Use `back_populates="chats"` in User models for two-way relationship.
    """
    __tablename__ = 'chat'
    __table_args__ = {'schema': 'asclavia_schema'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    scenario_name = Column(String(255), nullable=False)
    robots_name = Column(String(255), nullable=False)
    chat_url = Column(String(255), nullable=False)
    chat_type = Column(ChatType, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(f'{'asclavia_schema'}.users.id', ondelete="cascade"),
                     nullable=False)
    chat_name = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False)

    user = relationship("User", back_populates="chats")
    dialogs = relationship("Dialog", back_populates="chat")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CRM(Base):
    """
    The CRM class represents a CRM integration model in the database.

    Attributes:
        id (UUID): Unique CRM integration identifier (primary key). Generated automatically.
        scenario_name (String): Name of the scenario associated with the CRM integration. Required field.
        robots_name (String): Name of the robots involved in the CRM integration. Required field.
        chat_url (String): URL for the chat associated with the CRM integration. Required field.
        is_AMOCRM (Boolean): Indicates if the CRM is AMOCRM. Required field.
        integration_name (String): Name of the integration. Required field.
        variables (ARRAY(String)): Array of variables used in the CRM integration.
        send_token (Boolean): Indicates whether to send a token. Defaults to False.
        action (String): Action to be performed in the CRM integration. Required field.
        fields (ARRAY(String)): Array of fields used in the CRM integration.
        user_id (UUID): Foreign key referencing the user who owns this CRM integration. Required field.

    Methods:
        __repr__(): Returns a string representation of the CRM object in JSON format.
        to_dict(): Returns a dictionary, sequentially CRM data, where the keys are the names of the table columns.

    Table:
        Table name: crm
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        Many-to-one relationship with the User table (many CRMs can belong to one user).
        Use `back_populates="crms"` in User models for two-way relationship.
    """
    __tablename__ = 'crm'
    __table_args__ = {'schema': 'asclavia_schema'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    scenario_name = Column(String(255), nullable=False)
    robots_name = Column(String(255), nullable=False)
    chat_url = Column(String(255), nullable=False)
    is_AMOCRM = Column(Boolean, nullable=False)
    integration_name = Column(String(255), nullable=False)
    variables = Column(ARRAY(String))
    send_token = Column(Boolean, nullable=False, default=False)
    action = Column(String(255), nullable=False)
    fields = Column(ARRAY(String))
    user_id = Column(UUID(as_uuid=True), ForeignKey(f'{'asclavia_schema'}.users.id', ondelete='cascade'), nullable=False)

    user = relationship("User", back_populates="crms")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class DialogDescription(Base):
    """
    The DialogDescription class represents a description of a dialog in the database.

    Attributes:
        id (UUID): Unique dialog description identifier (primary key). Generated automatically.
        messages (ARRAY(String)): An array of strings representing the messages in the dialog. Cannot be null.
        dialogs (relationship): A relationship to the Dialog table.  Allows access to Dialog objects that use this description.

    Methods:
        __repr__(): Returns a string representation of the DialogDescription object in JSON format.
        to_dict(): Returns a dictionary representation of the DialogDescription, where the keys are the names of the table columns.

    Table:
        Table name: dialog_description
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        One-to-many relationship with the Dialog table (one description may be used by multiple dialogs).
        Use `back_populates="description"` in Dialog models for two-way relationship.
    """
    __tablename__ = "dialog_description"
    __table_args__ = {'schema': 'asclavia_schema'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    messages = Column(ARRAY(String), nullable=False)
    dialogs = relationship("Dialog", back_populates="description")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Dialog(Base):
    """
    The Dialog class represents a dialog model in the database.

    Attributes:
        id (UUID): Unique dialog identifier (primary key). Generated automatically.
        name (String): Dialog's name. Required field. Max length 20 characters.
        created_at (DateTime): Date and time of dialog creation. Required field.
        update_at (DateTime): Date and time of last dialog update. Required field.
        type (ChatType):  Type of the chat. Required field.
        count_messages (Integer): Number of messages in the dialog. Required field.
        status (String): Dialog's status. Required field. Max length 20 characters.
        price (Float):  Price associated with the dialog. Required field.
        description_id (UUID): Foreign key referencing the dialog description. Required field.  Establishes a relationship with the DialogDescription table.  `ON DELETE CASCADE` ensures that if the associated description is deleted, the dialog is also deleted.
        chat_id (UUID): Foreign key referencing the chat. Required field. Establishes a relationship with the Chat table. `ON DELETE CASCADE` ensures that if the associated chat is deleted, the dialog is also deleted.

    Methods:
        __repr__(): Returns a string representation of the Dialog query in JSON format.
        to_dict(): Returns a dictionary, sequentially dialog data, where the keys are the names of the table columns.

    Table:
        Table name: dialogs
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        One-to-one relationship with the DialogDescription table (one dialog has one description).
        Use `back_populates="dialogs"` in DialogDescription models for two-way relationship.

        One-to-one relationship with the Chat table (one dialog belongs to one chat).
        Use `back_populates="dialogs"` in Chat models for two-way relationship.
    """
    __tablename__ = "dialogs"
    __table_args__ = {'schema': 'asclavia_schema'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    update_at = Column(DateTime(timezone=True), nullable=False)
    type = Column(ChatType, nullable=False)
    count_messages = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    description_id = Column(UUID(as_uuid=True),
                            ForeignKey(f"{'asclavia_schema'}.dialog_description.id", ondelete="CASCADE"),
                            nullable=False)
    chat_id = Column(UUID(as_uuid=True),
                     ForeignKey(f"{'asclavia_schema'}.chat.id", ondelete="CASCADE"),
                     nullable=False)

    description = relationship("DialogDescription", back_populates="dialogs")
    chat = relationship("Chat", back_populates="dialogs")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PJSIPEndpoint(Base):
    """
    The PJSIPEndpoint class represents a PJSIP endpoint model in the database.

    Attributes:
        id (Integer): Unique endpoint identifier (primary key).  Generated automatically.
        user_id (UUID): Foreign key referencing the user to which this endpoint belongs. Required field.
        extension (String): Endpoint extension number. Required field.
        auth_type (String): Authentication type for the endpoint. Required field.
        password (Text): Endpoint password. Required field.
        transport (String): Transport protocol used by the endpoint. Required field.
        context (String): Asterisk context for the endpoint. Required field.

    Methods:
        __repr__(): Returns a string representation of the PJSIPEndpoint object in JSON format.
        to_dict(): Returns a dictionary representation of the PJSIPEndpoint object,
                   where keys are the table column names and values are the corresponding attributes.

    Table:
        Table name: pjsip_endpoints
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        Many-to-one relationship with the User table (many endpoints may belong to one user).
        Uses `back_populates="pjsip_endpoints"` in User model for two-way relationship.
    """
    __tablename__ = 'pjsip_endpoints'
    __table_args__ = {'schema': 'asclavia_schema'}

    id = Column(Integer, primary_key=True, default=uuid.uuid4())
    user_id = Column(UUID, ForeignKey(f'{'asclavia_schema'}.users.id'), nullable=False)
    extension = Column(String(255), nullable=False)
    auth_type = Column(String(255), nullable=False)
    password = Column(Text, nullable=False)
    transport = Column(String(255), nullable=False)
    context = Column(String(255), nullable=False)

    user = relationship("User", back_populates="pjsip_endpoints")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Scenario(Base):
    """
    The Scenario class represents a scenario model in the database.

    Attributes:
        id (UUID): Unique scenario identifier (primary key). Generated automatically.
        scenario_name (String): Name of the scenario. Required field.
        updated_at (DateTime): Date and time of the last update to the scenario. Set automatically.
        created_at (DateTime): Date and time of scenario creation. Set automatically.
        name (String): A descriptive name for the scenario. Required field.
        dialog_aim (String): The intended goal or purpose of the dialog within the scenario. Required field.
        product (String): The product associated with the scenario. Required field.
        client_portrait (String): A description or profile of the target client for the scenario. Required field.
        success_conditions (String): The conditions that define a successful outcome for the scenario. Required field.
        about_company (Text): A detailed description of the company related to the scenario. Required field.
        user_id (UUID): Foreign key referencing the user who created the scenario.  Links to the users table. Required field.

    Methods:
        __repr__(): Returns a string representation of the Scenario object in JSON format.
        to_dict(): Returns a dictionary representation of the Scenario object, where keys are column names and values are corresponding data.

    Table:
        Table name: scenarios
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        Many-to-one relationship with the User table (many scenarios can be created by one user).
        Use `back_populates="scenarios"` in User model for two-way relationship.
        On delete cascade is configured, deleting a user will delete all associated scenarios.
    """
    __tablename__ = 'scenarios'
    __table_args__ = {'schema': 'asclavia_schema'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    scenario_name = Column(String(255), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
    name = Column(String(255), nullable=False)
    dialog_aim = Column(String(255), nullable=False)
    product = Column(String(255), nullable=False)
    client_portrait = Column(String(255), nullable=False)
    success_conditions = Column(String(255), nullable=False)
    about_company = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(f'{'asclavia_schema'}.users.id', ondelete='cascade'), nullable=False)

    user = relationship("User", back_populates="scenarios")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Task(Base):
    """
    The Task class represents a task model in the database.

    Attributes:
        id (UUID): Unique task identifier (primary key). Generated automatically.
        task_name (String): The name of the task. Required field.
        progress (Float): The progress of the task, represented as a float. Required field.
        status (String): The status of the task. Required field.
        created_at (Date): The date when the task was created. Required field.
        connection_type (String): The type of connection used for the task. Required field.
        scenario_name (String): The name of the scenario associated with the task. Required field.
        task_type (String): The type of task.  Restricted to a predefined set of values (Чат, Входная телефония, Исходящая телефония, Рассылка). Required field.
        chat_id (UUID): Foreign key referencing the chat associated with the task.  Allows null values if the task isn't related to a chat.
        telephone_income_id (UUID): Foreign key referencing incoming telephone data associated with the task. Allows null values if the task isn't related to incoming telephone calls.
        telephone_outcome_id (UUID): Foreign key referencing outgoing telephone data associated with the task. Allows null values if the task isn't related to outgoing telephone calls.
        crm_id (UUID): Foreign key referencing CRM data associated with the task. Allows null values if the task isn't related to a CRM system.
        session_time (TSRANGE): A time range representing the duration of the task's session. Required field.
        crm_integration (Boolean): Indicates whether CRM integration is enabled for the task. Default is False.
        send_email (Boolean): Indicates whether an email should be sent as part of the task. Default is False.
        comment (Text): A comment or description for the task.
        user_id (UUID): Foreign key referencing the user who created or is responsible for the task. Required field.

    Methods:
        __repr__(): Returns a string representation of the Task query in JSON format.
        to_dict(): Returns a dictionary, sequentially task data, where the keys are the names of the table columns.

    Table:
        Table name: tasks
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        One-to-many relationship with Chat, TelephoneIncome, TelephoneOutcome, CRM and User tables.
        backref="tasks" is used in related models for two-way relationship.
    """
    __tablename__ = "tasks"
    __table_args__ = {'schema': 'asclavia_schema'}

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4())
    task_name = Column(String(255), nullable=False)
    progress = Column(Float, nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(Date, nullable=False)
    connection_type = Column(String(255), nullable=False)
    scenario_name = Column(String(255), nullable=False)
    task_type = Column(String(20), nullable=False)
    __table_args__ = (CheckConstraint(task_type.in_(['Чат', 'Входная телефония', 'Исходящая телефония', 'Рассылка'])),
                      {'schema': 'asclavia_schema'})
    chat_id = Column(UUID(as_uuid=True), ForeignKey(f"{'asclavia_schema'}.chat.id", ondelete="CASCADE"))
    telephone_income_id = Column(UUID(as_uuid=True),
                                 ForeignKey(f"{'asclavia_schema'}.telephone_income.id", ondelete="CASCADE"))
    telephone_outcome_id = Column(UUID(as_uuid=True),
                                  ForeignKey(f"{'asclavia_schema'}.telephone_outcome.id", ondelete="CASCADE"))
    crm_id = Column(UUID(as_uuid=True), ForeignKey(f"{'asclavia_schema'}.crm.id", ondelete="CASCADE"))
    session_time = Column(TSRANGE, nullable=False)
    crm_integration = Column(Boolean, nullable=False, default=False)
    send_email = Column(Boolean, nullable=False, default=False)
    comment = Column(Text)
    user_id = Column(UUID(as_uuid=True), ForeignKey(f"{'asclavia_schema'}.users.id", ondelete="CASCADE"), nullable=False)

    chat = relationship("Chat", backref="tasks")
    telephone_income = relationship("TelephoneIncome", backref="tasks")
    telephone_outcome = relationship("TelephoneOutcome", backref="tasks")
    crm = relationship("CRM", backref="tasks")
    user = relationship("User", backref="tasks")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TelephoneIncome(Base):
    """
    The TelephoneIncome class represents a telephone income source in the database.

    Attributes:
        id (UUID): Unique identifier for the telephone income source (primary key). Generated automatically.
        scenario_name (String): Name of the scenario associated with this income source. Required field.
        robots_name (String): Name of the robot associated with this income source. Required field.
        chat_url (String): URL for the chat associated with this income source. Required field.
        login (String): Login credentials for the telephone system. Required field.
        hash_password (String): Hashed password for the telephone system. Required field. Stored as a hash for security.
        connection_name (String): Name of the connection to the telephone system. Required field.
        host (String): Host address of the telephone system. Required field.
        port (Integer): Port number for the telephone system. Default is 5060. Required field.
        additional_info (JSON): Additional information related to the telephone income source.  Default is an empty JSON object ({}).
        user_id (UUID): Foreign key referencing the user who owns this telephone income source. Required field.

    Methods:
        __repr__(): Returns a string representation of the TelephoneIncome object in JSON format.
        to_dict(): Returns a dictionary representation of the TelephoneIncome object, where the keys are the names of the table columns.

    Table:
        Table name: telephone_income
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        One-to-many relationship with the User table (one user may have multiple telephone income sources).
        Use `backref="telephone_income"` in User model for two-way relationship.

        One-to-many relationship with the Call table (one telephone income source may have multiple calls).
        Use `back_populates="telephone_income"` in Call model for two-way relationship.
    """
    __tablename__ = 'telephone_income'
    __table_args__ = {'schema': 'asclavia_schema'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    scenario_name = Column(String(255), nullable=False)
    robots_name = Column(String(255), nullable=False)
    chat_url = Column(String(255), nullable=False)
    login = Column(String(255), nullable=False)
    hash_password = Column(String(255), nullable=False)
    connection_name = Column(String(255), nullable=False)
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False, default=5060)
    additional_info = Column(JSON, nullable=False, default='{}')
    user_id = Column(UUID(as_uuid=True), ForeignKey(f'{'asclavia_schema'}.users.id'), nullable=False)

    user = relationship("User", backref="telephone_income")
    calls = relationship("Call", back_populates="telephone_income")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TelephoneOutcome(Base):
    """
    The TelephoneOutcome class represents a telephone outcome model in the database.
    It stores information about the outcome of a telephone interaction or scenario.

    Attributes:
        id (UUID): Unique identifier for the telephone outcome (primary key). Generated automatically.
        scenario_name (String): Name of the telephone scenario. Required field.
        robots_name (String): Name of the robot involved in the scenario. Required field.
        chat_url (String): URL of the chat associated with the scenario. Required field.
        login (String): Login username used for the connection. Required field.
        hash_password (String): Hashed password used for authentication. Required field.
        connection_name (String): Name of the connection used. Required field.
        host (String): Hostname or IP address of the server. Required field.
        port (Integer): Port number for the connection. Required field. Defaults to 5060.
        additional_info (JSON): Additional information about the outcome, stored as a JSON object. Defaults to an empty JSON object ('{}').
        user_id (UUID): Foreign key referencing the user who initiated the outcome. Required field.

    Methods:
        __repr__(): Returns a string representation of the TelephoneOutcome query in JSON format.
        to_dict(): Returns a dictionary, sequentially telephone outcome data, where the keys are the names of the table columns.

    Table:
        Table name: telephone_outcome
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        One-to-many relationship with the User table (one user can have multiple telephone outcomes).  Accessed via the `user` attribute.
        Use `backref="telephone_outcome"` in User model for two-way relationship.
        One-to-many relationship with the Call table (one telephone outcome can have multiple calls).  Accessed via the `calls` attribute.
        Use `back_populates="telephone_outcome"` in Call model for two-way relationship.
    """
    __tablename__ = 'telephone_outcome'
    __table_args__ = {'schema': 'asclavia_schema'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    scenario_name = Column(String(255), nullable=False)
    robots_name = Column(String(255), nullable=False)
    chat_url = Column(String(255), nullable=False)
    login = Column(String(255), nullable=False)
    hash_password = Column(String(255), nullable=False)
    connection_name = Column(String(255), nullable=False)
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False, default=5060)
    additional_info = Column(JSON, nullable=False, default='{}')
    user_id = Column(UUID(as_uuid=True), ForeignKey(f'{'asclavia_schema'}.users.id'), nullable=False)

    user = relationship("User", backref="telephone_outcome")
    calls = relationship("Call", back_populates="telephone_outcome")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Template(Base):
    """
    The Template class represents a template model in the database.

    Attributes:
        id (UUID): Unique template identifier (primary key). Generated automatically.
        template_name (String): Template's name. Required field.
        created_at (Date): Date of template creation. Required field.
        count_steps (Integer): Number of steps in the template. Required field.
        connection_type (String): Type of connection used in the template. Required field.
        scenario_name (String): Name of the scenario associated with the template. Required field.
        task_type (String): Type of task associated with the template. Required field. Must be one of:
                           'Чат', 'Входная телефония', 'Исходящая телефония', 'Рассылка'.
        chat_id (UUID): Foreign key referencing the Chat table.  Can be null if not applicable.
        telephone_income_id (UUID): Foreign key referencing the TelephoneIncome table. Can be null if not applicable.
        telephone_outcome_id (UUID): Foreign key referencing the TelephoneOutcome table. Can be null if not applicable.
        crm_id (UUID): Foreign key referencing the CRM table. Can be null if not applicable.
        session_time (TSRANGE): Time range for the template's session. Required field.
        crm_integration (Boolean): Indicates if CRM integration is enabled. Default is False.
        send_email (Boolean): Indicates if sending email is enabled. Default is False.
        comment (Text): Optional comment for the template.
        user_id (UUID): Foreign key referencing the Users table.  Represents the user who created the template. Required field.

    Methods:
        __repr__(): Returns a string representation of the Template query in JSON format.
        to_dict(): Returns a dictionary, sequentially template data, where the keys are the names of the table columns.

    Table:
        Table name: templates
        Schema: Defined by the settings in config.'asclavia_schema'

    Relationships:
        One-to-many relationship with the Chat, TelephoneIncome, TelephoneOutcome and CRM tables (one template may have one of each).
        One-to-many relationship with the Users table (one user may have multiple templates).
        Use `back_populates="templates"` in Chat, TelephoneIncome, TelephoneOutcome, CRM and Users models for two-way relationship.
"""
    __tablename__ = "templates"
    __table_args__ = {'schema': 'asclavia_schema'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    template_name = Column(String(255), nullable=False)
    created_at = Column(Date, nullable=False)
    count_steps = Column(Integer, nullable=False)
    connection_type = Column(String(255), nullable=False)
    scenario_name = Column(String(255), nullable=False)
    task_type = Column(String(20), nullable=False)
    __table_args__ = (CheckConstraint(task_type.in_(['Чат', 'Входная телефония', 'Исходящая телефония', 'Рассылка'])),
                      {'schema': 'asclavia_schema'})
    chat_id = Column(UUID(as_uuid=True), ForeignKey(f"{'asclavia_schema'}.chat.id", ondelete="CASCADE"))
    telephone_income_id = Column(UUID(as_uuid=True),
                                 ForeignKey(f"{'asclavia_schema'}.telephone_income.id", ondelete="CASCADE"))
    telephone_outcome_id = Column(UUID(as_uuid=True),
                                  ForeignKey(f"{'asclavia_schema'}.telephone_outcome.id", ondelete="CASCADE"))
    crm_id = Column(UUID(as_uuid=True), ForeignKey(f"{'asclavia_schema'}.crm.id", ondelete="CASCADE"))
    session_time = Column(TSRANGE, nullable=False)
    crm_integration = Column(Boolean, nullable=False, default=False)
    send_email = Column(Boolean, nullable=False, default=False)
    comment = Column(Text)
    user_id = Column(UUID(as_uuid=True), ForeignKey(f"{'asclavia_schema'}.users.id", ondelete="CASCADE"),
                     nullable=False)

    chat = relationship("Chat", backref="templates")
    telephone_income = relationship("TelephoneIncome", backref="templates")
    telephone_outcome = relationship("TelephoneOutcome", backref="templates")
    crm = relationship("CRM", backref="templates")
    user = relationship("User", backref="templates")

    def __repr__(self):
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=4, default=str)})"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}