def tagTopic(cursor, title, content):
    cursor.execute('SELECT * FROM ttd.topic')
    gov_dept = cursor.fetchall()

    # Turn government department into dict
    ind_to_dept = {}
    dept_to_nick = {}
    for line in gov_dept:
        ind_to_dept[line[1]] = line[0]
        dept_to_nick[line[1]] = line[2].split(",")

    topic_tag = ''

    for nick in dept_to_nick:
        for name in dept_to_nick[str(nick)]:
            if str(name) in title or str(name) in content:
                topic_tag += nick + ','
                break


    return topic_tag[:-1]