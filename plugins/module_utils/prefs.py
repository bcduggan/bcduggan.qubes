from functools import wraps
from ansible.errors import AnsibleError
import qubesadmin
from qubesadmin.app import QubesBase
from qubesadmin.exc import QubesPropertyAccessError, QubesNoSuchPropertyError, QubesPropertyValueError

type PrefValue = None | bool | str | int | float
type PrefList = list[str]

def pref_accessor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (QubesPropertyAccessError, QubesNoSuchPropertyError, QubesPropertyValueError) as exc:
            raise AnsibleError from exc
    return wrapper

class QubesPrefs:
    def __init__(self):
        self.app = qubesadmin.Qubes()
        self.app.cache_enabled = True
        self.target = self._target()
        
    def _target(self) -> QubesBase:
        return self.app
    
    @pref_accessor
    def get(self, pref: str) -> PrefValue:
        return getattr(self.target, pref)

    # See qubesadmin/base.py:197
    # See qubesadmin/base.py:260
    def get_default(self, pref: str) -> PrefValue | type[AttributeError]:
        try:
            default = self.target.property_get_default(pref)
        except AttributeError as exc:
            raise AnsibleError from exc

        if isinstance(default, AttributeError):
            raise AnsibleError(f"Unparseable default value for preference type for preference {pref}")

        return default

    @pref_accessor
    def is_default(self, pref: str) -> bool:
        return self.target.property_is_default(pref)

    def list(self) -> PrefList:
        return self.target.property_list()

    @pref_accessor
    def set(self, pref: str, value: PrefValue) -> None:
        setattr(self.target, pref, value)

    @pref_accessor
    def delete(self, pref: str) -> None:
        delattr(self.target, pref)

class QvmPrefs(QubesPrefs):
    def __init__(self, qube: str, *args, **kwargs):
        self.qube = qube
        super().__init__(*args, **kwargs)

    def _target(self) -> QubesBase:
        return self.app.domains[self.qube]
