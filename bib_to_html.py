# Get the name of the .bib file from user
bib_file = input("Welcome to the Bib to HTML Converter!\nPlease enter the name of the .bib file you want to convert:\n")
bib_file = bib_file.strip().split(".bib")[0]

# Create an empty html file
fhand_html = open(bib_file + ".html", "w")
fhand_html.write("")
fhand_html.close()

fhand_bib = open(bib_file + ".bib", "r")
fhand_html = open(bib_file + ".html", "r+")

item_list = fhand_bib.read().split("@")  # Store each item in the .bib file inside a list
item_list = [i.strip() for i in item_list]
item_list.pop(0)

# Remove empty lines from each of the items in the .bib file
no_emptyline_list = []
for item in item_list:
    emptylines_deleted_str = ""
    all_lines_list = item.split("\n")
    for line in all_lines_list:
        line = line.strip()
        if line != "":
            emptylines_deleted_str = emptylines_deleted_str + line + "\n"
    emptylines_deleted_str = emptylines_deleted_str[:-1]
    no_emptyline_list.append(emptylines_deleted_str)

# Check if a unique key which consists of alphanumeric characters exist in the specified item
def uniqkey_exists(item):
    try:
        item_lines = item.split("\n")
        uniqkey_list = item_lines[0].split("{")
        uniqkey = uniqkey_list[1].rstrip(",")
        if uniqkey.isalnum():
            return uniqkey
        else:
            return False
    except:
        return False


for i in no_emptyline_list:
    if uniqkey_exists(i) == False:
        fhand_html.write("Input file in.bib is not a valid .bib file!")
        fhand_html.close()
        fhand_bib.close()
        break

uniqkey_dict = {}
for i in no_emptyline_list:
    uniqkey_dict[uniqkey_exists(i)] = uniqkey_dict.get(uniqkey_exists(i), 0) + 1

uniqkey_count_list = []
for i in uniqkey_dict.values():
    uniqkey_count_list.append(i)

for i in uniqkey_count_list:
    try:
        if i != 1:  # There should be no more than one unique key in each item
            fhand_html.write("Input file in.bib is not a valid .bib file!")
            fhand_html.close()
            fhand_bib.close()
            break
    except:
        break

# Chech if there is a comma after each field except the last field of that item
def isthere_comma(item):
    item_lines = item.split("\n")
    for i in range(len(item_lines)):
        if i == len(item_lines) - 1:
            if item_lines[i][-1] != "}":
                return False
        elif i == len(item_lines) - 2:
            continue
        elif item_lines[i][-1] != ",":
            return False
    return True


for i in no_emptyline_list:
    try:
        if isthere_comma(i) == False:
            fhand_html.write("Input file in.bib is not a valid .bib file!")
            fhand_html.close()
            fhand_bib.close()
            break
    except:
        break

# Check if the Fieldcontent is enclosed in "" or {}
def fieldcontent_enclosed(item):
    try:
        fieldcontent_list = []
        item_lines = item.split("\n")
        for i in range(len(item_lines)):
            if i == 0 or i == len(item_lines) - 1:
                continue
            else:
                try:
                    try:
                        split_fromleft = item_lines[i].split("{")
                        split_fromrigth = split_fromleft[1].split("}")
                        split_fromrigth_str = split_fromrigth[0].strip()
                        if split_fromrigth_str != "":
                            fieldcontent_list.append(split_fromrigth_str)
                        else:
                            return False
                    except:
                        split_fromleft = item_lines[i].split("\"")
                        split_fromleft_str = split_fromleft[1].strip()
                        if split_fromleft_str != "":
                            fieldcontent_list.append(split_fromleft_str)
                        else:
                            return False
                except:
                    return False
        return fieldcontent_list
    except:
        return False


for i in no_emptyline_list:
    try:
        if fieldcontent_enclosed(i) == False:
            fhand_html.write("Input file in.bib is not a valid .bib file!")
            fhand_html.close()
            fhand_bib.close()
            break
    except:
        break


