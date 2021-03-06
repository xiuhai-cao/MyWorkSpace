# coding=utf-8
# python_version:python3
import mysql.connector


class DataBase():
    def __init__(self, host, port, user, passwd, database, table, rows):
        self.host = host
        self.port = port
        self.user = user
        self.passwd= passwd
        self.database = database
        self.table = table
        self.rows = rows
        self.conn = mysql.connector.connect(host=self.host, port=self.port, user=self.user,
                                       password=self.passwd, database=self.database, charset='utf8')
        self.cursor = self.conn.cursor()

        # 直接从数据库中获取表的columns名称
        self.cursor.execute("SHOW COLUMNS from " + str(self.table))
        columns_info = self.cursor.fetchall()
        self.columns = [column_info[0] for column_info in columns_info]
        self.columns = tuple(self.columns)
        self.columns = str(self.columns).replace('\'', '')

    def push(self):
        for row in self.rows:
            row = tuple(row)
            sql_insert_sentence = "insert into " + str(self.table) + str(self.columns) + " values" + str(row)
            try:
                #尝试插入一条数据
                self.cursor.execute(sql_insert_sentence)
            except mysql.connector.errors.IntegrityError:
                #利用异常IntegrityError自动过滤待推送数据中与表中已有数据重复的数据条目
                pass

        self.conn.commit()

    def select_column_to_print(self, column):
        #选择需要打印哪些列
        column = str(column).replace('\'', '')
        select_column_sentence = "select " + str(column) + " from " + str(self.table)
        self.cursor.execute(select_column_sentence)
        values = self.cursor.fetchall()
        for value in values:
            print(value)

    def close_cursor(self):
        #关闭cursor
        self.cursor.close()


if __name__ == '__main__':
    jenkinsbuilddata = {'jenkinsbuilddata': {'Data': [
        [
        u'4041',
        u'SUCCESS',
        u'Started by upstream project "master/master-pipeline-merge" build number 3,054',
        '2020-02-02 21:41:37',
        u'https://cloudci.zte.com.cn/wireline-zenic-vdc/view/test-data-collect/job/master/job/test/job/master-test-worker/4041/',
        1145,
        '2020-02-07 11:22:31',
        u'master/master-pipeline-merge',
        u'master-pipeline-merge-3054-part1',
        86,
        0,
        86,
        u'4041',
        u'SUCCESS',
        76,
        u'SUCCESS',
        886,
        u'SUCCESS',
        121
    ],
    [
        u'4043',
        u'SUCCESS',
        u'Started by upstream project "master/master-pipeline-merge" build number 3,054',
        '2020-02-02 21:41:37',
        u'https://cloudci.zte.com.cn/wireline-zenic-vdc/view/test-data-collect/job/master/job/test/job/master-test-worker/4041/',
        1145,
        '2020-02-07 11:22:31',
        u'master/master-pipeline-merge',
        u'master-pipeline-merge-3054-part1',
        86,
        0,
        86,
        u'4041',
        u'SUCCESS',
        76,
        u'SUCCESS',
        886,
        u'SUCCESS',
        121
    ]
    ]},
        'Columns': [
            "build_num_api",
            "build_result",
            "trigger_reason",
            "build_time",
            "build_url",
            "build_duration",
            "grabdata_time",
            "version_num",
            "test_part_name",
            "test_total_count",
            "test_fail_count",
            "test_pass_count",
            "build_num_wfapi",
            "alloctopo_result",
            "alloctopo_duration",
            "deploy_result",
            "deploy_duration",
            "test_result",
            "test_duration"
        ]}

    rows = jenkinsbuilddata["jenkinsbuilddata"]["Data"]
    JenkinsBuildData = DataBase(host='127.0.0.1', port=3306, user='root', passwd='201211', database="test",
                                table="jenkinsbuilddata", rows=rows)
    JenkinsBuildData.push()
    JenkinsBuildData.select_column_to_print(column="build_num_api,build_result")
    JenkinsBuildData.close_cursor()
