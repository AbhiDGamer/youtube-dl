# coding: utf-8
from __future__ import unicode_literals

import re
import time
import os.path

from .common import InfoExtractor
from ..utils import (
    compat_urllib_parse,
    compat_urllib_request,
)


class PlayedIE(InfoExtractor):
    IE_NAME = 'played.to'
    _VALID_URL = r'https?://played\.to/(?P<id>[a-zA-Z0-9_-]+)'

    _TEST = {
        'url': 'http://played.to/j2f2sfiiukgt',
        'md5': 'c2bd75a368e82980e7257bf500c00637',
        'info_dict': {
            'id': 'j2f2sfiiukgt',
            'ext': 'flv',
            'title': 'youtube-dl_test_video.mp4',
        },
    }

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')

        orig_webpage = self._download_webpage(url, video_id)
        fields = re.findall(r'type="hidden" name="(.+?)"\s* value="?(.+?)">', orig_webpage)
        data = dict(fields)

        self.to_screen('%s: Waiting for timeout' % video_id)
        time.sleep(2)

        post = compat_urllib_parse.urlencode(data)
        headers = {
            b'Content-Type': b'application/x-www-form-urlencoded',
        }
        req = compat_urllib_request.Request(url, post, headers)
        webpage = self._download_webpage(
            req, video_id, note='Downloading video page ...')

        title = os.path.splitext(data['fname'])[0]

        video_url = self._search_regex(
            r'file: "?(.+?)",', webpage, 'video URL')

        return {
            'id': video_id,
            'title': title,
            'url': video_url,
        }