def fieldname_lowercase(item):
    item_lines = item.split("\n")
    for i in range(len(item_lines)):
        if i == 0 or i == len(item_lines) - 1:
            continue
        else:
            if ord(item_lines[i][0]) not in range(ord("a"), ord("z") + 1):
                return False
    return True


for i in no_emptyline_list:
    try:
        if fieldname_lowercase(i) == False:
            fhand_html.write("Input file in.bib is not a valid .bib file!")
            fhand_html.close()
            fhand_bib.close()
            break
    except:
        break

has_to_contain = ["author", "title", "journal", "year", "volume"]
for i in has_to_contain:
    for k in no_emptyline_list:
        try:
            if i not in k:
                fhand_html.write("Input file in.bib is not a valid .bib file!")
                fhand_html.close()
                fhand_bib.close()
                break
        except:
            break

# Function for getting the information contained in a specified fieldcontent
def fieldcontent_extractor(line):
    try:
        try:
            stripfrom_left = line.split("{")
            stripfrom_right = stripfrom_left[1].split("}")
            return stripfrom_right[0].strip()
        except:
            stripfrom_left = line.split("\"")
            return stripfrom_left[1].strip()
    except:
        return False


all_names = []
for i in no_emptyline_list:
    item_lines = i.split("\n")
    for k in item_lines:
        if k.startswith("author"):
            try:
                tmp1 = fieldcontent_extractor(k).split(" and ")
                for m in tmp1:
                    tmp2 = m.split(",")
                    for n in tmp2:
                        all_names.append(n.strip())
            except:
                try:
                    fhand_html.write("Input file in.bib is not a valid .bib file!")
                    fhand_html.close()
                    fhand_bib.close()
                    break
                except:
                    break

# Store all author names from every item inside a list
for i in all_names:
    for m in i:
        if not (m.isalpha() or m == " " or m == "."):
            try:
                fhand_html.write("Input file in.bib is not a valid .bib file!")
                fhand_html.close()
                fhand_bib.close()
                break
            except:
                break

# Check whether the author field in the .bib file is in correct format
for i in no_emptyline_list:
    item_lines = i.split("\n")
    for k in item_lines:
        if k.startswith("title"):
            try:
                tmp3 = fieldcontent_extractor(k)
                for j in tmp3:
                    if not (j.isalnum() or (j in [" ", ",", ".", "_", "-", "*", "=", ":"])):
                        try:
                            fhand_html.write("Input file in.bib is not a valid .bib file!")
                            fhand_html.close()
                            fhand_bib.close()
                            break
                        except:
                            break
            except:
                try:
                    fhand_html.write("Input file in.bib is not a valid .bib file!")
                    fhand_html.close()
                    fhand_bib.close()
                    break
                except:
                    break

# Check whether the journal field in the .bib file is in correct format
for i in no_emptyline_list:
    item_lines = i.split("\n")  # i variable contains a different item block with each for iteration
    for k in item_lines:
        if k.startswith("journal"):
            try:
                tmp4 = fieldcontent_extractor(k)
                for j in tmp4:
                    if not (j.isalnum() or (j in [" ", ",", ".", "_"])):
                        try:
                            fhand_html.write("Input file in.bib is not a valid .bib file!")
                            fhand_html.close()
                            fhand_bib.close()
                            break
                        except:
                            break
            except:
                try:
                    fhand_html.write("Input file in.bib is not a valid .bib file!")
                    fhand_html.close()
                    fhand_bib.close()
                    break
                except:
                    break

# Check whether the year field in the .bib file is in correct format
for i in no_emptyline_list:
    item_lines = i.split("\n")
    for k in item_lines:
        if k.startswith("year"):
            try:
                tmp5 = fieldcontent_extractor(k)
                if not 1000 <= int(tmp5) <3000:
                    try:
                        fhand_html.write("Input file in.bib is not a valid .bib file!")
                        fhand_html.close()
                        fhand_bib.close()
                        break
                    except:
                        break
            except:
                try:
                    fhand_html.write("Input file in.bib is not a valid .bib file!")
                    fhand_html.close()
                    fhand_bib.close()
                    break
                except:
                    break

