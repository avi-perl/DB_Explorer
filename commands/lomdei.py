"""Module docstring is used as command help text"""

import typer
import requests
import pandas as pd

from utils.formatting import format_table
from utils.db_tools import get_engine

app = typer.Typer()


@app.command()
def locate_existing_user(username: str, split_char: str = "\\n"):
    """"""
    split_char = "\n" if split_char == "\\n" else split_char
    usernames = username.split(split_char)
    prepared_usernames = [f"'{username}'" for username in usernames]

    query = f"""select
                  u.id,
                  u.username,
                  if(teacher.appuser_id, 1, 0) as is_teacher,
                  c.id,
                  c.name,
                  concat("insert ignore into lyceum_usergroup_users (usergroup_id, appuser_id)  values (1, ", u.id, ");") as make_teacher
                from
                  lyceum_appuser u
                  left join lyceum_usergroup_users teacher on u.id = teacher.appuser_id
                  left join lyceum_class c on u.id = c.teacher_id
                where
                  u.username in ({','.join(prepared_usernames)})"""
    print(format_table(pd.read_sql(query, con=get_engine())))


@app.command()
def drop_class_and_users(class_id: str, split_char: str = "\\n"):
    """"""
    class_id = "\n" if class_id == "\\n" else class_id
    class_ids = class_id.split(split_char)
    engine = get_engine()

    query = f"""select
              c.*,
              t.username,
              t.email,
              t.is_active,
              t.is_verified,
              count(cs.appuser_id) as student_count
            from
              lyceum_class c
              left join lyceum_appuser t on c.teacher_id = t.id
              left join lyceum_class_students cs on c.id = cs.class_id
            where
              c.id in ({','.join(class_ids)})
            group by
              c.id"""
    df = pd.read_sql(query, con=engine)
    print(format_table(df))

    if input("Are you sure you want to drop these classes? [y/N] ")[:1].lower() == "y":
        with engine.connect() as con:
            for index, row in df.iterrows():
                class_id = row["id"]
                class_name = row["name"]

                print(f"Deleting STUDENTS from class '{class_name}' ({class_id})")
                query = f"""delete lyceum_class_students
                            from
                              lyceum_class_students
                            where
                              lyceum_class_students.class_id = {class_id}
                            """
                rs = con.execute(query)

                print(f"Deleting CLASS '{class_name}' ({class_id})")
                query = f"""delete lyceum_class
                           from
                             lyceum_class
                           where
                             lyceum_class.id = {class_id};"""
                rs = con.execute(query)


@app.command()
def verify_users(username: str, split_char: str = "\\n"):
    """"""
    split_char = "\n" if split_char == "\\n" else split_char
    usernames = username.split(split_char)
    prepared_usernames = [f"'{username}'" for username in usernames]

    query = f"""select
                  u.id,
                  u.username,
                  if(teacher.appuser_id, 1, 0) as is_teacher,
                  c.id,
                  c.name,
                  n.title,
                  if(
                    u.is_verified,
                    '',
                    concat(
                      "https://thumbprintapp.org/api/v2/user_auth/verify?username=",
                      u.username,
                      "&activation_key=",
                      u.activation_key,
                      "&add_default_nodes=0&api_client_code=1"
                    )
                  ) as verify_link
                from
                  lyceum_appuser u
                  left join lyceum_usergroup_users teacher on u.id = teacher.appuser_id
                  left join lyceum_class c on u.id = c.teacher_id
                  left join lyceum_node n on u.id = n.owner_id and n.tier = 0
                where
                  u.username in ({','.join(prepared_usernames)})"""
    df = pd.read_sql(query, con=get_engine())
    print(format_table(df))

    if input("Are you sure you want verify these users? [y/N] ")[:1].lower() == "y":
        for index, row in df.iterrows():
            verify_link = row["verify_link"]
            if verify_link:
                response = requests.get(verify_link)
                print(response.text)


@app.command()
def delete_user_nodes(username: str, split_char: str = "\\n"):
    """"""
    split_char = "\n" if split_char == "\\n" else split_char
    usernames = username.split(split_char)
    prepared_usernames = [f"'{username}'" for username in usernames]

    query = f"""select
                  u.id as user_id,
                  u.username,
                  u.last_login,
                  u.date_joined,
                  n.id as default_node,
                  user_with_node_to_delete.node_count
                from
                  lyceum_appuser u
                  join lyceum_node n on u.id = n.owner_id
                  and n.tier = 0
                  left join lyceum_usergroup_users is_teacher on u.id = is_teacher.appuser_id
                  and is_teacher.usergroup_id = 1
                  join (
                    # Users with a node to delete
                    select
                      n.owner_id as id,
                      count(n.id) as node_count
                    from
                      lyceum_node n
                    where
                      n.deleted = 0
                      and n.tier > 0
                    group by
                      n.owner_id
                  ) user_with_node_to_delete on u.id = user_with_node_to_delete.id
                where
                  u.username in ({','.join(prepared_usernames)})"""
    df = pd.read_sql(query, con=get_engine())
    print(format_table(df))


@app.command()
def user_class(username: str, split_char: str = "\\n"):
    """"""
    split_char = "\n" if split_char == "\\n" else split_char
    usernames = username.split(split_char)
    prepared_usernames = [f"'{username}'" for username in usernames]

    query = f"""select
                  u.id,
                  u.username,
                  c.id,
                  c.name
                from
                  lyceum_appuser u
                  left join lyceum_class_students cs on u.id = cs.appuser_id
                  left join lyceum_class c on cs.class_id = c.id
                where
                  u.username in ({','.join(prepared_usernames)})"""
    df = pd.read_sql(query, con=get_engine())
    print(format_table(df))


@app.command()
def create_class(teacher_username: str, class_name: str):
    engine = get_engine()
    query = f"""select id, username from lyceum_appuser where username = '{teacher_username}';"""
    df = pd.read_sql(query, con=engine)
    print(format_table(df))

    for index, row in df.iterrows():
        user_id = row["id"]
        username = row["username"]

        query = f"insert ignore into lyceum_class (name, teacher_id) values ('{class_name.strip()}', {user_id});"

        if (
            input(f"Are you sure you want to create the class '{class_name}'? [y/N] ")[
                :1
            ].lower()
            == "y"
        ):
            with engine.connect() as con:
                rs = con.execute(query)


@app.command()
def add_students_to_class(class_id: str, username: str, split_char: str = "\\n"):
    engine = get_engine()
    split_char = "\n" if split_char == "\\n" else split_char
    usernames = username.split(split_char)
    prepared_usernames = [f"'{username}'" for username in usernames]

    query = f"""select id from lyceum_class where id = {class_id}"""
    df = pd.read_sql(query, con=engine)
    print(format_table(df))

    if df[df.columns[0]].count() == 1:
        query = f"""select
                          u.id,
                          u.username
                        from
                          lyceum_appuser u
                        where
                          u.username in ({','.join(prepared_usernames)})"""
        df = pd.read_sql(query, con=get_engine())
        print(format_table(df))

        if (
            input(f"Are you sure you want to assign these users to the class? [y/N] ")[
                :1
            ].lower()
            == "y"
        ):

            user_ids = []

            for index, row in df.iterrows():
                user_id = row["id"]
                username = row["username"]

                user_ids.append(f"({class_id}, {user_id})")

            query = f"insert ignore into lyceum_class_students (class_id, appuser_id) values {','.join(user_ids)}"
            with engine.connect() as con:
                rs = con.execute(query)
