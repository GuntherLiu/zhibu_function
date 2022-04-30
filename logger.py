#encoding=utf-8
import logging
import json
logging.basicConfig(filename='zhibu.log', format='%(asctime)s-%(levelname)s %(message)s', level=logging.DEBUG)


def logger(log, info=None):
    jm = json.dumps(log, ensure_ascii=False, indent=1)
    logging.info('%s: %s' % (info, jm))

def test():
    data = {
        'article_id': u'jfkdas90909023',
        'content': u'关注#',
        'img': []
    }
    url ='https://capi.dangjianwang.com/official/cms/comment/add'
    logger(data, url)

if __name__ == '__main__':
    test()