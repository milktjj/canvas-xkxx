import pymssql
import pandas as pd
import threading

course_df = pd.DataFrame()
lock = threading.Lock()

sql = """select   
c.course_schoolyear, c.course_term,c.course_id ,c.instructional_class_id, c.course_name , c.course_kcdm  , c.course_credit, c.course_hours,c.course_type,
dg.KKBMMC as org,
dg.KCFZRJGH as kcfzegh ,dg.KCFZRXM  as kcfzr  ,
c.jw_gh  as teacher_id,u.user_name  as teacher,
convert(varchar(8000), DG.ZWKCJJ) as chinese,
convert(varchar(8000), DG.YWKCJJ) as english
from t_course c
left join t_user u on u.user_id =c.jw_gh 
left join t_org org on org.org_id =c.org_id 
left join CourseInfo.dbo.t_kcdg dg on dg.kch=c.course_kcdm  and dg.KCMC =c.course_name and dg.KKBMMC =org.org_name 
where c.course_schoolyear ='2023-2024' and c.course_term =1 and c.oper_status <> 3 and c.SJLY =60200 and dg.KKBMMC <> '密西根学院'
order by c.course_id 
"""


sql2 = """
select   
c.course_schoolyear, c.course_term,c.course_id ,c.instructional_class_id, convert(varchar(100), c.course_name) as course_name , c.course_kcdm  , c.course_credit, c.course_hours,c.course_type,
dg.KKBMMC as org,

dg.KCFZRJGH as kcfzegh ,dg.KCFZRXM  as kcfzr  ,
c.jw_gh  as teacher_id,convert(varchar(100),u.user_name) as teacher,
convert(varchar(8000), DG.ZWKCJJ) as chinese,
convert(varchar(8000), DG.YWKCJJ) as english
from t_course c
left join t_user u on u.user_id =c.jw_gh 

left join t_org org on org.org_id =c.org_id 
left join CourseInfo.dbo.t_kcdg dg on dg.kch=c.course_kcdm  and dg.KCMC =c.course_name and dg.KKBMMC =org.org_name 

where c.course_schoolyear ='2023-2024' and c.course_term =1 and c.oper_status <> 3 and c.SJLY =60200 and dg.KKBMMC <> '密西根学院'
order by c.course_id 

"""

sql3 = """
select   
c.course_schoolyear, c.course_term,c.course_id ,c.instructional_class_id, convert(varchar(100), c.course_name) as course_name , dg.kch as course_code, c.course_hours,c.course_type,dg.kcxz as course_type_2, 
dg.KKBMMC as org,dg.XF as course_xf, 

dg.KCFZRJGH as kcfzegh ,dg.KCFZRXM  as kcfzr  ,
c.jw_gh  as teacher_id,convert(varchar(100),u.user_name) as teacher,
convert(varchar(8000), DG.ZWKCJJ) as chinese,
convert(varchar(8000), DG.YWKCJJ) as english,
dg.kcmb as course_target, dg.khfs as course_exam
from t_course c
left join t_user u on u.user_id =c.jw_gh 

left join t_org org on org.org_id =c.org_id 
left join CourseInfo.dbo.t_kcdg dg on dg.kch=c.course_kcdm  and dg.KCMC =c.course_name and dg.KKBMMC =org.org_name 

where c.oper_status <> 3 and c.SJLY =60200 and dg.KKBMMC <> '密西根学院'
order by c.course_id 
"""

sql4 = """
select   
c.course_schoolyear, c.course_term, c.course_id,c.instructional_class_id, convert(varchar(100), c.course_name) as course_name ,
dg.kch as course_code ,dg.ZXS as course_hour , dg.kcxz as course_type, 
dg.KKBMMC as org, dg.XF as course_score, 
dg.KCFZRJGH as dg_kcfzegh ,dg.KCFZRXM  as dg_kcfzr  ,
c.jw_gh  as c_teacher_id,convert(varchar(100),u.user_name) as course_teacher,
convert(varchar(8000), DG.ZWKCJJ) as chinese,
convert(varchar(8000), DG.YWKCJJ) as english,
dg.kcmb as course_target, dg.khfs as course_exam
from t_course c
left join t_user u on u.user_id =c.jw_gh 
left join t_org org on org.org_id =c.org_id 
left join CourseInfo.dbo.t_kcdg dg on dg.kch=c.course_kcdm  and dg.KCMC =c.course_name and dg.KKBMMC =org.org_name 
where c.oper_status <> 3 and c.SJLY =60200 
and c.course_schoolyear  ='2023-2024' and c.course_term  =1
and dg.XNMC ='2023-2024' and dg.XQMMC =1
order by c.course_id  
"""

charset = 'GB18030'


def get_course_df():
    return course_df


def get_course_infos():
    conn = pymssql.connect(server='10.119.5.39', user='etcsjtu_read',
                           password='N5knPJvN', database='CourseInfo', port='10086', charset=charset)
    # cursor = conn.cursor(as_dict=True)
    cursor = conn.cursor()
    cursor.execute(sql4)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    row_set = set(rows)
    course_info_list = []
    for info in row_set:
        result_dict = {k: v for k, v in zip(column_names, info)}
        course_info_list.append(result_dict)
    print(len(course_info_list))
    a = set([])
    for row in course_info_list:
        a.add(row.get('course_id'))
    print(len(a))
    cursor.close()
    conn.close()
    return course_info_list


def refresh_course_df():
    course_info_list = get_course_infos()
    df = pd.DataFrame(course_info_list)
    print(len(df))
    df = df.drop_duplicates()
    print(len(df))
    df = df.sort_values(['chinese', 'english', 'course_target', 'course_exam'], ascending=False).drop_duplicates(
        subset=df.columns.difference(['chinese', 'english', 'course_target', 'course_exam'])).sort_index()

    df_first = df.groupby('course_id').first().reset_index()

    def merge_set_without_nan(x):
        merged_set = set()
        for value in x:
            if pd.notnull(value):
                merged_set.add(value)
        return merged_set

    df_merged = df.groupby('course_id')[['course_type', 'course_teacher']].agg(
        merge_set_without_nan).reset_index()

    result = pd.merge(df_first, df_merged, on='course_id')
    result = result.drop(['course_teacher_x', 'course_type_x'], axis=1)
    result = result.rename(
        columns={'course_teacher_y': 'course_teacher', 'course_type_y': 'course_type'})
    global course_df
    with lock:
        course_df = result


def get_course_info_in_sis(sis_id_list):
    course_df = get_course_df()
    print(len(course_df))
    result = course_df[course_df['course_id'].isin(sis_id_list)]
    print(result)


def get_course_info_by_sis(sis_id):
    course_df = get_course_df()
    ret_df = course_df[course_df['course_id'] == sis_id]
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)
    print(ret_df)
    return ret_df.to_json(orient='records')


if __name__ == "__main__":
    course_info_list = get_course_infos()
    import pandas as pd
    df = pd.DataFrame(course_info_list)
    print(len(df))
    df = df.drop_duplicates(inplace=True)
    print(len(df))
    df = df.sort_values(['chinese', 'english', 'course_target', 'course_exam'],
                        ascending=False).drop_duplicates(subset=df.columns.difference(
                            ['chinese', 'english', 'course_target', 'course_exam'])).sort_index()

    print(len(df))
    print(df.iloc[0].to_dict())
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)
    # grouped = df.groupby('course_id')
    # for course_id, group in grouped:
    #     print("Course ID:", course_id)
    #     print(group)
