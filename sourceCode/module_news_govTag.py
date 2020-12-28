def tagGov(cursor, title, content):
    cursor.execute('SELECT * FROM ttd.gov_dept')
    gov_dept = cursor.fetchall()

    # Turn government department into dict
    ind_to_dept = {}
    dept_to_nick = {}
    for line in gov_dept:
        ind_to_dept[line[1]] = line[0]
        dept_to_nick[line[1]] = line[2].split(",")

    gov_tag = ''

    for nick in dept_to_nick:
        for name in dept_to_nick[nick]:
            if name in title or name in content:
                gov_tag += nick + ','
                break


    return gov_tag[:-1]