def application(env,start_response):
    start_response('200 ok',[('Content-Type','text/html')])
    return ["hello world"]


