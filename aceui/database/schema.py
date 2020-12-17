# vim: sw=4:ts=4:et:cc=120

import json

from typing import Set

import ace.constants

from ace.analysis import Indicator, IndicatorList, RootAnalysis
from ace.database import Base, retry, use_db
from ace.json import JSONEncoder

from sqlalchemy import (
    BigInteger,
    BOOLEAN,
    Binary,
    Column,
    DATE,
    DATETIME,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
    TIMESTAMP,
    Text,
    UniqueConstraint,
    func,
    text,
)

from sqlalchemy.orm import relationship, reconstructor, backref, validates, aliased
from sqlalchemy.dialects.mysql import BOOLEAN, VARBINARY, BLOB

class Config(Base):
    """Holds generic key=value configuration settings."""

    __tablename__ = 'config'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    key = Column(
        String,
        primary_key=True,
        nullable=False)

    value = Column(
        Text, 
        nullable=False)

class User(Base):

    __tablename__ = 'users'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True)

    username = Column(
        String(64), 
        unique=True, 
        index=True)

    password_hash = Column(String(128))

    email = Column(
        String(64), 
        unique=True, 
        index=True)

    omniscience = Column(
        BOOLEAN, 
        nullable=False, 
        default=False)

    timezone = Column(
        String(512),
        comment='The timezone this user is in. Dates and times will appear in this timezone in the GUI.')

    display_name = Column(
        String(1024),
        comment='The display name of the user. This may be different than the username. This is used in the GUI.')

    queue = Column(
        String(64),
        nullable=False,
        default='default')

    def __str__(self):
        return self.username

    @property
    def gui_display(self):
        """Returns the textual representation of this user in the GUI.
           If the user has a display_name value set then that is returned.
           Otherwise, the username is returned."""

        if self.display_name is not None:
            return self.display_name

        return self.username

Index('ix_users_username_email', User.username, User.email, unique=True)

Owner = aliased(User)
DispositionBy = aliased(User)
RemediatedBy = aliased(User)

class Campaign(Base):

    __tablename__ = 'campaign'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(128), nullable=False, index=True)

class CloudphishAnalysisResults(Base):

    __tablename__ = 'cloudphish_analysis_results'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    sha256_url = Column(
        VARBINARY(32),
        primary_key=True,
        nullable=False,
        comment='The binary SHA2 hash of the URL.')

    http_result_code = Column(
        Integer,
        nullable=True,
        comment='The HTTP result code give by the server when it was fetched (200, 404, 500, etc…)')

    http_message = Column(
        String(256),
        nullable=True,
        comment='The message text that came along with the http_result_code.')

    sha256_content = Column(
        VARBINARY(32),
        nullable=True,
        index=True,
        comment='The binary SHA2 hash of the content that was downloaded for the URL.')

    result = Column(
        Enum('UNKNOWN','ERROR','CLEAR','ALERT','PASS'),
        nullable=False,
        default='UNKNOWN',
        comment='The analysis result of the URL. This is updated by the cloudphish_request_analyzer module.')

    insert_date = Column(
        TIMESTAMP,
        nullable=False,
        index=True,
        server_default=text('CURRENT_TIMESTAMP'),
        comment='When this entry was created.')

    uuid = Column(
        String(36),
        nullable=False,
        comment='The UUID of the analysis. This would also become the UUID of the alert if it ends up becoming one.')

    status = Column(
        Enum('NEW','ANALYZING','ANALYZED'),
        nullable=False,
        default='NEW')

