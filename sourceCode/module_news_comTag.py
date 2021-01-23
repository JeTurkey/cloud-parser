def tagCom(cursor, title, content):
    cursor.execute('SELECT * FROM ttd.company')
    gov_dept = cursor.fetchall()

    # Turn government department into dict
    ind_to_dept = {}
    dept_to_nick = {}
    for line in gov_dept:
        ind_to_dept[line[1]] = line[0]
        dept_to_nick[line[1]] = line[2].split(",")

    com_tag = ''

    for nick in dept_to_nick:
        for name in dept_to_nick[str(nick)]:
            if str(name) in title or str(name) in content:
                com_tag += nick + ','
                break


    return com_tag[:-1]