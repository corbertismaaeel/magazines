# -*- coding: utf-8 -*-

import os
import sys
import shutil
import datetime
import re


def find_magazine_dir(file_name):
    if 'TheEconomist' in file_name:
        return 'economist'
    if 'new_yorker' in file_name:
        return 'new_yorker'
    if 'nature' in file_name:
        return 'nature'
    if 'wired' in file_name:
        return 'wired'
    if 'atlantic' in file_name:
        return 'atlantic'
    return None


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception('参数错误! 需要传递 epub文件路径, '
                        '例如  python copy_ebook.py  /books/nature_2021.02.10.epub')
    epub_file_path = sys.argv[1]
    mag_name = os.path.basename(epub_file_path)
    magazine_dir = find_magazine_dir(mag_name)
    if magazine_dir is None or not os.path.exists(epub_file_path):
        raise Exception('文件名错误, 请检查: ' + epub_file_path)

    date_str = re.findall(r'\d{4}.\d{2}.\d{2}', mag_name)[0]
    print("=======> epub book : " + mag_name + ", date : " + date_str)

    # 将日期进行格式转换
    date_str = datetime.datetime.strptime(date_str, "%Y.%m.%d").strftime("%Y%m%d")
    full_path = "/github/magazines/" + magazine_dir + os.path.sep + date_str
    # 创建目录, 例如 /github/magazines/economist/2021.02.10/
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    # copy epub file
    shutil.copyfile(epub_file_path, full_path + os.path.sep + mag_name)
    # copy pdf
    shutil.copyfile(epub_file_path.replace(".epub", ".pdf"),
                    full_path + os.path.sep + mag_name.replace(".epub", ".pdf"))
