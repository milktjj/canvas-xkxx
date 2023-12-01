from datetime import date
from datetime import datetime, timedelta
import psycopg2

db_params = {
    "host": "10.119.10.48",
    "database": "postgres",
    "user": "postgres",
    "password": "Etc@1234",
    "port": "5432"
}


async def insert_data(timestamp, is_listen):
    # 连接到PostgreSQL数据库
    conn = psycopg2.connect(**db_params)

    try:
        # 创建游标对象
        cursor = conn.cursor()
        # 执行插入操作
        insert_query = "INSERT INTO tear (timestamp, is_listen) VALUES (%s, %s)"
        data = (timestamp, is_listen)
        cursor.execute(insert_query, data)

        # 提交事务
        conn.commit()

        print("数据插入成功！")

    except (Exception, psycopg2.Error) as error:
        print("数据插入失败:", error)

    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_is_listen(timestamp, is_listen):
    # 连接到PostgreSQL数据库
    conn = psycopg2.connect(**db_params)

    try:
        # 创建游标对象
        cursor = conn.cursor()

        # 执行更新操作
        update_query = "UPDATE tear SET is_listen = %s WHERE timestamp = %s"
        data = (is_listen, timestamp)
        cursor.execute(update_query, data)

        # 提交事务
        conn.commit()

        print("数据更新成功！")

    except (Exception, psycopg2.Error) as error:
        print("数据更新失败:", error)

    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_timestamp_range_by_date_string(date_string):
    # 解析日期字符串
    query_date = datetime.strptime(date_string, '%Y-%m-%d').date()

    # 构建日期范围
    start_date = datetime(query_date.year, query_date.month, query_date.day)
    end_date = start_date + timedelta(days=1)

    # 转换为时间戳
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    return start_timestamp, end_timestamp


def query_data_by_date(date_string):
    # 连接到PostgreSQL数据库
    conn = psycopg2.connect(**db_params)

    try:
        # 创建游标对象
        cursor = conn.cursor()
        start_date, end_date = get_timestamp_range_by_date_string(date_string)
        # 执行查询操作
        select_query = "SELECT * FROM tear WHERE timestamp >= %s AND timestamp < %s ORDER BY timestamp DESC"
        cursor.execute(select_query, (start_date, end_date))

        # 获取结果
        results = cursor.fetchall()

        # 输出结果
        # for row in results:
        #     print(row)

    except (Exception, psycopg2.Error) as error:
        print("查询数据失败:", error)

    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return results


if __name__ == "__main__":
    current_timestamp = int(datetime.timestamp(datetime.now()))
    is_listen = True

    insert_data(current_timestamp, is_listen)
    # current_timestamp = int(datetime.timestamp(datetime.now()))
    # timestamp = current_timestamp  # 要更新的时间戳
    # print(timestamp)
    # is_listen = False
    #
    # update_is_listen(1700118283, is_listen)
    query_data_by_date("2023-11-16")
