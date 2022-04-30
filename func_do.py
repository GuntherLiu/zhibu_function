#encoding=utf-8
import logger
import save_util
from time import sleep


class Func:
    def __init__(self):
        # logger.logger 'the function of zhibu '
        self.zhibu_session = save_util.get_zhibu_session()
        if self.zhibu_session.is_login():
            logger.logger('the persistence zhibu_session is logined')
        else:
            logger.logger('the persistence zhibu_session is not logined')

    def check_in(self):
        logger.logger('the check in func')
        sleep(10)
        check_in_url = 'https://capi.dangjianwang.com/official/ucenter/ucuser/checkin'

        check_in_body = {
            'version': '0.0.1',
            'client': '2'
        }
        self.zhibu_session.do_post(check_in_url, check_in_body)
        logger.logger('1. check in ')

    def do_comments(self):
        logger.logger('the post comments func')
        sleep(10)

        history_comment_url = 'https://capi.dangjianwang.com/official/cms/article/list'
        post_comment_url = 'https://capi.dangjianwang.com/official/cms/comment/add'
        detail_url = "https://capi.dangjianwang.com/official/cms/article/detail"
        # page_index = save_util.do_read('comment_page_index')
        history_comment_body = {
            'page_index': 1,
            'menu_id': 'a751aa593cee6067ce55067241eee11b',
            'system_id': '1645bedea45d734cbef263f4fa378215'
        }
        # save_util.do_write(page_index-1, 'comment_page_index')
        news_list = self.zhibu_session.do_post(history_comment_url, history_comment_body).json()['data']['list']

        for i, tem in enumerate(news_list):
            if i % 4 == 0 and i != 0:
                sleep(61)
            nid = tem['id']
            data = {
                'article_id': nid,
                'content': u'不忘初心，牢记使命',
                'img': []
            }
            data2 = {
                'article_id': nid
            }
            resc2 = self.zhibu_session.do_post(detail_url, data2)
            res = resc2.json()['msg']
            logger.logger('%s%s, %d' % ('2. get article detail:  ', res, i))
            sleep(5)
            resc = self.zhibu_session.do_post(post_comment_url, data)
            logger.logger('%s%s, %d' % ('3. comment post:  ',  resc.json()['msg'], i))
            sleep(5)

    def do_time(self):
        logger.logger('the post time func')
        sleep(10)
        mid = self.get_time_mid()
        # video_type = time_video['data']['type']

        start_study_url = 'https://capi.dangjianwang.com/official/study/common/studyTmpCard'
        add_time_url = 'https://capi.dangjianwang.com/official/study/common/addStudyTime'

        start_time_body = {
            'mid': mid,
            'type': 2
        }
        add_time_body = {
            'ticket': None
        }
        start_time_res = self.zhibu_session.do_post(start_study_url, start_time_body)
        res_json = start_time_res.json()
        if res_json:
            logger.logger('%s%s' % ('3. start time res:  ', res_json['msg']))
            ticket = res_json['data']['ticket']
            add_time_body['ticket'] = ticket
            study_time = 60 * 10 + 10
            snap_time = 9
            index = 0
            while index * snap_time < study_time:
                time_res = self.zhibu_session.do_post(add_time_url, add_time_body)
                index += 1
                sleep(snap_time)

                logger.logger('%s%s' % ('4. add time res:  ', time_res.json()))
        # sleep(10)

    def get_time_mid(self):
        logger.logger('get time list first')
        time_list_url = "https://capi.dangjianwang.com/official/study/video/matDetail"
        body = {
            'mid': '0b86df4066c6f4644d0094b30f879f33'
        }
        res_times_list = self.zhibu_session.do_post(time_list_url, body).json()['data']['affix']
        if len(res_times_list) > 0:
            time_video = res_times_list[0]
            mid = time_video['id']
            return mid
        else:
            logger.logger("get time mid ERROR")

    def do_exam(self):
        logger.logger('the post exam func')
        # sleep(10)
        bank_id = self.get_exam_list()
        post_begin_exam_url = 'https://capi.dangjianwang.com/official/exam/competition/begin'
        begin_exam_body = {
            'id': bank_id
        }
        question_list = self.zhibu_session.do_post(post_begin_exam_url, begin_exam_body).json()['data']['list']
        logger.logger("%s:%s " % ("question list: ", question_list))
        post_check_url = 'https://capi.dangjianwang.com/official/exam/ques/check'

        for i, ex in enumerate(question_list):
            qu_id = ex['id']
            user_answer = '0'
            options = len(ex['options'])
            i2 = 1
            while i2 < options:
                user_answer = ('%s,%d' % (user_answer, i2))
                i2 += 1
            check_body = {
                'bank_id': bank_id,
                'question_id': qu_id,
                'user_answer': user_answer,
                'answer_loc': 2
            }
            check_res = self.zhibu_session.do_post(post_check_url, check_body)

            logger.logger('%s %s' % ('5. exam post', check_res.json()['msg']))

            sleep(5)

    def get_exam_list(self):
        logger.logger('get exam list first')
        sleep(10)
        exam_list = 'https://capi.dangjianwang.com/official/exam/competition/zbgzlist'
        exam_list_body = {
            'page_index': 1,
            'page_size': 15,
            'category_id': 6
        }
        exam_topic_res = self.zhibu_session.do_post(exam_list, exam_list_body).json()
        exam_topic_list = exam_topic_res['data']['list']

        exam_topic = exam_topic_list[0]
        exam_id = exam_topic['bank_id']

        return exam_id


def do():
    f = Func()
    f.check_in()
    f.do_comments()
    f.do_time()
    f.do_exam()


def test2():
    f = Func()
    f.do_exam()