class CloudphishContentMetadata(Base):

    __tablename__ = 'cloudphish_content_metadata'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    sha256_content = Column(
        VARBINARY(32),
        ForeignKey('cloudphish_analysis_results.sha256_content', 
            ondelete='CASCADE',
            onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
        comment='The binary SHA2 hash of the content that was downloaded from the URL.')

    node = Column(
        String(1024),
        nullable=True,
        comment='The name of the node which stores this binary data. This would match the name columns of the nodes table, however, there is not a database relationship because the nodes can change.')

    name = Column(
        VARBINARY(4096),
        nullable=False,
        comment='The name of the file as it was seen either by content disposition of extrapolated from the URL.\nThis is stored in python’s “unicode_internal” format.')

class CloudphishUrlLookup(Base):

    __tablename__ = 'cloudphish_url_lookup'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    sha256_url = Column(
        VARBINARY(32),
        ForeignKey('cloudphish_analysis_results.sha256_content', 
            ondelete='CASCADE',
            onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
        comment='The SHA256 value of the URL.')

    last_lookup = Column(
        TIMESTAMP,
        nullable=False,
        index=True,
        server_default=text('CURRENT_TIMESTAMP'),
        comment='The last time this URL was looked up. This is updated every time a query is made to cloudphish for this url. URLs that are not looked up after a period of time are cleared out.')

    url = Column( 
        Text,
        nullable=False,
        comment='The value of the URL.')

class Event(Base):

    __tablename__ = 'events'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = Column(
        Integer, 
        primary_key=True,
        nullable=False,
        autoincrement=True)

    creation_date = Column(
        DATE, 
        nullable=False)

    name = Column(
        String(128), 
        nullable=False)

    type = Column(
        Enum(
            'phish',
            'recon',
            'host compromise',
            'credential compromise',
            'web browsing'), 
        nullable=False)

    vector = Column(
        Enum(
            'corporate email',
            'webmail',
            'usb',
            'website',
            'unknown'), 
        nullable=False)

    risk_level = Column(
        Enum(
            '1',
            '2',
            '3'), 
        nullable=False)

    prevention_tool = Column(
        Enum(
            'response team',
            'ips',
            'fw',
            'proxy',
            'antivirus',
            'email filter',
            'application whitelisting',
            'user'), 
        nullable=False)

    remediation = Column(
        Enum(
            'not remediated',
            'cleaned with antivirus',
            'cleaned manually',
            'reimaged',
            'credentials reset',
            'removed from mailbox',
            'network block',
            'NA'), 
        nullable=False)

    status = Column(
        Enum('OPEN','CLOSED','IGNORE'), 
        nullable=False)

    comment = Column(Text)

    campaign_id = Column(
        Integer, 
        ForeignKey('campaign.id', ondelete='CASCADE', onupdate='CASCADE'), 
        nullable=False)

    event_time = Column(
        DATETIME, 
        nullable=True)

    alert_time = Column(
        DATETIME, 
        nullable=True)

    ownership_time = Column(
        DATETIME, 
        nullable=True)

    disposition_time = Column(
        DATETIME, 
        nullable=True)

    contain_time = Column(
        DATETIME, 
        nullable=True)

    remediation_time = Column(
        DATETIME, 
        nullable=True)


    malware = relationship("aceui.database.schema.MalwareMapping", passive_deletes=True, passive_updates=True)
    alert_mappings = relationship("aceui.database.schema.EventMapping", passive_deletes=True, passive_updates=True)

    @property
    def json(self):
        return {
            'id': self.id,
            'alerts': self.alerts,
            'campaign': self.campaign.name if self.campaign else None,
            'comment': self.comment,
            'creation_date': str(self.creation_date),
            'event_time': str(self.event_time),
            'alert_time': str(self.alert_time),
            'ownership_time': str(self.ownership_time),
            'disposition_time': str(self.ownership_time),
            'contain_time': str(self.contain_time),
            'remediation_time': str(self.remediation_time),
            'disposition': self.disposition,
            'malware': [{mal.name: [t.type for t in mal.threats]} for mal in self.malware],
            'name': self.name,
            'prevention_tool': self.prevention_tool,
            'remediation': self.remediation,
            'risk_level': self.risk_level,
            'status': self.status,
            'tags': self.sorted_tags,
            'type': self.type,
            'vector': self.vector,
            'wiki': self.wiki
        }

    @property
    def alerts(self):
        uuids = []
        for alert_mapping in self.alert_mappings:
            uuids.append(alert_mapping.alert.uuid)
        return uuids

    @property
    def alert_objects(self) -> list['Alert']:
        alerts = [m.alert for m in self.alert_mappings]
        for alert in alerts:
            alert.load()
        return alerts

    @property
    def malware_names(self):
        names = []
        for mal in self.malware:
            names.append(mal.name)
        return names

    @property
    def commentf(self):
        if self.comment is None:
            return ""
        return self.comment

    @property
    def threats(self):
        threats = {}
        for mal in self.malware:
            for threat in mal.threats:
                threats[threat.type] = True
        return threats.keys()

    @property
    def disposition(self):
        if not self.alert_mappings:
            disposition = ace.constants.DISPOSITION_DELIVERY
        else:
            disposition = None

        for alert_mapping in self.alert_mappings:
            if alert_mapping.alert.disposition is None:
                logging.warning(f"alert {alert_mapping.alert} added to event without disposition {alert_mapping.event_id}")
                continue

            if disposition is None or ace.constants.DISPOSITION_RANK[alert_mapping.alert.disposition] > ace.constants.DISPOSITION_RANK[disposition]:
                disposition = alert_mapping.alert.disposition
        return disposition

    @property
    def disposition_rank(self):
        return ace.constants.DISPOSITION_RANK[self.disposition]

    @property
    def sorted_tags(self):
        tags = {}
        for alert_mapping in self.alert_mappings:
            for tag_mapping in alert_mapping.alert.tag_mappings:
                tags[tag_mapping.tag.name] = tag_mapping.tag
        return sorted([x for x in tags.values()], key=lambda x: (-x.score, x.name.lower()))

    @property
    def wiki(self):
        if ace.CONFIG['mediawiki'].getboolean('enabled'):
            domain = ace.CONFIG['mediawiki']['domain']
            date = self.creation_date.strftime("%Y%m%d").replace(' ', '+')
            name = self.name.replace(' ', '+')
            return "{}display/integral/{}+{}".format(domain, date, name)
        else:
            return None

    @property
    def alert_with_email_and_screenshot(self) -> 'aceui.database.schema.Alert':
        return next((a for a in self.alert_objects if a.has_email_analysis and a.has_renderer_screenshot), None)

    @property
    def all_emails(self) -> Set['ace.modules.email.EmailAnalysis']:
        emails = set()

        for alert in self.alert_objects:
            observables = alert.find_observables(lambda o: o.get_analysis(ace.modules.email.EmailAnalysis))
            email_analyses = {o.get_analysis(ace.modules.email.EmailAnalysis) for o in observables}

            # Inject the alert's UUID into the EmailAnalysis so that we maintain a link of alert->email
            for email_analysis in email_analyses:
                email_analysis.alert_uuid = alert.uuid

            emails |= email_analyses

        return emails

    @property
    def all_iocs(self) -> list[Indicator]:
        iocs = IndicatorList()

        for alert in self.alert_objects:
            for analysis in alert.all_analysis:
                for ioc in analysis.iocs:
                    iocs.append(ioc)

        for alert in self.alert_objects:
            for observable_ioc in alert.observable_iocs:
                if observable_ioc not in iocs:
                    iocs.append(observable_ioc)

        if any(a.has_email_analysis for a in self.alert_objects):
            for ioc in iocs:
                ioc.tags += ['phish']

        return sorted(iocs, key=lambda x: (x.type, x.value))

    @property
    def all_url_domain_counts(self) -> dict[str, int]:
        url_domain_counts = {}

        for alert in self.alert_objects:
            domain_counts = find_all_url_domains(alert)
            for d in domain_counts:
                if d not in url_domain_counts:
                    url_domain_counts[d] = domain_counts[d]
                else:
                    url_domain_counts[d] += domain_counts[d]

        return url_domain_counts

    @property
    def all_urls(self) -> Set[str]:
        urls = set()

        for alert in self.alert_objects:
            observables = alert.find_observables(lambda o: o.type == F_URL)
            urls |= {o.value for o in observables}

        return urls

    @property
    def all_user_analysis(self) -> Set['ace.modules.user.UserAnalysis']:
        user_analysis = set()

        for alert in self.alert_objects:
            observables = alert.find_observables(lambda o: o.get_analysis(ace.modules.user.UserAnalysis))
            user_analysis |= {o.get_analysis(ace.modules.user.UserAnalysis) for o in observables}

        return user_analysis

    @property
    def showable_tags(self) -> dict[str, list]:
        special_tag_names = [tag for tag in ace.CONFIG['tags'] if ace.CONFIG['tags'][tag] in ['special', 'hidden']]

        results = {}
        for alert in self.alert_objects:
            results[alert.uuid] = []
            for tag in alert.sorted_tags:
                if tag.name not in special_tag_names:
                    results[alert.uuid].append(tag)

        return results

Index('ix_events_creation_date_name', Event.creation_date, Event.name, unique=True)

class EventMapping(Base):

    __tablename__ = 'event_mapping'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    event_id = Column(
        Integer, 
        ForeignKey('events.id', ondelete='CASCADE', onupdate='CASCADE'), 
        primary_key=True)

    alert_id = Column(
        Integer, 
        ForeignKey('alerts.id', ondelete='CASCADE', onupdate='CASCADE'), 
        primary_key=True,
        index=True)

    alert = relationship('aceui.database.schema.Alert', backref='event_mapping')
    event = relationship('aceui.database.schema.Event', backref='event_mapping')

class Malware(Base):

    __tablename__ = 'malware'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = Column(
        Integer, 
        primary_key=True)

    name = Column(
        String(128), 
        unique=True, 
        index=True)

    threats = relationship("aceui.database.schema.MalwareThreatMapping", passive_deletes=True, passive_updates=True)

class MalwareMapping(Base):

    __tablename__ = 'malware_mapping'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    event_id = Column(
        Integer, 
        ForeignKey('events.id', ondelete='CASCADE', onupdate='CASCADE'), 
        primary_key=True)

    malware_id = Column(
        Integer, 
        ForeignKey('malware.id', ondelete='CASCADE', onupdate='CASCADE'), 
        primary_key=True,
        index=True)

    malware = relationship("aceui.database.schema.Malware")

    @property
    def threats(self):
        return self.malware.threats

    @property
    def name(self):
        return self.malware.name

class MalwareThreatMapping(Base):

    __tablename__ = 'malware_threat_mapping'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    malware_id = Column(
        Integer,
        ForeignKey('malware.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True)

    type = Column(
        Enum(
            'UNKNOWN',
            'KEYLOGGER',
            'INFOSTEALER',
            'DOWNLOADER',
            'BOTNET',
            'RAT',
            'RANSOMWARE',
            'ROOTKIT',
            'FRAUD',
            'CUSTOMER_THREAT'),
        nullable=False,
        primary_key=True)

class Alert(Base):

    @reconstructor
    def init_on_load(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #
    # column definitions
    #

    __tablename__ = 'alerts'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = Column(
        Integer, 
        primary_key=True)

    root_json = Column(
        Text,
        nullable=False)

    @property
    def root(self) -> RootAnalysis:
        return RootAnalysis.from_dict(self.root_json)

    @staticmethod
    def from_root(root: RootAnalysis) -> 'Alert':
        alert = Alert(
            uuid=root.uuid,
            root_json=json.dumps(root.to_dict(), cls=JSONEncoder, sort_keys=True),
            tool=root.tool,
            tool_instance=root.tool_instance,
            alert_type=root.alert_type,
            description=root.description,
            queue=root.queue)

        # TODO all the rest of the stuff!
        return alert

    uuid = Column(
        String(36), 
        unique=True, 
        nullable=False)

    insert_date = Column(
        TIMESTAMP, 
        nullable=False, 
        index=True,
        server_default=text('CURRENT_TIMESTAMP'))

    tool = Column(
        String(256),
        nullable=False)

    tool_instance = Column(
        String(1024),
        nullable=False)

    alert_type = Column(
        String(64),
        nullable=False,
        index=True)

    description = Column(
        String(1024),
        nullable=False)

    priority = Column(
        Integer,
        nullable=False,
        default=0)

    disposition = Column(
        Enum(
            ace.constants.DISPOSITION_FALSE_POSITIVE,
            ace.constants.DISPOSITION_IGNORE,
            ace.constants.DISPOSITION_UNKNOWN,
            ace.constants.DISPOSITION_REVIEWED,
            ace.constants.DISPOSITION_GRAYWARE,
            ace.constants.DISPOSITION_POLICY_VIOLATION,
            ace.constants.DISPOSITION_RECONNAISSANCE,
            ace.constants.DISPOSITION_WEAPONIZATION,
            ace.constants.DISPOSITION_DELIVERY,
            ace.constants.DISPOSITION_EXPLOITATION,
            ace.constants.DISPOSITION_INSTALLATION,
            ace.constants.DISPOSITION_COMMAND_AND_CONTROL,
            ace.constants.DISPOSITION_EXFIL,
            ace.constants.DISPOSITION_DAMAGE,
            ace.constants.DISPOSITION_INSIDER_DATA_CONTROL,
            ace.constants.DISPOSITION_INSIDER_DATA_EXFIL),
        nullable=True,
        index=True)

    disposition_user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        index=True)

    disposition_time = Column(
        TIMESTAMP, 
        nullable=True)

    owner_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        index=True)

    owner_time = Column(
        TIMESTAMP,
        nullable=True)

    archived = Column(
        BOOLEAN, 
        nullable=False,
        default=False)

    removal_user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        index=True)

    removal_time = Column(
        TIMESTAMP,
        nullable=True)

    detection_count = Column(
        Integer,
        default=0)

    event_time = Column(
        TIMESTAMP,
        nullable=True)

    queue = Column(
        String(64),
        nullable=False,
        default=ace.constants.QUEUE_DEFAULT,
        index=True)

    #
    # relationships
    #

    disposition_user = relationship('aceui.database.schema.User', foreign_keys=[disposition_user_id])
    owner = relationship('aceui.database.schema.User', foreign_keys=[owner_id])
    remover = relationship('aceui.database.schema.User', foreign_keys=[removal_user_id])
    #observable_mapping = relationship('aceui.database.schema.ObservableMapping')
    tag_mappings = relationship('aceui.database.schema.TagMapping', passive_deletes=True, passive_updates=True)
    #delayed_analysis = relationship('aceui.database.schema.DelayedAnalysis')

    def get_observables(self):
        query = ace.db.query(Observable)
        query = query.join(ObservableMapping, Observable.id == ObservableMapping.observable_id)
        query = query.join(Alert, ObservableMapping.alert_id == Alert.id)
        query = query.filter(Alert.uuid == self.uuid)
        query = query.group_by(Observable.id)
        return query.all()

    def get_remediation_targets(self):
        # XXX hack to get around circular import - probably need to merge some modules into one
        from ace.observables import create_observable

        # get observables for this alert
        observables = self.get_observables()

        # get remediation targets for each observable
        targets = {}
        for o in observables:
            observable = create_observable(o.type, o.display_value)
            for target in observable.remediation_targets:
                targets[target.id] = target

        # return sorted list of targets
        targets = list(targets.values())
        targets.sort(key=lambda x: f"{x.type}|{x.value}")
        return targets

    def get_remediation_status(self):
        targets = self.get_remediation_targets()
        remediations = []
        for target in targets:
            if len(target.history) > 0:
                remediations.append(target.history[0])

        if len(remediations) == 0:
            return 'new'

        s = 'success'
        for r in remediations:
            if not r.successful:
                return 'failed'
            if r.status != 'COMPLETED':
                s = 'processing'
        return s

    @property
    def remediation_status(self):
        return self._remediation_status if hasattr(self, '_remediation_status') else self.get_remediation_status()

    @property
    def remediation_targets(self):
        return self._remediation_targets if hasattr(self, '_remediation_targets') else self.get_remediation_targets()

    @property
    def observable_iocs(self) -> IndicatorList:
        indicators = IndicatorList()

        for ob in self.find_observables(lambda o: o.type == F_EMAIL_ADDRESS):
            indicators.append(Indicator(I_EMAIL_ADDRESS, ob.value))

        for ob in self.find_observables(lambda o: o.type == F_URL):
            indicators.add_url_iocs(ob.value)

        return indicators

    @property
    def all_email_analysis(self) -> list['ace.modules.email.EmailAnalysis']:
        observables = self.find_observables(lambda o: o.get_analysis(ace.modules.email.EmailAnalysis))
        return [o.get_analysis(ace.modules.email.EmailAnalysis) for o in observables]

    @property
    def has_email_analysis(self) -> bool:
        return bool(self.find_observable(lambda o: o.get_analysis(ace.modules.email.EmailAnalysis)))

    @property
    def has_renderer_screenshot(self) -> bool:
        return any(
            o.type == F_FILE and o.is_image and o.value.startswith('renderer_') and o.value.endswith('.png')
            for o in self.all_observables
        )

    @property
    def screenshots(self) -> list[dict]:
        return [
            {'alert_id': self.uuid, 'observable_id': o.id, 'scaled_width': o.scaled_width, 'scaled_height': o.scaled_height}
            for o in self.all_observables
            if (
                    o.type == F_FILE
                    and o.is_image
                    and o.value.startswith('renderer_')
                    and o.value.endswith('.png')
            )
        ]

    @property
    def icon(self):
        """Returns appropriate icon name by attempting to match on self.description or self.tool."""
        description_tokens = {token.lower() for token in re.split('[ _]', self.description)}
        tool_tokens = {token.lower() for token in self.tool.split(' ')}
        type_tokens = {token.lower() for token in self.alert_type.split(' ')}

        available_favicons = set(ace.CONFIG['gui']['alert_favicons'].split(','))

        result = available_favicons.intersection(description_tokens)
        if not result:
            result = available_favicons.intersection(tool_tokens)
            if not result:
                result = available_favicons.intersection(type_tokens)

        if not result:
            return 'default'
        else:
            return result.pop()

    @validates('description')
    def validate_description(self, key, value):
        max_length = getattr(self.__class__, key).prop.columns[0].type.length
        if value and len(value) > max_length:
            return value[:max_length]
        return value

    def archive(self, *args, **kwargs):
        if self.archived:
            logging.warning(f"called archive() on {self} but already archived")
            return None

        result = super().archive(*args, **kwargs)
        self.archived = True
        return result

    @property
    def sorted_tags(self):
        tags = {}
        for tag_mapping in self.tag_mappings:
            tags[tag_mapping.tag.name] = tag_mapping.tag
        return sorted([x for x in tags.values()], key=lambda x: (-x.score, x.name.lower()))

    @retry
    def sync(self):
        """Saves the Alert to disk and database."""
        assert self.storage_dir is not None # requires a valid storage_dir at this point
        assert isinstance(self.storage_dir, str)

        # compute number of detection points
        self.detection_count = len(self.all_detection_points)

        # save the alert to the database
        session = Session.object_session(self)
        if session is None:
            session = ace.db()
        
        session.add(self)
        session.commit()
        self.build_index()

        self.save() # save this alert now that it has the id

        return True

    def reset(self):
        super().reset()

        if self.id:
            # rebuild the index after we reset the Alert
            self.rebuild_index()

    def build_index(self):
        """Rebuilds the data for this Alert in the observables, tags, observable_mapping and tag_mapping tables."""
        self.rebuild_index()

    def rebuild_index(self):
        """Rebuilds the data for this Alert in the observables, tags, observable_mapping and tag_mapping tables."""
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            with get_db_connection() as db:
                c = db.cursor()
                execute_with_retry(db, c, self._rebuild_index)

    def _rebuild_index(self, db, c):
        logging.info(f"rebuilding indexes for {self}")
        c.execute("""DELETE FROM observable_mapping WHERE alert_id = %s""", ( self.id, ))
        c.execute("""DELETE FROM tag_mapping WHERE alert_id = %s""", ( self.id, ))
        c.execute("""DELETE FROM observable_tag_index WHERE alert_id = %s""", ( self.id, ))

        tag_names = tuple([ tag.name for tag in self.all_tags ])
        if tag_names:
            sql = "INSERT IGNORE INTO tags ( name ) VALUES {}".format(','.join(['(%s)' for name in tag_names]))
            #logging.debug(f"MARKER: sql = {sql}")
            c.execute(sql, tag_names)

        all_observables = self.all_observables

        observables = []
        observable_hash_mapping = {} # key = md5, value = observable
        for observable in all_observables:
            observables.append(observable.type)
            observables.append(observable.value)
            observables.append(observable.md5_hex)
            observable_hash_mapping[observable.md5_hex] = observable

        observables = tuple(observables)

        if all_observables:
            sql = "INSERT IGNORE INTO observables ( type, value, md5 ) VALUES {}".format(','.join('(%s, %s, UNHEX(%s))' for o in all_observables))
            #logging.debug(f"MARKER: sql = {sql}")
            c.execute(sql, observables)

        tag_mapping = {} # key = tag_name, value = tag_id
        if tag_names:
            sql = "SELECT id, name FROM tags WHERE name IN ( {} )".format(','.join(['%s' for name in tag_names]))
            #logging.debug(f"MARKER: sql = {sql}")
            c.execute(sql, tag_names)

            for row in c:
                tag_id, tag_name = row
                tag_mapping[tag_name] = tag_id

            sql = "INSERT INTO tag_mapping ( alert_id, tag_id ) VALUES {}".format(','.join(['(%s, %s)' for name in tag_mapping.values()]))
            #logging.debug(f"MARKER: sql = {sql}")
            parameters = []
            for tag_id in tag_mapping.values():
                parameters.append(self.id)
                parameters.append(tag_id)

            c.execute(sql, tuple(parameters))

        observable_mapping = {} # key = observable_id, value = observable
        if all_observables:
            sql = "SELECT id, HEX(md5) FROM observables WHERE md5 IN ( {} )".format(','.join(['UNHEX(%s)' for o in all_observables]))
            #logging.debug(f"MARKER: sql = {sql}")
            c.execute(sql, tuple([o.md5_hex for o in all_observables]))

            for row in c:
                observable_id, md5_hex = row
                observable_mapping[md5_hex.lower()] = observable_id

            sql = "INSERT INTO observable_mapping ( alert_id, observable_id ) VALUES {}".format(','.join(['(%s, %s)' for o in observable_mapping.keys()]))
            #logging.debug(f"MARKER: sql = {sql}")
            parameters = []
            for observable_id in observable_mapping.values():
                parameters.append(self.id)
                parameters.append(observable_id)

            c.execute(sql, tuple(parameters))

        sql = "INSERT IGNORE INTO observable_tag_index ( alert_id, observable_id, tag_id ) VALUES "
        parameters = []
        sql_clause = []

        for observable in all_observables:
            for tag in observable.tags:
                try:
                    tag_id = tag_mapping[tag.name]
                except KeyError:
                    logging.debug(f"missing tag mapping for tag {tag.name} in observable {observable} alert {self.uuid}")
                    continue

                observable_id = observable_mapping[observable.md5_hex.lower()]

                parameters.append(self.id)
                parameters.append(observable_id)
                parameters.append(tag_id)
                sql_clause.append('(%s, %s, %s)')

        if sql_clause:
            sql += ','.join(sql_clause)
            #logging.debug(f"MARKER: sql = {sql}")
            c.execute(sql, tuple(parameters))

        db.commit()

@retry
def sync_observable(observable):
    """Syncs the given observable to the database by inserting a row in the observables table if it does not currently exist.
       Returns the existing or newly created aceui.database.schema.Observable entry for the corresponding row."""
    existing_observable = ace.db.query(aceui.database.schema.Observable).filter(aceui.database.schema.Observable.type == observable.type, 
                                                                       aceui.database.schema.Observable.md5 == func.UNHEX(observable.md5_hex)).first()
    if existing_observable is None:
        # XXX assuming all observables are encodable in utf-8 is probably wrong
        # XXX we could have some kind of binary data, or an intentionally corrupt value
        # XXX in which case we'd lose the actual value of the data here
        existing_observable = Observable(type=observable.type, 
                                         value=observable.value.encode('utf8', errors='ignore'), 
                                         md5=func.UNHEX(observable.md5_hex))
        ace.db.add(existing_observable)
        ace.db.flush()

    return existing_observable

def set_dispositions(alert_uuids, disposition, user_id, user_comment=None):
    """Utility function to the set disposition of many Alerts at once.
       :param alert_uuids: A list of UUIDs of Alert objects to set.
       :param disposition: The disposition to set the Alerts.
       :param user_id: The id of the User that is setting the disposition.
       :param user_comment: Optional comment the User is providing as part of the disposition."""

    with get_db_connection() as db:
        c = db.cursor()
        # update dispositions
        uuid_placeholders = ','.join(['%s' for _ in alert_uuids])
        sql = f"""UPDATE alerts SET 
                      disposition = %s, disposition_user_id = %s, disposition_time = NOW(),
                      owner_id = %s, owner_time = NOW()
                  WHERE 
                      (disposition IS NULL OR disposition != %s) AND uuid IN ( {uuid_placeholders} )"""
        parameters = [disposition, user_id, user_id, disposition]
        parameters.extend(alert_uuids)
        c.execute(sql, parameters)
        
        # add the comment if it exists
        if user_comment:
            for uuid in alert_uuids:
                c.execute("""
                          INSERT INTO comments ( user_id, uuid, comment ) 
                          VALUES ( %s, %s, %s )""", ( user_id, uuid, user_comment))

class Similarity:
    def __init__(self, uuid, disposition, percent):
        self.uuid = uuid
        self.disposition = disposition
        self.percent = round(float(percent))

class UserAlertMetrics(Base):
    
    __tablename__ = 'user_alert_metrics'

    alert_id = Column(
        Integer,
        ForeignKey('alerts.id'),
        primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        primary_key=True)

    start_time = Column(
        TIMESTAMP, 
        nullable=False, 
        server_default=text('CURRENT_TIMESTAMP'))

    disposition_time = Column(
        TIMESTAMP, 
        nullable=True)

    alert = relationship('aceui.database.schema.Alert', backref='user_alert_metrics')
    user = relationship('User', backref='user_alert_metrics')

class Comment(Base):

    __tablename__ = 'comments'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    comment_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True)

    insert_date = Column(
        TIMESTAMP, 
        nullable=False, 
        index=True,
        server_default=text('CURRENT_TIMESTAMP'))

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
        index=True)

    uuid = Column(
        String(36), 
        ForeignKey('alerts.uuid', ondelete='CASCADE'),
        nullable=False,
        index=True)

    comment = Column(
        Text,
        nullable=False)

    # many to one
    user = relationship('User', backref='comments')
    # TODO add other relationships?

