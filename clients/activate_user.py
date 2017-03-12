import sys
import json
import datetime

from urllib.request import Request, urlopen
from urllib.parse   import urlencode


def main():
    args = dict()
    args['username']=sys.argv[2]
    args['password']=sys.argv[3]
    args['role']=sys.argv[4]

    data = urlencode(args)
    my_route = sys.argv[1]+"activate_user"
#    my_route = "http://127.0.0.1:8080/activate_user"
    req = Request(my_route,data.encode('ascii'),method='POST')
    res = urlopen(req)
    print("Call to LOST returned: %s"%res.read().decode('ascii'))

if __name__=='__main__':
    main()
