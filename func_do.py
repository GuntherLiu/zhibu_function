#encoding=utf-8
import logger
import save_util
from time import sleep
import random


class Func:
    def __init__(self):
        print 'the function of zhibu '
        self.zhibu_session = save_util.do_read()
        if self.zhibu_session.is_login():
            print 'the persistence zhibu_session is logined'
        else:
            print 'the persistence zhibu_session is not logined'

    def check_in(self):
        logger.logger('the check in func')
        sleep(10)
        check_in_url = 'https://capi.dangjianwang.com/official/ucenter/ucuser/checkin'
        check_in_body = {
            'version': '0.0.1',
            'client': '2'
        }
        self.zhibu_session.do_post(check_in_url, check_in_body)
        print '1. check in '

    def do_comments(self):
        logger.logger('the post comments func')
        sleep(10)

        history_comment_url = 'https://capi.dangjianwang.com/official/cms/article/list'
        post_comment_url = 'https://capi.dangjianwang.com/official/cms/comment/add'
        page_index = save_util.do_read('comment_page_index')
        history_comment_body = {
            'page_index': page_index,
            'menu_id': 'a751aa593cee6067ce55067241eee11b',
            'system_id': '1645bedea45d734cbef263f4fa378215'
        }
        save_util.do_write(page_index-1, 'comment_page_index')
        news_list = self.zhibu_session.do_post(history_comment_url, history_comment_body).json()['data']['list']

        for i, tem in enumerate(news_list):
            if i % 4 == 0 and i != 0:
                sleep(61)
            nid = tem['id']
            data = {
                'article_id': nid,
                'content': u'关注#',
                'img': []
            }
            resc = self.zhibu_session.do_post(post_comment_url, data)
            print '%s%s, %d' % ('2. comment post:  ',  resc.content, i)
            sleep(5)

    def do_view(self):
        logger.logger('the post view func')
        sleep(10)
        view_url = 'https://capi.dangjianwang.com/official/view/View/publish'
        view_list = save_util.do_read('view_list')
        content = view_list[random.randint(0, len(view_list) -1)]
        view_body = {
            'content': content,
            'auth': 0,
            'img': []
        }
        for i in xrange(3):
            res = self.zhibu_session.do_post(view_url, view_body)
            print '3. view post' + res.content
            sleep(5)

    def do_forum(self):
        logger.logger('the post forum func')
        sleep(10)
        bbs_list_url = 'https://capi.dangjianwang.com/official/bbs/home/listBySys'
        bbs_list_body = {
            'system_id': 52994,
            'page_index': 1,
            'page_size': 10
        }
        bbs_list = self.zhibu_session.do_post(bbs_list_url, bbs_list_body).json()['data']['list']

        post_forum_url = 'https://capi.dangjianwang.com/official/bbs/comment/add'
        forum_list = save_util.do_read('forum_list')
        for q in bbs_list:
            pid = q['id']
            content = forum_list[random.randint(0, len(forum_list)-1)]
            post_help_body = {
                'pid': pid,
                'content': content,
                'img': [],
                'system_id': 52994
            }
            res = self.zhibu_session.do_post(post_forum_url, post_help_body)
            print '4. forum post' + res.content
            sleep(5)

    def do_idea(self):
        logger.logger('the post idea func')
        get_topic_url = 'https://capi.dangjianwang.com/official/study/Material/getTopicList'
        get_topic_body = {
            'page_index': 2,
            'page_size': 9
        }
        topic_list = self.zhibu_session.do_post(get_topic_url, get_topic_body).json()

        get_mat_list_url = 'https://capi.dangjianwang.com/official/study/Material/getMatList'
        post_mat_url = 'https://capi.dangjianwang.com/official/study/comment/add'

        for i in xrange(5):
            if topic_list['code'] == 200:
                topic = topic_list['data'][random.randint(0, len(topic_list['data'])-1)]
                topic_id = topic['id']
                logger.logger(topic, u'the choice topic')
            get_mat_list_body = {
                'topic_id': topic_id,
                'page_index': 1,
                'page_size': 10
            }
            mat_list = self.zhibu_session.do_post(get_mat_list_url, get_mat_list_body).json()
            if mat_list['code'] == 200 and len(mat_list) > 0:
                mat = mat_list['data'][random.randint(0, len(mat_list['data'])-1)]
                mat_id = mat['id']
                logger.logger(mat, u'the choice mat')
            ideal_list = save_util.do_read('ideal_list')
            ideal_content = ideal_list[random.randint(0, len(ideal_list)-1)]
            post_mat_body = {
                'mid': mat_id,
                'content': ideal_content,
            }
            res = self.zhibu_session.do_post(post_mat_url, post_mat_body)
            print '%s, %s' % ('4 ideal mat post', res.content)
            sleep(5)

    def do_time(self):
        logger.logger('the post time func')
        sleep(10)
        time_video = self.get_time_list()
        mid = time_video['data']['affix'][0]['hash']
        # video_type = time_video['data']['type']

        start_study_url = 'https://capi.dangjianwang.com/official/study/Common/startStudy'
        end_study_url = 'https://capi.dangjianwang.com/official/study/Common/endStudy'

        time_body = {
            'mid': mid,
            'type': 2,
            'web_time': 310
        }
        start_time_res = self.zhibu_session.do_post(start_study_url, None)
        print '5. start time res' + start_time_res.content
        sleep(310)
        time_res = self.zhibu_session.do_post(end_study_url, time_body)

        print '5.time post' + time_res.content
        sleep(10)

    def get_time_list(self):
        logger.logger('get time list first')
        time_list_url = "https://capi.dangjianwang.com/official/study/video/webstudynew"
        res_times_list = self.zhibu_session.do_post(time_list_url, None).json()['data']
        time_video = res_times_list[random.randint(0, len(res_times_list) -1)]
        mid = time_video['id']
        logger.logger(time_video, 'time one')

        view_detail_url = 'https://capi.dangjianwang.com/official/study/video/matDetail'
        view_detail_body = {
            'mid': mid
        }
        video_detail_res = self.zhibu_session.do_post(view_detail_url, view_detail_body).json()
        logger.logger(video_detail_res,"video_detail_res: ")

        return video_detail_res

    def do_exam(self):
        logger.logger('the post exam func')
        sleep(10)
        answer_list, bank_id = self.get_exam_list()
        post_begin_exam_url = 'https://capi.dangjianwang.com/official/exam/competition/begin'
        begin_exam_body = {
            'id': bank_id
        }
        question_list = self.zhibu_session.do_post(post_begin_exam_url, begin_exam_body).json()['data']['list']
        logger.logger(question_list, 'the question list')
        post_check_url = 'https://capi.dangjianwang.com/official/exam/ques/check'
        for i, ex in enumerate(question_list):
            qu_id = ex['id']
            user_answer = ''
            for qu in answer_list:
                if qu_id == qu['id']:
                    user_answer = qu['answer']
                    break

            check_body = {
                'bank_id': bank_id,
                'question_id': qu_id,
                'user_answer': user_answer,
                'answer_loc': 2
            }
            check_res = self.zhibu_session.do_post(post_check_url, check_body)

            print '7. exam post' + check_res.content
            if i == 9:
                check_res = self.zhibu_session.do_post(post_check_url, check_body)
                print '6. exam post  lsat exam' + check_res.content
            sleep(5)

    def get_exam_list(self):
        logger.logger('get exam list first')
        sleep(10)
        exam_topic_url = 'https://capi.dangjianwang.com/official/exam/competition/list'
        exam_topic_body = {
            'page_index': 1,
            'page_size': 10,
            'top': 1
        }
        exam_topic_res = self.zhibu_session.do_post(exam_topic_url, exam_topic_body).json()
        exam_topic_list = exam_topic_res['data']['list']

        exam_topic = exam_topic_list[random.randint(0, len(exam_topic_list) - 1)]
        logger.logger(exam_topic, 'the choice exam')
        exam_id = exam_topic['id']
        exam_content_url = 'https://capi.dangjianwang.com/official/exam/competition/order'
        exam_content_body = {
            'id': exam_id
        }
        res = self.zhibu_session.do_post(exam_content_url, exam_content_body)
        logger.logger(res.json(), 'the content exam in the topic')
        if res and res.json():
            answer_list = res.json()['data']['list']

        return answer_list, exam_id

def test():
    f = Func()
    f.check_in()
    f.do_view()
    f.do_comments()
    f.do_idea()
    f.do_forum()
    f.do_time()
    f.do_exam()


if __name__ == '__main__':
    test()