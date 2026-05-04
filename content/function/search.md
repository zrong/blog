+++
title = "站内搜索"
postid = 2678
date = 2017-08-06T11:12:42+08:00
isCJKLanguage = true
toc = false
type = "function"
slug = "search"
url = "/search/"
comment = false
+++

{{< rawhtml >}}
<style>
.search-box { display: flex; gap: 8px; margin: 1.5rem 0; }
.search-box input {
  flex: 1; padding: 10px 14px; font-size: 1rem;
  border: 2px solid #ddd; border-radius: 4px;
  outline: none; transition: border-color .2s;
}
.search-box input:focus { border-color: #3273dc; }
.search-box button {
  padding: 10px 20px; font-size: 1rem; cursor: pointer;
  background: #3273dc; color: #fff; border: none; border-radius: 4px;
  transition: background .2s;
}
.search-box button:hover { background: #2366d1; }
.search-status { color: #888; font-size: .9rem; margin: .5rem 0 1rem; }
.search-results { list-style: none; padding: 0; margin: 0; }
.search-result-item { padding: 1rem 0; border-bottom: 1px solid #f0f0f0; }
.search-result-item:last-child { border-bottom: none; }
.search-result-title { font-size: 1.1rem; font-weight: 600; }
.search-result-title a { color: #3273dc; text-decoration: none; }
.search-result-title a:hover { text-decoration: underline; }
.search-result-meta { font-size: .82rem; color: #888; margin: 3px 0 6px; }
.search-result-snippet { font-size: .9rem; line-height: 1.6; color: #555; }
.search-result-snippet mark { background: #fff3cd; padding: 0 2px; border-radius: 2px; }
.search-result-desc { font-size: .9rem; color: #666; margin: 4px 0 0; }
</style>

<div class="search-box">
  <input id="search-input" type="search" placeholder="输入关键词搜索全站文章…" autofocus>
  <button id="search-btn" onclick="doSearch()">搜索</button>
</div>
<div id="search-status" class="search-status"></div>
<ul id="search-results" class="search-results"></ul>

<script>
(function() {
  var API = 'https://aid.zengrong.net/api/search';
  var PAGE = 20;
  var currentQ = '', currentOffset = 0, totalCount = 0, loading = false;

  function esc(s) {
    return s ? s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') : '';
  }

  async function fetchResults(q, offset) {
    var r = await fetch(API + '?q=' + encodeURIComponent(q) + '&limit=' + PAGE + '&offset=' + offset);
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  }

  function renderItems(results) {
    var ul = document.getElementById('search-results');
    for (var i = 0; i < results.length; i++) {
      var item = results[i];
      var li = document.createElement('li');
      li.className = 'search-result-item';
      var html = '<div class="search-result-title"><a href="' + esc(item.url) + '">' + esc(item.title) + '</a></div>';
      html += '<div class="search-result-meta">' + esc(item.date) + '</div>';
      if (item.snippet) {
        html += '<div class="search-result-snippet">' + item.snippet + '</div>';
      } else if (item.description) {
        html += '<div class="search-result-desc">' + esc(item.description) + '</div>';
      }
      li.innerHTML = html;
      ul.appendChild(li);
    }
  }

  async function doSearch(append) {
    var q = document.getElementById('search-input').value.trim();
    if (!q) return;
    if (loading) return;

    if (!append) {
      currentQ = q;
      currentOffset = 0;
      document.getElementById('search-results').innerHTML = '';
    }

    loading = true;
    var statusEl = document.getElementById('search-status');
    statusEl.textContent = '搜索中…';

    try {
      var data = await fetchResults(currentQ, currentOffset);
      totalCount = data.total;
      renderItems(data.results || []);
      currentOffset += (data.results || []).length;

      if (totalCount === 0) {
        statusEl.textContent = '没有找到相关结果。';
      } else {
        statusEl.textContent = '共 ' + totalCount + ' 篇，已显示 ' + currentOffset + ' 篇' +
          (currentOffset < totalCount ? '（滚动加载更多）' : '（全部已显示）');
      }
    } catch(e) {
      statusEl.textContent = '搜索出错：' + e.message;
    }
    loading = false;
  }

  window.doSearch = doSearch;

  document.getElementById('search-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') doSearch();
  });

  window.addEventListener('scroll', function() {
    if (!currentQ || loading || currentOffset >= totalCount) return;
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200) {
      doSearch(true);
    }
  });

  var params = new URLSearchParams(window.location.search);
  var q0 = params.get('q');
  if (q0) {
    document.getElementById('search-input').value = q0;
    doSearch();
  }
})();
</script>
{{</ rawhtml >}}
