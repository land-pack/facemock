import sqlite3

db_path = '/Users/frank/code/selenium-dev/facemock2/facemock/core/mock.db'

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def save_image(conn, img):
    """
    Create a new project into the projects table
    :param conn:
    :param image:
    :return: project id
    """
    sql = ''' INSERT INTO image
                (img_id, location, url, status)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()

    cur.execute(sql, img)
    conn.commit()
    return cur.lastrowid

def load_image(image):
    print("image -->", image)
    default = (
        "image unique id",
        "//button[.='Yes']",
        "http://localhost:5000/assets/hd/t00001.png",
        "done"
    )
    image = image or default
    conn = create_connection(db_path)
    print("conn -> ", conn)
    row_id = save_image(conn, image)
    print("row_id:", row_id)


if __name__ == '__main__':
    s = ('./meta/click_at_1593606595_.png', "{'x': 615.88330078125, 'y': 473.5, 'width': 28.0, 'height': 20.0}", 'simple.com', 'done')
    load_image(s)