# Check whether the volume field in the .bib file is in correct format
for i in no_emptyline_list:
    item_lines = i.split("\n")
    for k in item_lines:
        if k.startswith("volume"):
            try:
                tmp6 = fieldcontent_extractor(k)
                if not int(tmp6) > 0:
                    try:
                        fhand_html.write("Input file in.bib is not a valid .bib file!")
                        fhand_html.close()
                        fhand_bib.close()
                        break
                    except:
                        break
            except:
                try:
                    fhand_html.write("Input file in.bib is not a valid .bib file!")
                    fhand_html.close()
                    fhand_bib.close()
                    break
                except:
                    break

# Check whether the number field in the .bib file is in correct format
for i in no_emptyline_list:
    if "number" in i:
        item_lines = i.split("\n")
        for k in item_lines:
            if k.startswith("number"):
                try:
                    tmp7 = fieldcontent_extractor(k)
                    if not int(tmp7) > 0:
                        try:
                            fhand_html.write("Input file in.bib is not a valid .bib file!")
                            fhand_html.close()
                            fhand_bib.close()
                            break
                        except:
                            break
                except:
                    try:
                        fhand_html.write("Input file in.bib is not a valid .bib file!")
                        fhand_html.close()
                        fhand_bib.close()
                        break
                    except:
                        break

# Check whether the pages field in the .bib file is in correct format
for i in no_emptyline_list:
    if "pages" in i:
        item_lines = i.split("\n")
        for k in item_lines:
            if k.startswith("pages"):
                try:
                    tmp8 = fieldcontent_extractor(k).split("--")
                    for j in tmp8:
                        try:
                            if not 0 < int(j):
                                try:
                                    fhand_html.write("Input file in.bib is not a valid .bib file!")
                                    fhand_html.close()
                                    fhand_bib.close()
                                    break
                                except:
                                    break
                        except:
                            try:
                                fhand_html.write("Input file in.bib is not a valid .bib file!")
                                fhand_html.close()
                                fhand_bib.close()
                                break
                            except:
                                break
                except:
                    try:
                        fhand_html.write("Input file in.bib is not a valid .bib file!")
                        fhand_html.close()
                        fhand_bib.close()
                        break
                    except:
                        break

# Check whether the doi field in the .bib file is in correct format
for i in no_emptyline_list:
    if "doi" in i:
        item_lines = i.split("\n")
        for k in item_lines:
            if k.startswith("doi"):
                try:
                    tmp9 = fieldcontent_extractor(k).split("/")
                    for j in tmp9:
                        for m in j:
                            if not (m.isalnum() or m == "."):
                                try:
                                    fhand_html.write("Input file in.bib is not a valid .bib file!")
                                    fhand_html.close()
                                    fhand_bib.close()
                                    break
                                except:
                                    break
                except:
                    try:
                        fhand_html.write("Input file in.bib is not a valid .bib file!")
                        fhand_html.close()
                        fhand_bib.close()
                        break
                    except:
                        break

