"""微信公众号 API 客户端

通过微信公众平台 API 发布文章（草稿 -> 发布）。
API 文档：https://developers.weixin.qq.com/doc/offiaccount/

主要流程：
1. 上传图片素材 -> 获取 media_id / url
2. 新建草稿（draft/add）
3. 发布草稿（freepublish/submit）
"""

import re
from pathlib import Path
from dataclasses import dataclass

import httpx
import markdown


API_BASE = "https://api.weixin.qq.com/cgi-bin"


@dataclass
class WechatArticle:
    """微信公众号文章结构"""
    title: str = ""
    content: str = ""  # HTML 内容
    author: str = ""
    digest: str = ""  # 摘要
    thumb_media_id: str = ""  # 封面图 media_id
    content_source_url: str = ""  # 原文链接
    need_open_comment: int = 0
    only_fans_can_comment: int = 0


class WechatClient:
    """微信公众号 API 客户端"""

    def __init__(self, appid: str, appsecret: str, access_token: str = ""):
        self.appid = appid
        self.appsecret = appsecret
        self._access_token = access_token
        self._client = httpx.Client(timeout=30)

    @property
    def access_token(self) -> str:
        if not self._access_token:
            self._refresh_token()
        return self._access_token

    def _refresh_token(self):
        """获取 access_token"""
        resp = self._client.get(
            f"{API_BASE}/token",
            params={
                "grant_type": "client_credential",
                "appid": self.appid,
                "secret": self.appsecret,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        if "access_token" not in data:
            raise RuntimeError(f"获取 access_token 失败: {data}")
        self._access_token = data["access_token"]

    def _api_url(self, path: str) -> str:
        return f"{API_BASE}{path}?access_token={self.access_token}"

    def upload_image(self, image_path: Path) -> dict:
        """上传图片素材（用于文章内图片）

        Returns:
            {"url": "https://mmbiz.qpic.cn/..."}
        """
        with open(image_path, "rb") as f:
            resp = self._client.post(
                self._api_url("/media/uploadimg"),
                files={"media": (image_path.name, f)},
            )
        resp.raise_for_status()
        data = resp.json()
        if "url" not in data:
            raise RuntimeError(f"上传图片失败: {data}")
        return data

    def upload_thumb(self, image_path: Path) -> str:
        """上传封面图（永久素材）

        Returns:
            media_id
        """
        with open(image_path, "rb") as f:
            resp = self._client.post(
                self._api_url("/material/add_material") + "&type=image",
                files={"media": (image_path.name, f)},
            )
        resp.raise_for_status()
        data = resp.json()
        if "media_id" not in data:
            raise RuntimeError(f"上传封面图失败: {data}")
        return data["media_id"]

    def add_draft(self, articles: list[WechatArticle]) -> str:
        """新建草稿

        Args:
            articles: 文章列表（支持多图文）

        Returns:
            media_id（草稿 ID）
        """
        payload = {
            "articles": [
                {
                    "title": a.title,
                    "author": a.author,
                    "digest": a.digest,
                    "content": a.content,
                    "thumb_media_id": a.thumb_media_id,
                    "content_source_url": a.content_source_url,
                    "need_open_comment": a.need_open_comment,
                    "only_fans_can_comment": a.only_fans_can_comment,
                }
                for a in articles
            ]
        }
        resp = self._client.post(self._api_url("/draft/add"), json=payload)
        resp.raise_for_status()
        data = resp.json()
        if "media_id" not in data:
            raise RuntimeError(f"创建草稿失败: {data}")
        return data["media_id"]

    def publish_draft(self, media_id: str) -> str:
        """发布草稿

        Args:
            media_id: 草稿 media_id

        Returns:
            publish_id
        """
        resp = self._client.post(
            self._api_url("/freepublish/submit"),
            json={"media_id": media_id},
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("errcode", 0) != 0:
            raise RuntimeError(f"发布失败: {data}")
        return data.get("publish_id", "")

    def get_publish_status(self, publish_id: str) -> dict:
        """查询发布状态"""
        resp = self._client.post(
            self._api_url("/freepublish/get"),
            json={"publish_id": publish_id},
        )
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
