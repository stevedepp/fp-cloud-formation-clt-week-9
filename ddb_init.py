#!/usr/bin/env python

import json

def request(fin="conames.txt", request_type='PutRequest'):
    company_names = open(fin).read().splitlines()
    table_name = 'fang'
    request_type = 'PutRequest'
    request_names = []
    for company_name in company_names:
        request_names.append(
            {request_type:
                {'Item':
                    {'name':
                        {'S': company_name}
                    }
                }
            }
        )
    request_item = {'fang': request_names}
    print(json.dumps(request_item))
    return json.dumps(request_item)

if __name__ == '__main__':
#   request(fin)
    request()