# Start writing the html file
try:
    fhand_html.write("<html>\n")
    fhand_html.flush()

    items_accordingtoyear_dict = {}
    for i in no_emptyline_list:
        item_lines = i.split("\n")
        for k in item_lines:
            if k.startswith("year"):
                items_accordingtoyear_dict[i] = fieldcontent_extractor(k)

    tmp_lst = []
    for key, value in items_accordingtoyear_dict.items():
        tmp_lst.append((value, key))

    tmp_lst.sort()
    items_sortedby_year = {}
    for value, key in tmp_lst[::-1]:
        items_sortedby_year[key] = value

    year = None
    title_item_dict = {}
    title_sorted_dict = {}
    count1 = 0
    for i in items_sortedby_year:
        count1 += 1

    count2 = 0
    for key, value in items_sortedby_year.items():
        count2 += 1
        if year is None:
            year = value
        if value == year:
            item_lines = key.split("\n")
            for j in item_lines:
                if j.startswith("title"):
                    title = fieldcontent_extractor(j)
                    title_item_dict[title] = key
            if count2 == count1:
                tmp_lst2 = []
                for k, v in title_item_dict.items():
                    tmp_lst2.append((k, v))
                tmp_lst2.sort()
                for k, v in tmp_lst2:
                    title_sorted_dict[v] = year
        else:
            tmp_lst3 = []
            for k, v in title_item_dict.items():
                tmp_lst3.append((k, v))
            tmp_lst3.sort()
            for k, v in tmp_lst3:
                title_sorted_dict[v] = year
            year = value
            title_item_dict = {}
            item_lines = key.split("\n")
            for j in item_lines:
                if j.startswith("title"):
                    title = fieldcontent_extractor(j)
                    title_item_dict[title] = key
            if count2 == count1:
                tmp_lst4 = []
                for k, v in title_item_dict.items():
                    tmp_lst4.append((k, v))
                tmp_lst4.sort()
                for k, v in tmp_lst4:
                    title_sorted_dict[v] = year

    years_list = []
    for i in title_sorted_dict.values():
        years_list.append(i)

    unique_years = []
    for i in years_list:
        if i not in unique_years:
            unique_years.append(i)

    only_sorted_items = []
    for key in title_sorted_dict:
        only_sorted_items.append(key)

    j_count = 0
    for i in unique_years:
        fhand_html.write("<br> <center> <b> " + i + " </b> </center>\n")
        fhand_html.flush()
        for j in range(len(years_list)):
            if years_list[j] == i:
                j_count += 1
                fhand_html.write("<br>\n[J" + str(len(years_list) - j_count + 1) + "] ")
                fhand_html.flush()
                item_lines = only_sorted_items[j_count - 1].split("\n")
                for m in item_lines:
                    if m.startswith("author"):
                        author_lastname_first = fieldcontent_extractor(m).split(" and ")
                        for n in range(len(author_lastname_first)):
                            author_firstname_first = author_lastname_first[n].split(",")
                            author_string = author_firstname_first[1].strip() + " " + author_firstname_first[0].strip()
                            if len(author_lastname_first) == 1:
                                fhand_html.write(author_string + ", <b>")
                                fhand_html.flush()
                            else:
                                if n == len(author_lastname_first) - 1:
                                    fhand_html.write(" and " + author_string + ", <b>")
                                    fhand_html.flush()
                                if n == len(author_lastname_first) - 2:
                                    fhand_html.write(author_string)
                                    fhand_html.flush()
                                if (n != len(author_lastname_first) - 1) and (n != len(author_lastname_first) - 2):
                                    fhand_html.write(author_string + ", ")
                                    fhand_html.flush()
                for m in item_lines:
                    if m.startswith("title"):
                        fhand_html.write(str(fieldcontent_extractor(m)) + "</b>, <i>")
                        fhand_html.flush()
                for m in item_lines:
                    if m.startswith("journal"):
                        fhand_html.write(str(fieldcontent_extractor(m)) + "</i>, ")
                        fhand_html.flush()
                for m in item_lines:
                    if m.startswith("volume"):
                        fhand_html.write(str(fieldcontent_extractor(m)))
                        fhand_html.flush()
                for m in item_lines:
                    if m.startswith("number"):
                        fhand_html.write(":" + str(fieldcontent_extractor(m)))
                        fhand_html.flush()
                for m in item_lines:
                    if m.startswith("pages"):
                        pages_single_dash = fieldcontent_extractor(m).split("--")
                        fhand_html.write(", pp. " + str(pages_single_dash[0]) + "-" + str(pages_single_dash[1]) + ", ")
                        fhand_html.flush()
                for m in item_lines:
                    if m.startswith("year"):
                        fhand_html.write(str(fieldcontent_extractor(m)) + ". ")
                        fhand_html.flush()
                for m in item_lines:
                    if m.startswith("doi"):
                        fhand_html.write("<a href=\"https://doi.org/" + str(fieldcontent_extractor(m)) + "\">link</a> ")
                        fhand_html.flush()
                fhand_html.write("<br>\n")
                fhand_html.flush()

    fhand_html.write("</html>")
    fhand_html.close()
    print("Conversion completed.")
except:
    try:
        fhand_html.write("Input file in.bib is not a valid .bib file!")
        fhand_html.close()
        fhand_bib.close()
    except:
        pass
