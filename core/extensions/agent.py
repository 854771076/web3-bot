import os,string
def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password, scheme='http', plugin_path=None):
    # 创建Chrome插件的manifest.json文件内容
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "16YUN Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    # 创建Chrome插件的background.js文件内容
    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["localhost"]
            }
        };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )

    # 创建插件目录并写入manifest.json和background.js文件
    os.makedirs(plugin_path, exist_ok=True)
    with open(os.path.join(plugin_path, "manifest.json"), "w+") as f:
        f.write(manifest_json)
    with open(os.path.join(plugin_path, "background.js"), "w+") as f:
        f.write(background_js)
    
    return os.path.join(plugin_path)

# 拆分代理url的函数
def split_proxy_url(proxy_url):
    parts = proxy_url.replace('http://','').split('@')
    if len(parts) == 2:
        auth_part, host_port = parts
        auth_parts = auth_part.split(':')
        if len(auth_parts) == 2:
            username, password = auth_parts
            host, port = host_port.split(':')
            return username, password, host, port
    return None, None, None, None