import json
from typing import Any
from django.http import HttpRequest
from django.template.context_processors import csrf as get_csrf


class Helper:
    @staticmethod
    def parse_json(data: str) -> Any:
        return json.loads(data)

    @staticmethod
    def is_ajax(header) -> bool:
        r = header.get('X-Requested-With')
        if r is not None and r == 'XMLHttpRequest':
            return True
        return False

    @staticmethod
    def get_csrf(r: HttpRequest) -> str:
        return get_csrf(r).get('csrf_token')
