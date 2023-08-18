from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json, time
import capsolver
import requests
import threading, concurrent.futures

# 填入CapSolver API key // Enter your CapSolver API key here
API_KEY = ''
CAPSOLVER_MAX_RETRIES = 50
PUBLIC_POOL_MAX_RETRIES = 50

def get_token_from_capsolver(stop_event=threading.Event()):
    retry_count = 0
    capsolver.api_key = API_KEY
    solution = {}
    while retry_count < CAPSOLVER_MAX_RETRIES and not stop_event.is_set():
        try:
            solution = capsolver.solve({
                "type": "FunCaptchaTaskProxyLess",
                "websitePublicKey": "35536E1E-65B4-4D96-9D97-6ADB7EFF8147",
                "websiteURL": "https://chat.openai.com",
            })
            break
        except (capsolver.error.UnknownError, capsolver.error.Timeout) as e:
            retry_count += 1
            print(f"Error occurred: {e}. Retrying...%d/%d" % (retry_count, MAX_RETRIES,))
            time.sleep(5)
    else:
        if retry_count == MAX_RETRIES:
            print("Max retries reached. Please check the issue.")
#    if stop_event.is_set():
#        print('Stop CapSolver API solving.')

    return solution


def get_token_from_public_pool(url, stop_event=threading.Event()):
    s = requests.Session()
    retry_count = -1
    token = {}
    while retry_count < PUBLIC_POOL_MAX_RETRIES and not stop_event.is_set():
        retry_count += 1
        try:
            r = s.get(url, timeout=(5, 15))
        except:
            time.sleep(5)
            continue
        if r.status_code != 200:
            time.sleep(5)
            continue
        token = r.json()
        if 'token' not in token.keys() or len(token['token']) < 50:
            print('Wrong content for url: %s.\n%s' % (url, r.text, ))
            time.sleep(5)
            continue
        break
    else:
        if not stop_event.is_set():
            time.sleep(300)
    
    return token


def get_first_result(stop_event):
    executor = concurrent.futures.ThreadPoolExecutor()
	# 取消注释并赋值public_pool_urlx以启用公共token池
    # Uncomment and assign a value to public_pool_urlx to enable the public token pool support
	# 注意保持value值和service_pool中元素一一对应
    # Ensure that the values correspond with the elements in service_pool
    futures = {
        executor.submit(get_token_from_capsolver, stop_event): "capsolver", 
    #    executor.submit(get_token_from_public_poll, public_pool_url1, stop_event): "public_pool1", 
    #    executor.submit(get_token_from_public_pol2, public_pool_url2, stop_event): "public_pool2", 
    }
	service_pool = ('capsolver', 'public_pool1', 'public_pool2',)

    for future in concurrent.futures.as_completed(futures):
        if futures[future] in service_pool:
            stop_event.set()  # 通知其他函数提前结束 // Notify other functions to terminate early
            token = future.result()
            print('Service %s get the token first.' % futures[future])
            return token


def get_token():
    stop_event = threading.Event()
    result = get_first_result(stop_event)
    return result


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path != '/token':
            self.send_response(502)
            self.end_headers()
            return

        token = get_token()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(token).encode())
        return


if __name__ == '__main__':
    # 避免服务器暴露于公网 // Avoid binding to public ip address
    server = HTTPServer(('127.0.0.1', 8999), RequestHandler)
    print('Server started.\nGet your arkose token via http://127.0.0.1:8999/token')
    server.serve_forever()
