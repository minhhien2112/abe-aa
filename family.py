import uuid


def get_andersen_family_item():
    andersen_item = {
    'id': 'Andersen_' + str(uuid.uuid4()),
    'lastName': 'Andersen',
    'district': 'WA5',
    'parents': [
        {
            'familyName': None,
            'firstName': 'Thomas'
        },
        {
            'familyName': None,
            'firstName': 'Mary Kay'
        }
    ],
    'children': None,
    'address': {
        'state': 'WA',
        'county': 'King',
        'city': 'Seattle'
    },
    'registered': True
}
    return andersen_item

def get_wakefield_family_item():
    wakefield_item = {
        'id': 'Wakefield_' + str(uuid.uuid4()),
        'lastName': 'Wakefield',
        'district': 'NY23',
        'parents': [
            {
                'familyName': 'Wakefield',
                'firstName': 'Robin'
            },
            {
                'familyName': 'Miller',
                'firstName': 'Ben'
            }
        ],
        'children': [
            {
                'familyName': 'Merriam',
                'firstName': 'Jesse',
                'gender': None,
                'grade': 8,
                'pets': [
                    {
                        'givenName': 'Goofy'
                    },
                    {
                        'givenName': 'Shadow'
                    }
                ]
            },
            {
                'familyName': 'Miller',
                'firstName': 'Lisa',
                'gender': 'female',
                'grade': 1,
                'pets': None
            }
        ],
        'address': {
            'state': 'NY',
            'county': 'Manhattan',
            'city': 'NY'
        },
        'registered': True
    }
    return wakefield_item

def get_smith_family_item():
    smith_item = {
    'id': 'Johnson_' + str(uuid.uuid4()),
    'lastName': 'Johnson',
    'district': None,
    'registered': False
    }
    return smith_item

def get_johnson_family_item():
    johnson_item = {
    'id': 'Smith_' + str(uuid.uuid4()),
    'lastName': 'Smith',
    'parents': None,
    'children': None,
    'address': {
        'state': 'WA',
        'city': 'Redmond'
    },   
    'registered': True
    }
    return johnson_item
