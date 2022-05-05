#encoding=utf-8
import save_util
import time


def main():
    zhibu_session = save_util.get_zhibu_session()
    get_article_list(zhibu_session)


def get_article_list(zhibu_session):
    article_url = 'https://capi.dangjianwang.com/official/cms/article/list'
    comment_url = 'https://capi.dangjianwang.com/official/cms/comment/list'
    page_index = 5
    page_size = 20

    article_body = {
        'page_index': page_index,
        'page_size': page_size,
        'menu_id': 'a751aa593cee6067ce55067241eee11b',
        'system_id': '1645bedea45d734cbef263f4fa378215'
    }

    article_list = zhibu_session.do_post(article_url, article_body).json()['data']['list']
    print(len(article_list))
    for i, new in enumerate(article_list):
        n_id = new["id"]
        title = new["title"]
        with open("test.txt", "a", encoding="utf-8") as f:
            f.write("%d, %s \n" % (i, title))
        index = 1
        page_index2 = 1
        page_size2 = 100
        while True:
            comments_body = {
                "article_id": n_id,
                'page_index': page_index2,
                'page_size': page_size2
            }
            comment_list = zhibu_session.do_post(comment_url, comments_body).json()['data']['new']['list']
            for comment in comment_list:

                with open("test.txt", "a", encoding="utf-8") as f:
                    content = comment['content']
                    user_name = comment['user_name']
                    # print(content)
                    # user_name.encode("gbk").decode("utf-8")
                    # content.encode("gbk").decode("utf-8")
                    print("   %d, %s - %s - %s \n" %
                       (index, user_name,
                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(comment['createdt']))),
                       content))
                    f.write("   %d, %s - %s - %s \n" %
                       (index, user_name,
                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(comment['createdt']))),
                       content))
                index += 1
            page_index2 += 1
            if len(comment_list) < page_size2:
                print("   no more comments")
                break


def test():
    # print(time.localtime())
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1651120379)))

if __name__ == '__main__':
    main()