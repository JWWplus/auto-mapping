# coding=utf-8
# create database tlog character set utf8mb4;
import logging
import pandas as pd
from app_mysql_backend import Appversion, PageInfo, db, user

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

# df = pd.read_excel('分页面打点纪录点.xlsx', sheetname=['4.6', '4.7', '4.8', '4.9', '4.10'])
df = pd.read_excel('分页面打点记录点 new.xlsx', sheetname=['4.11', '4.12', '4.13'])
# sheetname = ['4.6', '4.7', '4.8', '4.9', '4.10']


sheetname = ['4.11', '4.12', '4.13']


def exl2mysql():
    for sheet in sheetname:
        df[sheet] = df[sheet].fillna('')
        appversion = Appversion(sheet)
        db.session.add(appversion)
        db.session.commit()
        app_id = appversion.id

        for i in df[sheet].index:
            logging.info('start to push line %d appversion: %s' % (i + 1, sheet))
            row = df[sheet].ix[i]
            if not row[u'页面'].strip():
                logging.error(u'该页面字段为空,跳过! appversion:%s, line: %d' % (sheet, i + 1))
                continue

            if row['se_category'].strip() or row['se_action'].strip():
                pageinfo_and = PageInfo(page=row[u'页面'], event=row[u'事件'], objects=row[u'对象'],
                                        appversion=appversion, types=row['type'], sub_type=row['sub_type'],
                                        pm=row.get(u'产品负责人', ''), page_key=row['page_key'], se_action=row[u'se_action'],
                                        se_category=row[u'se_category'], platform='Android',
                                        notes=row[u'额外信息'] + ', ' + row['Android'])
                db.session.add(pageinfo_and)

            if row['se_category.1'].strip() or row['se_action.1'].lstrip():
                pageinfo_ios = PageInfo(page=row[u'页面'], event=row[u'事件'], objects=row[u'对象'],
                                        appversion=appversion, types=row['type'], sub_type=row['sub_type'],
                                        pm=row.get(u'产品负责人', ''), page_key=row['page_key'],
                                        se_action=row[u'se_action.1'],
                                        se_category=row[u'se_category.1'], platform='iOS',
                                        notes=row[u'额外信息'] + ', ' + row['iOS'])
                db.session.add(pageinfo_ios)

            if row['se_category.2'].strip() or row['se_action.2'].strip():
                pageinfo_h5 = PageInfo(page=row[u'页面'], event=row[u'事件'], objects=row[u'对象'],
                                       appversion=appversion, types=row['type'], sub_type=row['sub_type'],
                                       pm=row.get(u'产品负责人', ''), page_key=row['page_key'], se_action=row[u'se_action.2'],
                                       se_category=row[u'se_category.2'], platform='H5',
                                       notes=row[u'额外信息'] + ', ' + row['H5'])
                db.session.add(pageinfo_h5)
        db.session.commit()

if __name__ == '__main__':
    # db.create_all()
    # admin = user('admin', 'admin', 'admin')
    # db.session.add(admin)
    # db.session.commit()
    exl2mysql()