def get_index_dtb(id):
    db = {    "id": "Document1",
    "Seller detail": {
        "Name": "Alice",
        "Identiy": "18520051",
        "Phone": "09012439009",
        "Address": "Ktx khu B Di an",
        "key": "eJxNkktOBDEMRK8S9TqLOB/H4SoItQY0u9kNICHE3XHZzsAirY7jlMsv/j7O8+12ud/P83hKx+vX+/V+5KTRz8vt42rR50E5DcmJZ05dl5ScZsuJih7MpYe2GfjIDuuS7otK1R/WPGwq4aMSrLkDUhwpRDvKkbcgR9MjvJCnEgMeUI0QIfZjqbsSLurJKlCpnm+SZe368Gn2sKHttcRm/isi0cysETejuysq08NEqthbRKi0MG6GqaAx48OhLE7O3HeJUuzy0jwB3GVttFADHDABSIOOZsw2hE3M69sftSDtLlVpjngEeMdTjhHYYd1qUY0XtEYfsEwRiLFWDMMUT/NnIg/anb6LkbfW5UEGOvOPL7OzNWSGxNnVGIXmswbXPQbGSkXHsgs25wbKaIx5Y+eYAtPtM15vzd0v+/vacGBsMI5mjF5+fgGOopQS"
    },
    "Buyer detail": {
        "Name": "Bob",
        "Identity": "215519191",
        "Phone": " 0956929888",
        "Address": "Dai hoc Cong Nghe thong tin Linh Trung Thu Duc",
        "key": "eJxNUkFuxDAI/IqVsw/GMcbuV6pVtK32tre0laqqfy8DOOrBjgMDDAM/23G8P+/neRzbS9revj8e55aTWr/uz8+HWV+ZcuKR05ScBk7LiWpVw9QH6YN3tVb8cE5SHdqGG0VtVAgXXlTUVPCHizTFoDD3rkcj2TxapQ9PR7QvbPOyngEV4Cn1ym5AhO1RmeYKLX6IOtB7xALMRrEHkKuT92RgbhV7kBqra6vo5BXYI9KtkKhclxGS5aeIR3c4Rt+yVvNLtIc/E7C7ew7/Gjf03jCM7hygHbelnazmcFVa7GVxRfB+SdGWerVcrYVgNgGKKRhPy0GR1tVvsRuI4eBmA/1HJEYSeiiqc6CRTGLQNh9AMBFp7sBK2La0oC3TvyYn6EIZW7drcborg8WUcM4RDXOLfCZ+pZAaAzQzgCyLJt1+/wDB95Va"
    },
    "Property Detail": {
        "Address": "Nga 4 Thu Duc",
        "Type": "Land",
        "Landtype": "Dat Tho cu",
        "Primary area": " 1000 m2 ",
        "Secondary area": " 500 m2",
        "Delivery Time": " 20-11-2022",
        "key": "eJxFUs1OxkAIfJWm5x6W7g+sr2JM82m+23ermhjjuzsDVA+0LAvDDOz3ehxvj9t5Hsf6tKyvX+/3c90WRD9vj4+7R5+7bEu3bZHS4MBMcRBErCNQYPu2TEsf1ir+MEXymEwGhA46/mkZkh0f2wM17oFoko5nG0yRohJpk/jAHBo+OQwa+czEVDjdGyBDNdhYDeq8YDXPUkhZUxeq7NKIlmNEsV7ikzm6NYtr4mkNPCkulbMgtz/dOLRE4XC0R4mDTUsOIjUQw/HiGUqdgiTfPUfBkbA5W2m5qJWRm/FiorTrQBSKsxLFLkgvUZZr9Y3mpKX0rO2+cM1R+oEty/4/SKrqNbs7a8s3Ua8Hk/Cx4z0mRMWtJnMunlpmTotr9eEwk6VsT0xvpvFkuHeum8tr+ebUCyXHJUVzt97IkgKTIoLrIS8/v9fykWE="
    },
    "Purchase price": {
        "Price": " 2 ti ",
        "Tax": " 20 Trieu",
        "Deposits": " 1,69 ti",
        "key": "eJxNUkluwzAM/Irhsw+irIXqV4rASIvccnNboCj693I4VJqLI1HkcJb8rMfxfr+e53GsL8v69v1xO9dtserX9f558+prlW2pui2K331bJOdt6c0OYhVJA5+MT2G9W/Owak08S8Zkt0s1FGtSH9EYrhVQe3zUbr3jUjnkW5o3S5RVHjebb1ZpsU4EvBIwMl8GILI/lUkZTar/nJywUp1irgdpl6SdKNhadvLVxtow4Jq536mJKCegAayBB72ugCo1tqaogGoZlO4ENYW0AlIyUZ8J1YdfLbwAtdYmcQnLafXgRsBBN9rc9ZSitRe2U4dMYgDxoNGXEO1ci0MfwawWul/6TEA6XXRnE5PwYonZGqYyYWVHeUqzTTM8TaiEguErc4DptMaXgo6nzX/kPt1KDOFxcVRf1SIE9PoLfPTg5PL7B1w/k8Q="
    },
    "Time and payments": {
        "Time": {
            "Phase 1": {
                "Price": "1 ti 5",
                "Time": "18-8-2000"
            },
            "Phase 2": {
                "Price": "500 tr",
                "Time": "28-8-2000"
            }
        },
        "Payments": {
            "Method": "Chuyen khoan",
            "Account name": "Alice",
            "Bank": "BIDV",
            "Account number": "5801000123890",
            "Beneficiary": "Bob"
        },
        "key": "eJw9UstOxDAM/JWo5xziNq4dfgWhakF721sBCSH+nczY3YMrx4+xZ9zf5Tg+HrfzPI7lpSzvP5/3c6llRr9vj687o68qtajXMkYt+zS1WmyvRWSbAZ2PtRYfCPSo2B2P2bajrLXZI3DwkZkz5FsWOqANmVncNzjAg9MmnsFGwliLScAdnIggmhsino40yzxHtjVeytRcWNZ2edgS+2uig1j3MO7Kbl8DHYbKbuHbFj6qIQvqvIcBDfx0C1GejFwSvllGoI77xZxrWeoLFJGR5JDvdvEiC6EHBjkTczCfyLvlHERNUzGqjB7sB8bYj1fM46jmgaA8V4D6vLXndqBLDJMYg72eelhgOcdv0QbeODTwtKeyzJIJR0mUGv8Uzd2JdpGRNU9H7FXyKKkr6Y0WqmtejsMCTUJfvfBRul+/Bv9Yefv7BwGakqE="
    },
    "Construction detail": {
        "Name contractors": "Cty TNHH Sala",
        "Address": "Binh Thanh",
        "Business Registration Certificate": "18UA9I",
        "Construction costs": {
            "Primary Area": "200 tr",
            "Secondary Area": "100 tr",
            "Addition Area ": "30 tr"
        },
        "TimeStart": "31-12-2022",
        "Payments": {
            "Method": "The",
            "Bank": "TP Bank",
            "Account Number": "58010001236778",
            "Payer": "Alice",
            "Payee": "Clint",
            "key": "eJw9UkFuwzAM+0qQcw6Wa8n2vjIMQTf01lu3AcOwv0+U6B6cWBJNU7R+9/P8uF8fj/PcX7b9/efz9tiPzbPf1/vXLbKvKsem49jMl5TGj03fCFJiXtdjGxf/12ObqJTiEMvANJeIIzqDQGvGUjqqwVjIOJx6CGoIvN490bD8YJtU0ScZcK775eZIbZTWLeHoQMQ/jTy9JWeQS63YAVeIEwlBuhpZm8D3pRMbMKKVuFd5fPoV0wFqaQK8gpYwQEqI16d9uL1K3g61EVAUjUKLY5mFUxq4QhwaT+ciBd3j2ViYLrmM8tE7zIVACIWfg7jBztL42FQ+RV0+QsfsWcYLhzZwLwONyUmLlK+dzSfPYDgaZwumL5axIPF+yzaMlxIVM5BPZFmBqi60tF9YjhEptHcZbp2MmAZ4tWYnptDk7e8fkueThA=="
        },
        "key": "eJxNUkluwzAM/Irgsw6iJWrpV4rCSIvccnNboCj693K4JDnIkLgMZ4b+3Y7j43Y5z+PYXtL2/vN5PbecJPp9uX1dNfrKlBPPnEbNacrhPac1cqJdEqPJKZIgS1LRTLEoFelrMyJLLoQ8yYuH56OdW5RgwPKm3iW7HqdLW2c5QCW0MHAkM8YDpzkuYtxR0EyATpwakSmDTAraqAQQEWbuwVOLgSWd7IzG7pisl+7uKAKFStwa8MqTc60+iTO3oMK8Q4gohjs8UhAJ1lyNhykHmTDM8KiaO0RukZlPjkTmiNa24cOUHheXq9xKFOp+yJTZ3Ol1Ooo5GCxT1iONRWIk3FMHVU1zSLUO1FZxeraB5q9WnZYaOWMn9kHVvP9K5T5xREjlsltOboall0mBRbaZ2CPEremODP8BO739/QPclpSv"
    }
    }
    db['id'] = id
    return db
if __name__ == '__main__':
    get_index_dtb()