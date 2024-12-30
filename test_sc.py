import re
import pandas as pd
from bs4 import BeautifulSoup

def parse_local_html():
    with open("test_sc.html", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    
    # Identify the large table containing rows
    results_table = soup.select_one("table.tw-min-w-full.tw-divide-y.tw-divide-gray-300")
    if not results_table:
        print("[!] No main table found.")
        return
    
    rows = results_table.select("tbody tr")
    i = 0
    all_data = []

    while i < len(rows):
        main_row = rows[i]
        tds = main_row.select("td")
        if len(tds) < 4:
            i += 1
            continue

        # Example parse of some columns:
        school = tds[0].get_text(strip=True)
        program = tds[1].get_text(strip=True)
        date_posted = tds[2].get_text(strip=True)
        decision_text = tds[3].get_text(strip=True)

        # Check if the next row is the "tag row" with gre / gpa / etc.
        tag_row = None
        if i + 1 < len(rows) and "tw-border-none" in rows[i+1].get("class", []):
            tag_row = rows[i+1]
            i += 2
        else:
            i += 1

        # Prepare variables
        gre_total = ""
        gre_v = ""
        gre_aw = ""
        gpa = ""
        status_tags = []  # store raw text from each .tw-inline-flex

        if tag_row:
            tag_tds = tag_row.select("td")
            if tag_tds:
                # Each “tag” is in .tw-inline-flex
                tag_divs = tag_tds[0].select("div.tw-inline-flex")
                for div in tag_divs:
                    tag_text = div.get_text(strip=True)
                    status_tags.append(tag_text)

        # Now use regex or if-conditions to detect the different GRE patterns:
        # e.g. "GRE 324", "GRE V 156", "GRE AW 4.50", "GPA 3.07"
        for txt in status_tags:
            lower_txt = txt.lower()

            # e.g. "GRE 324"
            mt = re.search(r'\bgre\D*(\d+(\.\d+)?)\b', lower_txt)
            if mt:
                gre_total = mt.group(1)

            # e.g. "GRE V 156"
            mv = re.search(r'\bgre\s+v\s+(\d+(\.\d+)?)\b', lower_txt)
            if mv:
                gre_v = mv.group(1)

            # e.g. "GRE AW 4.50"
            maw = re.search(r'\bgre\s+aw\s+(\d+(\.\d+)?)\b', lower_txt)
            if maw:
                gre_aw = maw.group(1)

            # e.g. "GPA 3.07"
            mgpa = re.search(r'\bgpa\s+(\d+(\.\d+)?)\b', lower_txt)
            if mgpa:
                gpa = mgpa.group(1)

        all_data.append({
            "School": school,
            "Program": program,
            "Date_Posted": date_posted,
            "Decision_Text": decision_text,
            "GRE_Total": gre_total,
            "GRE_V": gre_v,
            "GRE_AW": gre_aw,
            "GPA": gpa,
            "Raw_Tags": status_tags  # optional debug
        })

    df = pd.DataFrame(all_data)
    print(df)
    return df

if __name__ == "__main__":
    df_local = parse_local_html()