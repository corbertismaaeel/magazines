# -*- coding: utf-8 -*-

import os
import sys
import json
from json import JSONEncoder


class MagazineIssue(object):

    mag_name = ""
    file_name = ""
    pub_date = 0
    cover_name = ""
    formats = None

    def __init__(self, name, p_date, formats):
        self.mag_name = name
        self.pub_date = p_date
        self.formats = formats

    def add_format(self, book_format):
        self.formats.append(book_format)

    def __str__(self):
        return "name : %s, file_name : %s, pub_date : %d" % (self.mag_name, self.file_name, self.pub_date)


class MagEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__


def main(root_dir):
    print('repo dir : ' + root_dir)
    magazines = [{'dir': 'economist', 'name': "经济学人"}, {'dir': 'new_yorker', 'name': "纽约客"}]
    all_mag_issues = []
    for mag in magazines:
        mag_dir = root_dir + os.path.sep + mag.get('dir')
        # 杂志下每一期的杂志
        issues = os.listdir(mag_dir)
        for issue_date in issues:
            if os.path.isfile(issue_date):
                continue
            a_mag_issue = process_mag_issue(mag.get('name'), issue_date, mag_dir + os.path.sep + issue_date)
            if a_mag_issue is not None:
                all_mag_issues.append(a_mag_issue)
    # 按照发布日期排序
    all_mag_issues.sort(key=lambda x: x.pub_date, reverse=True)
    dump_json(root_dir=root_dir, all_mag_issues=all_mag_issues)


def dump_json(root_dir, all_mag_issues):
    if len(all_mag_issues) > 0:
        # dump to files
        with open(root_dir + os.path.sep + "magazines.json", 'w+') as jfile:
            json_content = json.dumps(all_mag_issues, cls=MagEncoder)
            jfile.write(json_content)


def process_mag_issue(mag_name, pub_date, issue_dir):
    try:
        mag_issue = MagazineIssue(mag_name, int(pub_date), formats=[])
        book_files = os.listdir(issue_dir)
        for f in book_files:
            if f.lower().endswith(".epub"):
                mag_issue.add_format("epub")
                mag_issue.file_name = os.path.splitext(f)[0]

            if f.lower().endswith(".pdf"):
                mag_issue.add_format("pdf")
                mag_issue.file_name = os.path.splitext(f)[0]

            if f.lower() == "cover.jpg" or f.lower() == "cover.jpeg" or f.lower() == "cover.png":
                mag_issue.cover_name = f
        return mag_issue
    except Exception as e:
        print("process_mag_issue error " + str(e))
    return None


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        raise Exception('参数错误!')
    repo_dir = sys.argv[1]
    main(repo_dir)