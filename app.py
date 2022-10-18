"""
    PYTHON APP(/SCRIPT) TO CALCULATE PERFORMANCES HOURLY AND STORE DATA
    IN MYSQL DATABASE
"""

import time
import logging
from datetime import datetime
from mysql.connector import connect, Error

logging.basicConfig(filename="log.txt", level=logging.DEBUG,
                    format="%(asctime)s %(message)s")

triggers = {
    "08:00": {"start": "07:00:00", "end": "07:59:59", "work_time": "60"},
    "09:00": {"start": "08:00:00", "end": "08:59:59", "work_time": "60"},
    "10:00": {"start": "09:00:00", "end": "09:59:59", "work_time": "60"},
    "11:00": {"start": "10:00:00", "end": "10:59:59", "work_time": "60"},
    "12:00": {"start": "11:00:00", "end": "11:59:59", "work_time": "60"},
    # "13:00": {"start": "12:00:00", "end": "12:59:59", "work_time": "60"},
    "14:00": {"start": "13:00:00", "end": "13:59:59", "work_time": "60"},
    "15:00": {"start": "14:00:00", "end": "14:59:59", "work_time": "60"},
    "16:00": {"start": "15:00:00", "end": "15:59:59", "work_time": "60"},
    "17:00": {"start": "16:00:00", "end": "17:00:00", "work_time": "60"},
}


def main():
    """ MAIN FUNCTION: FOR LOCAL SCOPING """
    logging.info("Program Started")

    while True:
        now = datetime.now()
        cur_day = now.strftime("%d/%m/%Y")
        cur_time = now.strftime("%H:%M")

        if cur_time in triggers:
            try:
                with connect(
                    host="localhost",
                    user="root",  # ETC
                    password="",  # SmarTex2021
                    database="db_etc",
                ) as conn:
                    print("Connection to DB succeeded!")
                    select_query = """
                        SELECT
                            registration_number,
                            Firstname,
                            Lastname,
                            ROUND(SUM((quantity * tps_ope_uni)) / """ + triggers[cur_time]["work_time"] + """, 2) AS performance
                        FROM
                            `pack_operation`
                        WHERE
                            cur_day = '""" + cur_day + """' AND cur_time BETWEEN '""" + triggers[cur_time]["start"] + """' AND '""" + triggers[cur_time]["end"] + """'
                        GROUP BY
                            registration_number;
                    """
                    insert_query = """
                        INSERT INTO performance_per_hour
                        (registration_number, first_name,
                        last_name, performance, cur_day, cur_time)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """

                    with conn.cursor() as cursor:
                        cursor.execute(select_query)
                        results = cursor.fetchall()

                        if len(results) > 0:
                            insert_records = [
                                (result[0], result[1], result[2],
                                 result[3], cur_day, cur_time,)
                                for result in results
                            ]
                            cursor.executemany(insert_query, insert_records)
                            conn.commit()
                            conn.close()

                            logging.info(
                                "Performance of operators calculated successfully")

                        else:
                            logging.info(
                                "No Performance of operators exist")

            except Error as msg_err:
                logging.error("DB Error: %s", msg_err)

        print(cur_day, cur_time)
        time.sleep(60)


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        logging.error("Keyboard Interrupt")

    except Exception as err:
        logging.error("Crashing Error: %s", err)
        # logging.error("Error Type: %s", type(err).__name__)
