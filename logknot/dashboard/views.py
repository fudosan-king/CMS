import urllib3
from urllib3.exceptions import TimeoutError
import time
import json
from wagtail.admin.menu import MenuItem


http = urllib3.PoolManager()


def fetch_url(url):
    while True:
        try:
            response = http.request('GET', url)
            break
        except TimeoutError:
            print('timeout retry after 10secs: {}'.format(url))
            time.sleep(10)
    if response.status != 200:
        print('Status code: {}'.format(response.status))
    return response.data


def fetch_url_to_json(url):
    while True:
        try:
            response = http.request('GET', url)
            break
        except TimeoutError:
            print('timeout retry after 10secs: {}'.format(url))
            time.sleep(10)
    if response.status != 200:
        print('Status code: {}'.format(response.status))
    return json.loads(response.data.decode('utf-8'))


class MenuBuildingItem(MenuItem):
    def is_shown(self, request):
        return (
            request.user.has_perm('buildinggroup.add_building') or
            request.user.has_perm('buildinggroup.change_building') or
            request.user.has_perm('buildinggroup.delete_building')
        )


class MenuRemovedItem(MenuItem):
    def is_shown(self, request):
        return (
            request.user.has_perm('removedgroup.change_removed')
        )


class MenuImportItem(MenuItem):
    def is_shown(self, request):
        return (
            request.user.has_perm('importgroup.add_import')
        )


class MenuLogsItem(MenuItem):
    def is_shown(self, request):
        return (
            request.user.has_perm('logsgroup.change_logs')
        )


class MenuSearchItem(MenuItem):
    def is_shown(self, request):
        return (
            request.user.has_perm('searchgroup.change_search')
        )
