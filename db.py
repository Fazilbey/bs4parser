import sqlite3

conn=sqlite3.connect('example.db')
cursor=conn.cursor()


class DB :

    def insert_to_resource(self , res_name1 , res_url1 , top_tag1 , bottom_tag1 , title_cut1 , date_cut1) :
        conn=sqlite3.connect('example.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS resource
                        ( ID                INTEGER       PRIMARY KEY  AUTOINCREMENT,
                          RESOURCE_NAME     VARCHAR(255),
                          RESOURCE_URL      VARCHAR(255),
                          top_tag           VARCHAR(255)                NOT NULL,
                          bottom_tag        VARCHAR(255)     NOT NULL,
                          title_cut        VARCHAR(255)     NOT NULL,
                          date_cut        VARCHAR(255)     NOT NULL
                        );''')
        cursor.execute('''INSERT INTO  resource( RESOURCE_NAME, RESOURCE_URL, top_tag, bottom_tag, title_cut, date_cut)
                         VALUES (?,?,?,?,?,?)''' ,
                       (res_name1 , res_url1 , top_tag1 , bottom_tag1 , title_cut1 , date_cut1))

        conn.commit()

        conn.close()

    def insert_into_items(self , res_id1 , link1 , title1 , content1 , nd_date1 , s_date1 , not_date1) :
        conn=sqlite3.connect('example.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS items
                    ( id          INTEGER       PRIMARY KEY         NOT NULL,
                      res_id      INTEGER            NOT NULL,
                      link        VARCHAR(255)       NOT NULL,
                      title       TEXT               NOT NULL,
                      content     TEXT               NOT NULL,
                      nd_date     VARCHAR(255)       NOT NULL,
                      s_date      VARCHAR(255)       NOT NULL,
                      not_date    DATE               NOT NULL,
                      FOREIGN KEY (res_id)
                      REFERENCES resource(ID)
                      );''')

        cursor.execute('''INSERT INTO items(res_id, link, title, content, nd_date, s_date, not_date)
                    VALUES (?,?,?,?,?,?,?)''' ,
                       ( res_id1 , link1 , title1 , content1 , nd_date1 , s_date1 , not_date1))

        conn.commit()

        conn.close()
