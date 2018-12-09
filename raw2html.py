#!/usr/bin/env python

# version 1
# simple implementation
# hardcode first


import sys
import os

if len(sys.argv) > 1:
    report_dir   = sys.argv[1]
else:
    report_dir   = "./report"

template_dir = os.path.dirname(sys.argv[0]) + "/template"

basic_raw    = report_dir + "/basic.raw"
library_raw  = report_dir + "/library.raw"
user_raw     = report_dir + "/user.raw"
system_raw   = report_dir + "/system.raw"

raw_html       = report_dir + "/raw.html"
bar_html       = report_dir + "/bar.html"
bar_block_html = report_dir + "/bar_block.html"
pie_uss_html   = report_dir + "/pie_uss.html"
pie_pss_html   = report_dir + "/pie_pss.html"
pie_rss_html   = report_dir + "/pie_rss.html"

raw_template       = template_dir + "/raw.template"
bar_template       = template_dir + "/bar.template"
bar_block_template = template_dir + "/bar_block.template"
pie_template       = template_dir + "/pie.template"

basic_raw_content   = open(basic_raw).read()
library_raw_content = open(library_raw).read()
user_raw_content    = open(user_raw).read()
system_raw_content  = open(system_raw).read()

debug = False

if debug:
    print "basic info"
    print basic_raw_content
    print "library info"
    print library_raw_content
    print "user info"
    print user_raw_content
    print "system info"
    print system_raw_content


# replace_strings = [("old", "new"), ...]
def make_html(template, output, replace_strings):
    template_content = open(template).read()
    for old, new in replace_strings:
        template_content = template_content.replace(old, new)
    open(output, 'w').write(template_content)


raw_report  = "#### all smem report\n"
raw_report += "\n#### process basic information\n"
raw_report += basic_raw_content
raw_report += "\n#### library information\n"
raw_report += library_raw_content
raw_report += "\n#### user information\n"
raw_report += user_raw_content
raw_report += "\n#### system information\n"
raw_report += system_raw_content

make_html(raw_template, raw_html, [("LABEL_SMEM", raw_report)])


cmd_string = ""
uss_string = ""
pss_string = ""
rss_string = ""
for line in open(basic_raw):
    if "PID" in line:
        continue
    if "----" in line:
        break
    line = line.replace(",", " ")
    fields = [s for s in line.strip().split(" ") if len(s) > 0]
    cmd = fields[0] + " : " + " ".join(fields[2:-4])
    uss = fields[-3]
    pss = fields[-2]
    rss = fields[-1]
    cmd_string += "'" + cmd + "',"
    uss_string += ""  + uss + ","
    pss_string += ""  + pss + ","
    rss_string += ""  + rss + ","

cmd_string = cmd_string[:-1]
uss_string = uss_string[:-1]
pss_string = pss_string[:-1]
rss_string = rss_string[:-1]

if debug:
    print cmd_string
    print uss_string
    print pss_string
    print rss_string


bar_replace_strings = [
    ("LABEL_xAxis_list", "[" + cmd_string + "]"),
    ("LABEL_USS_list", "[" + uss_string + "]"),
    ("LABEL_PSS_list", "[" + pss_string + "]"),
    ("LABEL_RSS_list", "[" + rss_string + "]")
]
make_html(bar_template, bar_html, bar_replace_strings)


def make_xss_data(cmd, xss):
    data = ""
    info = zip(xss.split(","), cmd.split(","))
    for value,name in info:
        data += "{value:" + value + ", name:" + name + "},"
    data = data[:-1]
    return "[" + data + "]"

xss_replace_strings = [
    ("LABEL_title", "process USS"),
    ("LABEL_legend_list", "[" + cmd_string + "]"),
    ("LABEL_data_list", make_xss_data(cmd_string, uss_string))
]
make_html(pie_template, pie_uss_html, xss_replace_strings)

xss_replace_strings = [
    ("LABEL_title", "process PSS"),
    ("LABEL_legend_list", "[" + cmd_string + "]"),
    ("LABEL_data_list", make_xss_data(cmd_string, pss_string))
]
make_html(pie_template, pie_pss_html, xss_replace_strings)

xss_replace_strings = [
    ("LABEL_title", "process RSS"),
    ("LABEL_legend_list", "[" + cmd_string + "]"),
    ("LABEL_data_list", make_xss_data(cmd_string, rss_string))
]
make_html(pie_template, pie_rss_html, xss_replace_strings)


bar_block_replace_strings = [
    ("LABEL_PROCESS_LIST", "[" + cmd_string + "]"),
    ("LABEL_USS_LIST", "[" + uss_string + "]"),
    ("LABEL_PSS_LIST", "[" + pss_string + "]"),
    ("LABEL_RSS_LIST", "[" + rss_string + "]")
]
make_html(bar_block_template, bar_block_html, bar_block_replace_strings)
