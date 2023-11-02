CREATE TABLE t_course_info (
    course_schoolyear varchar(20),
    course_term NUMERIC(4,0),
    course_id varchar(35),
    instructional_class_id varchar(30),
    course_name text,
    course_kcdm TEXT,
    course_credit NUMERIC(4,0),
    course_hours NUMERIC(4,0),
    course_type varchar(5),
    org TEXT,
    kcfzegh TEXT,
    kcfzr TEXT,
    teacher_id TEXT,
    teacher TEXT,
    chinese TEXT,
    english TEXT
) WITH (ENCODING = 'GB18030', LC_COLLATE = 'Chinese_China.936', LC_CTYPE = 'Chinese_China.936');
