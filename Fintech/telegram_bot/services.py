from contextlib import closing

from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return []
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def get_videos(sub_name, name=None, teacher=None):
    extra = ""
    tsql = ""
    if name:
        extra = f""" and lower(tv."name")= lower('{name}') """

    if teacher:
        tsql = f"where ss.course_id = {teacher}"

    sql = f"""
    select ts."name", array_agg(row_to_json(tv)) as videos from telegram_bot_sub ts
    inner join (
        select vv.video, vv.sub_id, vv."name", vv.chat_id, ss.course_id  from telegram_bot_videos vv
        inner join telegram_bot_sub ss on ss.id = vv.sub_id 
        {tsql}
        
    ) tv on tv.sub_id = ts.id
        where lower(ts."name") = lower(%s) {extra}

    group by ts."name" 
    """
    # print("\n\n\n", sql, "\n\n\n")
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql, [sub_name])

        items = dictfetchone(cursor)
        result = []

        if items:
            for i in items["videos"]:
                result.append(i)

    return result
