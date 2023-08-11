import mysql.connector
from os import environ

def insert_sentences(sentence, hand_label):
    """
    This function saves the reported sentence in a SQL database
    Input: the sentence to report, the hand label
    Output: None
    """
    try:
        db_host = environ.get('DB_HOST', "localhost")
        db_user = environ.get('DB_USER', "root")
        db_password = environ.get('DB_PASSWORD', "123456")

        connection = mysql.connector.connect(host=db_host,
                                                user=db_user,
                                                password=db_password)
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS isinno_db")
        connection.commit()
        cursor.execute("USE isinno_db")
        connection.commit()
        cursor.execute("CREATE TABLE IF NOT EXISTS reported_sentences (id INT AUTO_INCREMENT PRIMARY KEY, sentence VARCHAR(255) NOT NULL UNIQUE, hand_label VARCHAR(255))")
        connection.commit()
        cursor.execute("INSERT INTO reported_sentences (sentence, hand_label) VALUES (%s, %s) ON DUPLICATE KEY UPDATE hand_label = %s", (sentence, hand_label, hand_label))
        connection.commit()
        cursor.close()
        connection.close()
    

    except mysql.connector.Error as error:
        print("Failed to process the request into DB {}".format(error))