# vim: ts=4:sw=4:et:cc=120

import json
from typing import Union, Any

import ace

from ace.analysis import RootAnalysis
from ace.json import JSONEncoder
from ace.system.alerting import AlertTrackingInterface
from aceui.database.schema import Alert

class DatabaseAlertTrackingInterface(AlertTrackingInterface):

    def track_alert(self, root: RootAnalysis):
        assert isinstance(root, RootAnalysis)
        alert = Alert.from_root(root)
        ace.db.merge(alert)
        ace.db.commit()
        return alert

    def get_alert(self, id: str) -> Union[Any, None]:
        assert isinstance(id, str)
        # XXX detach?
        return ace.db.query(Alert).filter(Alert.uuid == id).one_or_none()
