import pymysql

# autocommit=True指自动提交SQL语句执行结果，否则由于缓存原因会导致查询结果
# 不能及时查询到数据，尤其是更新过后的数据，默认建议设置，除非需要使用事务
conn = pymysql.connect(host='127.0.0.1', port=3306, user='qiang', password='123456',
                       database='woniuai', charset='utf8', autocommit=True)
print(conn.get_server_info())   # 能正常打印MySQL的版本号则说明连接成功

# cursor = conn.cursor()  # 执行任意SQL语句前均需要创建一个游标对象
# sql = "select * from users where userid<=3"
# cursor.execute(sql)     # 执行SQL语句
# result = cursor.fetchall()  # 从游标中返回全部结果，默认以(())二维元组保存
# print(result)            # 打印查询结果集里面的所有数据
#
# # 如果需要输出第二条用户信息的id号和电话号码，则通过取元组值的方式输出
# print(result[1][0], result[1][3])


from pymysql.cursors import DictCursor

cursor = conn.cursor(DictCursor)
sql = "select * from users where userid>3"
cursor.execute(sql)
result = cursor.fetchall()
print(result[1]['phone'])   # 打印第二行数据的phone字段的值，通过字段名取值

