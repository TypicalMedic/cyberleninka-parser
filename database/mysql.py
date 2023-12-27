import mysql.connector
from mysql.connector import connect, Error

class mysql:
    def __init__(self):
        self.conn = connect(
            port="3306",
            host="localhost",
            user="root",
            password="root",
            database="articles"
        )

    def AddRequestResult(self, res:[], req:{}):
        add_req_sql = f"INSERT INTO request (text, date, results_found) values('{req['text']}', TIMESTAMP('{req['date'].strftime('%Y-%m-%d %H:%M:%S')}'), {len(res)});"
        with self.conn.cursor() as cursor:
            cursor.execute(add_req_sql)
            self.conn.commit()
        
        last_id_sql = "SELECT LAST_INSERT_ID()"
        req_id = 0
        with self.conn.cursor() as cursor:
            cursor.execute(last_id_sql)
            result = cursor.fetchmany(1)
            req_id = result[0][0]
        
        for article in res:
            find_artcl_sql = f"SELECT url FROM article WHERE url='{article['url']}'"
            is_found = False
            with self.conn.cursor() as cursor:
                cursor.execute(find_artcl_sql)
                result = cursor.fetchall()
                if len(result) > 0:
                    is_found = True
            if not is_found:
                add_artcl_sql = f"INSERT INTO article (url, title, year, journal, science_field, abstract, likes, dislikes, seen, downloaded, link_gost) values('{article['url']}', '{article['title']}', {article['year']}, '{article['journal']}', '{article['science_field']}', '{article['abstract']}', {article['liked']}, {article['disliked']}, {article['viewed']}, {article['downloaded']}, '{article['gost_link']}');"
                with self.conn.cursor() as cursor:
                    cursor.execute(add_artcl_sql)
                    self.conn.commit()

                artcl_id = 0
                with self.conn.cursor() as cursor:
                    cursor.execute(last_id_sql)
                    result = cursor.fetchmany(1)
                    artcl_id = result[0][0]

                for w in article['keywords']:
                    add_words_sql = f"INSERT INTO keywords values({artcl_id}, '{w}');"
                    with self.conn.cursor() as cursor:
                        cursor.execute(add_words_sql)
                        self.conn.commit()

                for a in article['authors']:
                    add_words_sql = f"INSERT INTO authors values({artcl_id}, '{a}');"
                    with self.conn.cursor() as cursor:
                        cursor.execute(add_words_sql)
                        self.conn.commit()
            
                add_relation_sql = f"INSERT INTO article_request values({artcl_id}, {req_id});"
                with self.conn.cursor() as cursor:
                    cursor.execute(add_relation_sql)
                    self.conn.commit()
        return "Данные экспортированы в MySQL!"

