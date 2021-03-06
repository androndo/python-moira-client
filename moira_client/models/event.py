from ..client import InvalidJSONError
from ..client import ResponseStructureError


MAX_FETCH_LIMIT = 1000


class EventManager:
    def __init__(self, client):
        self._client = client

    def fetch_by_trigger(self, trigger, limit=MAX_FETCH_LIMIT):
        """
        Get all events by trigger
        :param trigger: Trigger trigger
        :param limit: int limit
        :return: list of dicts

        :raises: ValueError
        :raises: ResponseStructureError
        """
        if not trigger.id:
            raise ValueError('Trigger id is None')
        params = {
            'p': 0,
            'size': limit
        }
        result = self._client.get(self._full_path(trigger.id), params=params)
        if 'list' not in result:
            raise ResponseStructureError("list doesn't exist in response", result)

        return result['list']

    def delete_all(self):
        """
        Remove all events

        :return: True on success, False otherwise
        """
        try:
            result = self._client.delete(self._full_path("/all"))
            return False
        except InvalidJSONError as e:
            if e.content == b'':  # successfully if response is blank
                return True
            return False

    def _full_path(self, path=''):
        if path:
            return 'event/' + path
        return 'event'
