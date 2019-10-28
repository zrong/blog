+++
title = "Google站内搜索"
postid = 2678
date = 2017-08-06T11:12:42+08:00
isCJKLanguage = true
toc = false
type = "function"
slug = "search"
url = "/search/"
comment = false
+++

使用 [Google CSE ](https://cse.google.com/) ，若无法访问 Google， 请使用首页中嵌入的搜索框。

{{< rawhtml >}}
<script>
  (function() {
    var cx = '010248203365983979668:happqssy-hw';
    var gcse = document.createElement('script');
    gcse.type = 'text/javascript';
    gcse.async = true;
    gcse.src = 'https://cse.google.com/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);
  })();
</script>
<gcse:search></gcse:search>
{{< rawhtml >}}
