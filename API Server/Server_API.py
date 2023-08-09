from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import urllib.parse
import urllib.request
import tldextract
import re
import enchant
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from flask_cors import CORS
import ssl

app = Flask(__name__)
cors = CORS(app)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.options |= ssl.OP_NO_TLSv1  # Disable TLS v1.0
ssl_context.options |= ssl.OP_NO_TLSv1_1  # Disable TLS v1.1
ssl_context.set_ciphers('ECDHE+AESGCM')  # Set desired cipher suites

@app.route('/translate', methods=['POST'])
def translate():
    posturl = request.get_json()
    phishing_keywords = ['login', 'secure', 'banking', 'account', 'confirm', 'verify', 'update', 'paypal', 'amazon', 'ebay']
    srv_clt_keywords = ['server','client']
	
    def check_phishing_keywords(url, phishing_keywords):
        for keyword in phishing_keywords:
            if keyword in url:
                return keyword
        return None

    def check_srv_clt(url, srv_clt_keywords):
        for keyword in srv_clt_keywords:
            if keyword in url:
                return keyword
        return None
	
    url_info_list = []
	
    for url in posturl:
        parsed_url = urllib.parse.urlparse(url)
        extracted = tldextract.extract(url)
        subdomain = extracted.subdomain
        if subdomain == 'www':
            www = 1
        else:
            www = 0
    
        protocol = parsed_url.scheme
        if protocol == 'http':
            http = 1
        else:
            http = 0
        if protocol == 'https':
            https = 1
        else:
            https = 0
        path_length = len(parsed_url.path)
        query_length = len(parsed_url.query)
        netloc_length = len(parsed_url.netloc)
        tld_length = len(extracted.suffix)
        url_length = len(url)
        url_numbers_count = sum(len(re.findall(r'\d', url)) for url in [url])
        url_letter_count = len(re.findall(r'[a-zA-Z]', url))
        url_special_count = len(re.findall(r'[^\w\s]', url))
        and_count = url.count('&')
        percent_count = url.count('%')
        dot_count = url.count('.')
        equal_count = url.count('=')
        hyphen_count = url.count('-')
        underscore_count = url.count('_')
        tilde_count = url.count('~')
        semicolon_count = url.count(';')
        keyword = check_phishing_keywords(url, phishing_keywords)
        if keyword:
            phishing = 1
        else:
            phishing = 0
        keyword = check_srv_clt(url, srv_clt_keywords)
        if keyword:
            srv_clt = 1
        else:
            srv_clt = 0

        url_info = {
            'path_length': path_length, #path 길이
            'query_length': query_length, #quert 길이
            'netloc_length': netloc_length, #netloc 길이 
            'tld_length' : tld_length, #tld 길이
            'url_length': url_length,
            'url_numbers_count' : url_numbers_count, #url의 존재하는 숫자 갯수
            'url_letter_count' : url_letter_count, #url의 존재하는 문자 갯수
            'url_special_count' : url_special_count, #url의 특수문자 갯수
            'and_count' : and_count, #&
            'percent_count' : percent_count, #%
            'dot_count' : dot_count, #.
            'equal_count' : equal_count, #=
            'hyphen_count' : hyphen_count, #-
            'underscore_count' : underscore_count, #_
            'tilde_count' :tilde_count , #~
            'semicolon_count' :semicolon_count, #;
            'www' : www, #www
            'phishing': phishing, #피싱에 자주 사용되는 키워드 존재 유무
            'srv_clt' : srv_clt, #서버 또는 클라이언트의 단어가 존재하는지
        }
    
        url_info_list.append(url_info)

    data = pd.read_csv('./url_info2.csv',encoding='latin1')

    feature_columns = list(data.columns.difference(['url_type']))

    X = data[feature_columns]
    y = data['url_type']

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size = 0.2, random_state=42)

    model = DecisionTreeClassifier(random_state=0, max_depth=20)
    model.fit(X_train, y_train)

    url_info_df = pd.DataFrame(url_info_list)
    url_info_df = url_info_df.reindex(columns=feature_columns)

    malignancy = []
    for i in range(len(posturl)):
        label = model.predict(url_info_df)[i]
        if label == 0:
            malignancy.append(posturl[i])
    translated_url = malignancy  # Placeholder for the translated URL
    
    return jsonify({'result': translated_url})

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain('server.crt', 'server.key','server.csr')  # Specify the paths to your SSL certificate and key files

    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
