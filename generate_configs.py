import json
import os


def remove_subdirs(d):
    for root, dirs, files in os.walk(d, topdown=False):
        for name in dirs:
            os.system(f"rm -rf {os.path.join(root, name)}")


def mk_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"Created directory {dir_name}")


# /nginx/ssl/ssl.json
# parse json file to key, pem for each site under "/nginx/ssl/[site]/*.[key|pem]"
try:
    ssl_dir = "./nginx/ssl/sites"
    remove_subdirs(ssl_dir)
    mk_dir(ssl_dir)
    with open(os.path.join(ssl_dir, "ssl.json"), "r") as ssl_in:
        ssl = json.load(ssl_in)
        if ssl:
            print("Loaded ssl configs")
            rsa = ssl.get("rsa_cloudflare")
            rsa = rsa if rsa else ''
            for site, cert in ssl.items():
                if "rsa_cloudflare" == site:
                    continue
                dir_name = os.path.join(ssl_dir, site)
                mk_dir(dir_name)
                with open(os.path.join(dir_name, "server.pem"), "w") as pem:
                    p_cert = cert.get('pem')
                    pem.write(f"{p_cert if p_cert else ''}{rsa}")
                    print(f"Written {dir_name}/server.pem")
                with open(os.path.join(dir_name, "server.key"), "w") as key:
                    k_cert = cert.get('key', '')
                    key.write(k_cert if k_cert else '')
                    print(f"Written {dir_name}/server.key")
except Exception as e:
    print(e)


# /nginx/conf.d/auth.json
# parse json auth for each site under "nginx/conf.d/.[site]passwd
try:
    conf_dir = "./nginx/conf.d/sites"
    remove_subdirs(conf_dir)
    mk_dir(conf_dir)
    with open(os.path.join(conf_dir, "auth.json"), "r") as auth_in:
        auth = json.load(auth_in)
        if auth:
            print("Loaded auth configs")
            for site, passwd in auth.items():
                if not passwd:
                    continue
                dir_name = os.path.join(conf_dir, site)
                mk_dir(dir_name)
                with open(os.path.join(dir_name, f".{site}passwd"), "w") as p:
                    p.write(passwd)
                    print(f"Written {dir_name}/.{site}passwd")
except Exception as e:
    print(e)



