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
    ssl_dir = "./nginx/ssl/wsites"
    remove_subdirs(ssl_dir)
    mk_dir(ssl_dir)
    with open(os.path.join(ssl_dir, "ssl.json"), "r") as ssl_in:
        ssl = json.load(ssl_in)
        if ssl:
            print("Loaded ssl configs")
            for site, cert in ssl.items():
                p_cert = cert.get('pem')
                if p_cert:
                    with open(os.path.join(ssl_dir, f"{site}.pem"), "w") as pem:
                        pem.write(p_cert)
                        print(f"Written {ssl_dir}/{site}.pem")
                k_cert = cert.get('key', '')
                if k_cert:
                    with open(os.path.join(ssl_dir, f"{site}.key"), "w") as key:
                        key.write(k_cert)
                        print(f"Written {ssl_dir}/{site}.key")
    os.remove(os.path.join(ssl_dir, "ssl.json"))
except Exception as e:
    print(e)


# /nginx/conf.d/auth.json
# parse json auth for each site under "nginx/conf.d/.[site]passwd
try:
    conf_dir = "./nginx/conf.d/wsites"
    remove_subdirs(conf_dir)
    mk_dir(conf_dir)
    with open(os.path.join(conf_dir, "auth.json"), "r") as auth_in:
        auth = json.load(auth_in)
        if auth:
            print("Loaded auth configs")
            for site, passwd in auth.items():
                if not passwd:
                    continue
                with open(os.path.join(conf_dir, f".{site}passwd"), "w") as p:
                    p.write(passwd)
                    print(f"Written {conf_dir}/.{site}passwd")
    os.remove(os.path.join(conf_dir, "auth.json"))
except Exception as e:
    print(e)



