import re
from mitmproxy import ctx

def request(flow):
    remote_host = flow.request.pretty_host
    method = flow.request.method

    ctx.log.info('remote_host %s'%remote_host)
    ctx.log.info('request.host %s' % flow.request.host)
    ctx.log.info('request.path %s' % flow.request.path)
    ctx.log.info('request.pretty_url %s' % flow.request.pretty_url)
    ctx.log.info('request.query %s' % flow.request.query)
    ctx.log.info('request.method %s' % flow.request.method)
    ctx.log.info('client host %s' % flow.client_conn.address.host)

    flow.request.replace('Mozilla', 'Google', re.M)