class Observable(Base):

    __tablename__ = 'observables'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True)

    type = Column(
        String(64),
        nullable=False)

    value = Column(
        LargeBinary,
        nullable=False)

    md5 = Column(
        VARBINARY(16),
        nullable=False,
        index=True)

    @property
    def display_value(self):
        return self.value.decode('utf8', errors='ignore')

    tags = relationship('aceui.database.schema.ObservableTagMapping', passive_deletes=True, passive_updates=True)

Index('ix_observable_type_md5', Observable.type, Observable.md5, unique=True)

class ObservableMapping(Base):

    __tablename__ = 'observable_mapping'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    observable_id = Column(
        Integer,
        ForeignKey('observables.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True)

    alert_id = Column(
        Integer,
        ForeignKey('alerts.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        index=True)

    alert = relationship('aceui.database.schema.Alert', backref='observable_mappings')
    observable = relationship('aceui.database.schema.Observable', backref='observable_mappings')

# this is used to automatically map tags to observables
# same as the etc/site_tags.csv really, just in the database
class ObservableTagMapping(Base):
    
    __tablename__ = 'observable_tag_mapping'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    observable_id = Column(
        Integer,
        ForeignKey('observables.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        index=True)

    tag_id = Column(
        Integer,
        ForeignKey('tags.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True)

    observable = relationship('aceui.database.schema.Observable', backref='observable_tag_mapping')
    tag = relationship('aceui.database.schema.Tag', backref='observable_tag_mapping')

def add_observable_tag_mapping(o_type, o_value, o_md5, tag):
    """Adds the given observable tag mapping specified by type, and md5 (hex string) and the tag you want to map.
       If the observable does not exist and o_value is provided then the observable is added to the database.
       Returns True if the mapping was successful, False otherwise."""

    try:
        tag = ace.db.query(aceui.database.schema.Tag).filter(aceui.database.schema.Tag.name == tag).one()
    except NoResultFound as e:
        ace.db.execute(aceui.database.schema.Tag.__table__.insert().values(name=tag))
        ace.db.commit()
        tag = ace.db.query(aceui.database.schema.Tag).filter(aceui.database.schema.Tag.name == tag).one()

    observable = None

    if o_md5 is not None:
        try:
            observable = ace.db.query(aceui.database.schema.Observable).filter(aceui.database.schema.Observable.type==o_type, 
                                                                      aceui.database.schema.Observable.md5==func.UNHEX(o_md5)).one()
        except NoResultFound as e:
            if o_value is None:
                logging.warning(f"observable type {o_type} md5 {o_md5} cannot be found for mapping")
                return False

    if observable is None:
        from ace.observables import create_observable
        observable = sync_observable(create_observable(o_type, o_value))
        ace.db.commit()

    try:
        mapping = ace.db.query(ObservableTagMapping).filter(ObservableTagMapping.observable_id == observable.id,
                                                            ObservableTagMapping.tag_id == tag.id).one()
        ace.db.commit()
        return True

    except NoResultFound as e:
        ace.db.execute(ObservableTagMapping.__table__.insert().values(observable_id=observable.id, tag_id=tag.id))
        ace.db.commit()
        return True

def remove_observable_tag_mapping(o_type, o_value, o_md5, tag):
    """Removes the given observable tag mapping specified by type, and md5 (hex string) and the tag you want to remove.
       Returns True if the removal was successful, False otherwise."""

    tag = ace.db.query(aceui.database.schema.Tag).filter(aceui.database.schema.Tag.name == tag).first()
    if tag is None:
        return False

    observable = None
    if o_md5 is not None:
        observable = ace.db.query(aceui.database.schema.Observable).filter(aceui.database.schema.Observable.type == o_type,
                                                                  aceui.database.schema.Observable.md5 == func.UNHEX(o_md5)).first()
    
    if observable is None:
        if o_value is None:
            return False

        from ace.observables import create_observable
        o = create_observable(o_type, o_value)
        observable = ace.db.query(aceui.database.schema.Observable).filter(aceui.database.schema.Observable.type == o.type,
                                                                  aceui.database.schema.Observable.md5 == func.UNHEX(o.md5_hex)).first()

    if observable is None:
        return False

    ace.db.execute(ObservableTagMapping.__table__.delete().where(and_(ObservableTagMapping.observable_id == observable.id,
                                                                 ObservableTagMapping.tag_id == tag.id)))
    ace.db.commit()
    return True

class PersistenceSource(Base):

    __tablename__ = 'persistence_source'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }
    
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True)

    name = Column(
        String(256),
        nullable=False,
        index=True,
        comment='The name of the persistence source. For example, the name of the ace collector.')

class Persistence(Base):

    __tablename__ = 'persistence'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True)

    source_id = Column(
        Integer,
        ForeignKey('persistence_source.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        comment='The source that generated this persistence data.'
    )

    permanent = Column(
        BOOLEAN,
        nullable=False,
        default=False,
        comment='Set to 1 if this value should never be deleted, 0 otherwise.')

    uuid = Column(
        String(512),
        nullable=False,
        comment='A unique identifier (key) for this piece of persistence data specific to this source.')

    value = Column(
        LargeBinary,
        nullable=True,
        comment='The value of this piece of persistence data. This is pickled python data.')

    created_at = Column(
        TIMESTAMP, 
        nullable=False, 
        index=True,
        server_default=text('CURRENT_TIMESTAMP'),
        comment='The time this information was created.')

    last_update = Column(
        TIMESTAMP, 
        nullable=False, 
        index=True,
        server_default=text('CURRENT_TIMESTAMP'),
        comment='The last time this information was updated.')

Index('ix_persistence_source_id_uuid', Persistence.source_id, Persistence.uuid, unique=True)
Index('ix_persistence_permanent_last_update', Persistence.permanent, Persistence.last_update)

# this is used to map what observables had what tags in what alerts
# not to be confused with ObservableTagMapping (see above)
# I think this is what I had in mind when I originally created ObservableTagMapping
# but I was missing the alert_id field
# that table was later repurposed to automatically map tags to observables

class ObservableTagIndex(Base):

    __tablename__ = 'observable_tag_index'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    observable_id = Column(
        Integer,
        ForeignKey('observables.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True)

    tag_id = Column(
        Integer,
        ForeignKey('tags.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        index=True)

    alert_id = Column(
        Integer,
        ForeignKey('alerts.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        index=True)

    observable = relationship('aceui.database.schema.Observable', backref='observable_tag_index')
    tag = relationship('aceui.database.schema.Tag', backref='observable_tag_index')
    alert = relationship('aceui.database.schema.Alert', backref='observable_tag_index')

class Tag(Base):
    
    __tablename__ = 'tags'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True)

    name = Column(
        String(256),
        nullable=False,
        index=True,
        unique=True)

    @property
    def display(self):
        tag_name = self.name.split(':')[0]
        if tag_name in ace.CONFIG['tags'] and ace.CONFIG['tags'][tag_name] == "special":
            return False
        return True

    @property
    def style(self):
        tag_name = self.name.split(':')[0]
        if tag_name in ace.CONFIG['tags']:
            return ace.CONFIG['tag_css_class'][ace.CONFIG['tags'][tag_name]]
        else:
            return 'label-default'

    #def __init__(self, *args, **kwargs):
        #super(aceui.database.schema.Tag, self).__init__(*args, **kwargs)

    @reconstructor
    def init_on_load(self, *args, **kwargs):
        super(aceui.database.schema.Tag, self).__init__(*args, **kwargs)

class TagMapping(Base):

    __tablename__ = 'tag_mapping'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    tag_id = Column(
        Integer,
        ForeignKey('tags.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True)

    alert_id = Column(
        Integer,
        ForeignKey('alerts.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        index=True)

    alert = relationship('aceui.database.schema.Alert', backref='tag_mapping')
    tag = relationship('aceui.database.schema.Tag', backref='tag_mapping')

class Remediation(Base):

    __tablename__ = 'remediation'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True)

    type = Column(
        String,
        nullable=False,
        default='email')

    action = Column(
        Enum('remove', 'restore'),
        nullable=False,
        default='remove',
        comment='The action that was taken, either the time was removed or it was restored.')

    insert_date = Column(
        TIMESTAMP, 
        nullable=False, 
        index=True,
        server_default=text('CURRENT_TIMESTAMP'),
        comment='The time the action occured.')

    update_time = Column(
        TIMESTAMP, 
        nullable=True, 
        index=True,
        server_default=None,
        comment='Time the action was last attempted')

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
        index=True,
        comment='The user who performed the action.')

    user = relationship('aceui.database.schema.User', backref='remediations')

    key = Column(
        String(512),
        nullable=False,
        index=True,
        comment='The key to look up the item.  In the case of emails this is the message_id and the recipient email address.')

    restore_key = Column(
        String(512),
        nullable=True,
        comment='optional location used to restore the file from')

    result = Column(
        Text,
        nullable=True,
        comment='The result of the action.  This is free form data for the analyst to see, usually includes error codes and messages.')

    _results = None

    @property
    def results(self):
        if self._results is None:
            try:
                if self.result is None:
                    self._results = {}
                else:
                    self._results = json.loads(self.result)
            except:
                self._results = {'remediator_deprecated': {'complete': True, 'success':self.successful, 'result':self.result}}
        return self._results

    comment = Column(
        Text,
        nullable=True,
        comment='Optional comment, additional free form data.')
    
    @property
    def alert_uuids(self):
        """If the comment is a comma separated list of alert uuids, then that list is provided here as a property.
           Otherwise this returns an emtpy list."""
        result = []
        if self.comment is None:
            return result

        for _uuid in self.comment.split(','):
            try:
                validate_uuid(_uuid)
                result.append(_uuid)
            except ValueError:
                continue

        return result

    successful = Column(
        BOOLEAN,
        nullable=True,
        default=None,
        comment='1 - remediation worked, 0 - remediation didn’t work')

    lock = Column(
        String(36), 
        nullable=True,
        comment='Set to a UUID when an engine processes it. Defaults to NULL to indicate nothing is working on it.')

    lock_time = Column(
        DateTime,
        nullable=True)

    status = Column(
        Enum('NEW', 'IN_PROGRESS', 'COMPLETED'),
        nullable=False,
        default='NEW',
        comment="""
        The current status of the remediation.
        NEW - needs to be processed
        IN_PROGRESS - entry is currently being processed
        COMPLETED - entry completed successfully""")

    @property
    def json(self):
        return {
            'id': self.id,
            'type': self.type,
            'action': self.action,
            'insert_date': self.insert_date,
            'user_id': self.user_id,
            'key': self.key,
            'result': self.result,
            'comment': self.comment,
            'successful': self.successful,
            'status': self.status,
        }

    def __str__(self):
        return f"Remediation: {self.action} - {self.type} - {self.status} - {self.key} - {self.result}"

class EncryptedPasswords(Base):

    __tablename__ = 'encrypted_passwords'
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    key = Column(
        String(256),
        primary_key=True,
        nullable=False,
        comment='The name (key) of the value being stored. Can either be a single name, or a section.option key.')

    encrypted_value = Column(
        Text,
        nullable=False,
        comment='Encrypted value, base64 encoded')
