import sys
import json
import datetime

from urllib.request import Request, urlopen
from urllib.parse import urlencode

def main():
    args = dict()
    args['username'] = sys.argv[2]

    data = urlencode(args)

    my_route= sys.argv[1] + "revoke_user"
    req = Request(my_route, data.encode('ascii'), method='POST')
    res = urlopen(req)
    
    print("Call to LOST returned: %s"%res.read().decode('ascii'))

if __name__=='__main__':
    main()
