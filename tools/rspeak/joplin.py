"""Joplin REST API 客户端

通过本地 Web Clipper 服务（默认 localhost:41184）与 Joplin 交互。
支持笔记的创建、更新、读取以及笔记本管理。
"""

import json
import base64
from pathlib import Path
from dataclasses import dataclass, field

import httpx


DEFAULT_BASE_URL = "http://localhost:41184"


@dataclass
class JoplinNote:
    """Joplin 笔记数据结构"""
    id: str = ""
    title: str = ""
    body: str = ""
    parent_id: str = ""  # notebook/folder id
    source_url: str = ""
    created_time: int = 0
    updated_time: int = 0
    is_todo: int = 0
    tags: list = field(default_factory=list)


@dataclass
class JoplinNotebook:
    """Joplin 笔记本数据结构"""
    id: str = ""
    title: str = ""
    parent_id: str = ""


class JoplinClient:
    """Joplin Data API 客户端"""

    def __init__(self, token: str, base_url: str = DEFAULT_BASE_URL):
        self.token = token
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(timeout=30)

    def _params(self, extra: dict | None = None) -> dict:
        p = {"token": self.token}
        if extra:
            p.update(extra)
        return p

    def _get(self, path: str, **params) -> dict:
        resp = self._client.get(
            f"{self.base_url}{path}",
            params=self._params(params),
        )
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, data: dict) -> dict:
        resp = self._client.post(
            f"{self.base_url}{path}",
            params=self._params(),
            json=data,
        )
        resp.raise_for_status()
        return resp.json()

    def _put(self, path: str, data: dict) -> dict:
        resp = self._client.put(
            f"{self.base_url}{path}",
            params=self._params(),
            json=data,
        )
        resp.raise_for_status()
        return resp.json()

    def _delete(self, path: str) -> None:
        resp = self._client.delete(
            f"{self.base_url}{path}",
            params=self._params(),
        )
        resp.raise_for_status()

    def ping(self) -> bool:
        """检测 Joplin 服务是否可用"""
        try:
            resp = self._client.get(f"{self.base_url}/ping")
            return resp.text.strip('"') == "JoplinClipperServer"
        except httpx.ConnectError:
            return False

    # ---- 笔记本操作 ----

    def list_notebooks(self) -> list[JoplinNotebook]:
        """列出所有笔记本"""
        result = []
        page = 1
        while True:
            data = self._get("/folders", page=page)
            items = data.get("items", data) if isinstance(data, dict) else data
            if not items:
                break
            for item in items:
                result.append(JoplinNotebook(
                    id=item["id"],
                    title=item["title"],
                    parent_id=item.get("parent_id", ""),
                ))
            if isinstance(data, dict) and not data.get("has_more", False):
                break
            page += 1
        return result

    def find_notebook(self, title: str) -> JoplinNotebook | None:
        """按标题查找笔记本"""
        for nb in self.list_notebooks():
            if nb.title == title:
                return nb
        return None

    def create_notebook(self, title: str, parent_id: str = "") -> JoplinNotebook:
        """创建笔记本"""
        data = {"title": title}
        if parent_id:
            data["parent_id"] = parent_id
        resp = self._post("/folders", data)
        return JoplinNotebook(id=resp["id"], title=title, parent_id=parent_id)

    def get_or_create_notebook(self, title: str) -> JoplinNotebook:
        """获取或创建笔记本"""
        nb = self.find_notebook(title)
        if nb is None:
            nb = self.create_notebook(title)
        return nb

    # ---- 笔记操作 ----

    def create_note(
        self,
        title: str,
        body: str,
        parent_id: str = "",
        source_url: str = "",
    ) -> JoplinNote:
        """创建笔记

        Args:
            title: 标题
            body: Markdown 内容
            parent_id: 笔记本 ID
            source_url: 来源 URL
        """
        data = {"title": title, "body": body}
        if parent_id:
            data["parent_id"] = parent_id
        if source_url:
            data["source_url"] = source_url
        resp = self._post("/notes", data)
        return JoplinNote(id=resp["id"], title=title, body=body, parent_id=parent_id)

    def update_note(self, note_id: str, **kwargs) -> dict:
        """更新笔记（只更新提供的字段）"""
        return self._put(f"/notes/{note_id}", kwargs)

    def get_note(self, note_id: str, fields: str = "id,title,body,parent_id,source_url,created_time,updated_time") -> JoplinNote:
        """获取笔记详情"""
        data = self._get(f"/notes/{note_id}", fields=fields)
        return JoplinNote(
            id=data["id"],
            title=data.get("title", ""),
            body=data.get("body", ""),
            parent_id=data.get("parent_id", ""),
            source_url=data.get("source_url", ""),
            created_time=data.get("created_time", 0),
            updated_time=data.get("updated_time", 0),
        )

    def search_notes(self, query: str, limit: int = 10) -> list[JoplinNote]:
        """搜索笔记"""
        data = self._get("/search", query=query, limit=limit, fields="id,title,parent_id,source_url")
        items = data.get("items", data) if isinstance(data, dict) else data
        return [
            JoplinNote(
                id=item["id"],
                title=item.get("title", ""),
                parent_id=item.get("parent_id", ""),
                source_url=item.get("source_url", ""),
            )
            for item in items
        ]

    # ---- 标签操作 ----

    def list_tags(self) -> list[dict]:
        """列出所有标签，分页获取"""
        result = []
        page = 1
        while True:
            data = self._get("/tags", page=page)
            items = data.get("items", data) if isinstance(data, dict) else data
            if not items:
                break
            result.extend(items)
            if isinstance(data, dict) and not data.get("has_more", False):
                break
            page += 1
        return result

    def find_tag(self, title: str) -> dict | None:
        """按标题精确查找标签"""
        for tag in self.list_tags():
            if tag["title"] == title:
                return tag
        return None

    def create_tag(self, title: str) -> dict:
        """创建标签"""
        return self._post("/tags", {"title": title})

    def get_or_create_tag(self, title: str) -> dict:
        """幂等获取/创建标签"""
        tag = self.find_tag(title)
        if tag is None:
            tag = self.create_tag(title)
        return tag

    def set_note_tags(self, note_id: str, tag_titles: list[str]) -> None:
        """为笔记同步标签（增删至完全匹配 tag_titles）

        移除不在 tag_titles 中的标签，添加缺少的标签。
        """
        existing = self.get_note_tags(note_id)
        existing_map = {t["title"]: t["id"] for t in existing}
        desired = set(tag_titles)

        # 移除多余标签
        for title, tag_id in existing_map.items():
            if title not in desired:
                self._delete(f"/tags/{tag_id}/notes/{note_id}")

        # 添加缺少的标签
        for title in desired:
            if title not in existing_map:
                tag = self.get_or_create_tag(title)
                try:
                    self._post(f"/tags/{tag['id']}/notes", {"id": note_id})
                except httpx.HTTPStatusError:
                    pass

    def get_note_tags(self, note_id: str) -> list[dict]:
        """获取笔记的所有标签

        Returns:
            [{"id": ..., "title": ...}, ...]
        """
        data = self._get(f"/notes/{note_id}/tags", fields="id,title")
        items = data.get("items", data) if isinstance(data, dict) else data
        return [{"id": item["id"], "title": item["title"]} for item in items]

    # ---- 资源操作 ----

    def get_note_resources(self, note_id: str) -> list[dict]:
        """获取笔记关联的资源列表"""
        data = self._get(f"/notes/{note_id}/resources", fields="id,title,mime,file_extension")
        items = data.get("items", data) if isinstance(data, dict) else data
        return items

    def get_resource(self, resource_id: str) -> dict:
        """获取资源元数据

        Returns:
            包含 id, title, mime, filename, file_extension 的 dict
        """
        return self._get(
            f"/resources/{resource_id}",
            fields="id,title,mime,filename,file_extension",
        )

    def get_resource_file(self, resource_id: str) -> bytes:
        """下载资源文件内容"""
        resp = self._client.get(
            f"{self.base_url}/resources/{resource_id}/file",
            params=self._params(),
        )
        resp.raise_for_status()
        return resp.content

    # ---- 嵌套笔记本路径 ----

    def resolve_notebook_path(self, path: str) -> JoplinNotebook:
        """按 '/' 分隔路径解析嵌套笔记本，缺失的层级自动创建

        Args:
            path: 如 "Thought/Writing/Blog"

        Returns:
            最终层级的 JoplinNotebook
        """
        parts = [p.strip() for p in path.split("/") if p.strip()]
        if not parts:
            raise ValueError("笔记本路径不能为空")

        notebooks = self.list_notebooks()
        # 构建 {(parent_id, title): notebook} 索引
        index = {}
        for nb in notebooks:
            index[(nb.parent_id, nb.title)] = nb

        parent_id = ""
        current = None
        for part in parts:
            key = (parent_id, part)
            if key in index:
                current = index[key]
            else:
                current = self.create_notebook(part, parent_id)
                index[(parent_id, part)] = current
            parent_id = current.id
        return current

    def upload_resource(self, file_path: Path, title: str = "") -> dict:
        """上传附件资源（图片等）

        Returns:
            包含 id, title 等字段的 dict
        """
        if not title:
            title = file_path.name
        with open(file_path, "rb") as f:
            resp = self._client.post(
                f"{self.base_url}/resources",
                params=self._params(),
                data={"props": json.dumps({"title": title})},
                files={"data": (file_path.name, f)},
            )
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
