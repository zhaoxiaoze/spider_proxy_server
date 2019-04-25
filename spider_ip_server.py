# coding=utf-8
# get and vertify  proxy server,爬取万人骑的服务器代理，速度极慢，极不稳定

import re
import socket
import sys
import requests
import logging


class Proxy_search:


#默认加载的初始函数，定义一些全局变量，头信息

    def __init__(self):

        self.file_proxy_all_list = "proxy_all.txt"
        self.file_proxy_vaild_list = "proxy_vaild.txt"
        self.proxy_source = "http://www.xicidaili.com/wn/"
        self.verify_url = "http://www.baidu.com/"

#使用requests.session()的方法，区别于使用cookie的头设置
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        #'Accept-Language':' zh-CN,zh;q=0.9',
                        #'Cache-Control': 'max-age=0',
                        #'Connection': 'keep-alive',
                        #'Cookie': 'free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTNiMWJmZmVmOGQ3MWIwNjM5NDgzYzg0ODczZWEwYWM5BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTZUZXRkNW9FcUJ5Rkl3elhlNlRpSGhKM1BjYWxqQ1haVy9pVmtRKzdtRTQ9BjsARg%3D%3D--18b6ecb24ddc0e0912bbb92f36b4096ca85e15af; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1556156111; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1556156140',
                        #'Host':' www.xicidaili.com',
                        #'If-None-Match':' W/"a459f14496e99288f6ece1c2081774ea"',
                        #'Upgrade-Insecure-Requests': 1,
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

#定义一个log
        logging.basicConfig(filename='proxy_debug.log', filemode='w', level=logging.DEBUG)
#设置一个访问的3秒，防止阻塞
        socket.setdefaulttimeout(3)

#正则表达式从context里面匹配出 ip 和 port
    def get_ip_proxy(self,context):

        ip_port_list =[]

        get_ip_re = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}')
        ip_list = get_ip_re.findall(str(context))
#use tag compare port
        get_port_raw_with_tag = re.compile('<td>\d{2,5}</td>')
        port_list_raw = get_port_raw_with_tag.findall(str(context))

        get_port_list = re.compile('\d{5}|\d{4}|\d{2}')
        port_list = get_port_list.findall(str(port_list_raw))

#check
        print(ip_list)
        print(port_list)
#errot checking,check the num_of ip and port
        if ip_list is None:

            return None


        if port_list is None:

            return None


        if len(ip_list) != len(port_list):

            return None

        num_of_ip = len(ip_list)
        print(num_of_ip)

        for index in range(len(ip_list)):

            ip_port_list.append(str(ip_list[index]) + ':' + str(port_list[index]))


        return ip_port_list

        #check
        #print('ip_port_list:',ip_port_list)



#requests web
#save ip_port_st
    def get_webside_source(self,url):

        if len(url) == 0:

           print('Url is Null')
           return

        requests.adapters.DEFAULT_RETRIES = 5
        proxy_resource_requests = requests.session()
        proxy_resource_requests.keep_alive = False

        try:
            proxy_resource_result =  proxy_resource_requests.get(url,headers=self.headers)
#           content = BeautifulSoup(proxy_resource_result.text)
            #check
            #print(context)

        except:
            print('proxy resource can\'t get !!!' )
            return


        logging.debug(proxy_resource_result.content)

        proxy_list = self.get_ip_proxy(proxy_resource_result.content)
        #check
        print(proxy_list)
        #print(len(proxy_list))

        if len(proxy_list) == 0:
            print('Get proxy failed')
            return

        fd_proxy_all = open(self.file_proxy_all_list, 'w')

        with open(self.file_proxy_all_list, 'w') as fd_proxy_all:
            for ip_port in proxy_list:

                fd_proxy_all.write(str(ip_port)+'\n')


#testify ip and port
    def verify_proxy(self):

        test_lists = []
        index = 0
        requests.adapters.DEFAULT_RETRIES = 5
        text_proxy = requests.session()
        text_proxy.keep_alive = False
#read txt,读取的txt格式比较怪异，采用了先stick，再split的方法
        with open(self.file_proxy_all_list,'r') as  fd_proxy_all:

            for line in fd_proxy_all.read():

                test_lists.append(line)

                adds = ''.join(test_lists)

            #print(adds)
            results = adds.split('\n')
            print(results)
            for result in results:

                test_url = {'http':'https://' + result.strip('\n') }

                index +=1
                print(index)
                print(test_url)

                try:

                    test_page = text_proxy.get(self.verify_url, headers= self.headers, proxies= test_url,timeout=3)


                except:

                    print('Invaild proxy :',str(test_url))

                    continue

                if test_page.Statues_code != 200:

                    print('Invaild proxy :', str(test_url))
                    continue

                print('Vaild proxy:',str(test_url))

                with open(self.file_proxy_vaild_list,'a') as  fd_proxy_vaild:

                    fd_proxy_vaild.write(str(test_url) + '\n')





if __name__ == "__main__":
    prober_handle = Proxy_search()
    prober_handle.get_webside_source(prober_handle.proxy_source)
    prober_handle.verify_proxy()

