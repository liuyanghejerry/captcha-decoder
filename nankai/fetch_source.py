# -*- coding: utf-8  -*-

import sys, httplib2, base64

def get_content():
    h = httplib2.Http()  
    resp, content = h.request("http://222.30.32.10/ValidateCode")
    return content

def content_to_file(content, num):
    f = open('%s%d.jpg'%(file_path, num), 'wb')
    f.write(content)
    f.close()

def main():
    times = int(sys.argv[1:][0])
    print '%d files needed.'%times
    for i in range(times):
        num_of_file = i
        c = get_content()
        content_to_file(c, i)
        print '%d files done.'%i


if __name__ == '__main__':
    file_path = './source/'
    main()