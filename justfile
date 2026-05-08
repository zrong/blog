set shell := ["bash", "-euo", "pipefail", "-c"]

remote_dir := "/srv/www/blog.zengrong.net"
aid_url := "https://aid.zengrong.net"
aid_region := "0"

dev:
    hugo server -D

build:
    hugo

deploy: build
    rsync -avz --delete public/ ubuntu@zengrong-net:{{remote_dir}}
    @echo "[OK] blog 部署完成"

push-index:
    @test -n "${AID_TOKEN}" || (echo "请设置 AID_TOKEN 环境变量" && exit 1)
    @echo "[*] 推送 blog 索引到 aid (r={{aid_region}})..."
    curl -s -X POST "{{aid_url}}/api/search/rebuild?r={{aid_region}}" \
        -H "Authorization: Bearer ${AID_TOKEN}" \
        -H "Content-Type: application/json" \
        -d @public/index.json
    @echo ""
    @echo "[OK] blog 索引已更新"

deploy-all: deploy push-index
    @echo "[OK] blog 部署 + 索引推送完成"
