with open('urls_label.txt','r') as f:
    lines = f.readlines()
    f.close()
    list_zgd = []
    print len(lines)
    for line in lines:
        line = line.strip()
        if 'http://d.amigo' in line:
            list_zgd.append(line)


print len(list_zgd)

with open('firmwareurl_amigo_label.txt', 'w') as f1:
    no_strip_list = []
    for line in list_zgd:
        if line not in no_strip_list:
            f1.write(line.strip())
            f1.write('\n')
    f1.close()

