import post_crawler as pc
import os

feed_csv = "feed.csv"
out_dir = "output_without_masking"

csv = open(feed_csv)
count = 1

if out_dir not in os.listdir():
    os.mkdir(out_dir)

crawler = pc.crawler()

done_list = []
temp = os.listdir(out_dir)

for el in temp:
    if ".png" in el:
        done_list.append(el)

for line in csv:
    line_split = line.strip().split(",")
    if len(line_split) != 2:
        continue

    querry = line_split[0].strip()
    key2 = line_split[1].strip()
    if len(key2) < 2:
        continue
    key2 = key2[1]
    key1 = "구"
    if len(key2) != 1:
        continue

    if "-" in querry:
        splt = querry.split("-")
        querry = ""
        for el in splt:
            querry = querry + el

    if len(querry) != 13 or not querry.isdigit():
        continue

    if querry + ".png" in done_list:
        continue
    try:
        if not crawler.save_screenshot_withhout_masking(querry, out_dir, key1, key2):
            print(str(querry) + " has wrong information")
            out_log = "line was      " + line + "key2 was    " + key2 + "\n\n"
            print(out_log)
            error_log = open("errored_ids.txt", "a")
            error_log.write(out_log)
            error_log.close()
            continue
    except:
        print(str(querry) + " showed error")
        continue
    #print("JOB Number " + str(count) + " Done.\n>>>>>" + querry)
    count += 1

crawler.kill()
