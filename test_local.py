import re
import pandas as pd
from bs4 import BeautifulSoup

def test_local_html():
    with open("test_local.html", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    results_table = soup.select_one("table.tw-min-w-full.tw-divide-y.tw-divide-gray-300")
    if not results_table:
        print("[!] Could not find table in test_local.html")
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

        # For demonstration, parse date and decision from the main row
        date_posted = tds[2].get_text(strip=True)
        decision_text = tds[3].get_text(strip=True)

        # The next row might be a tag row with class="tw-border-none"
        tag_row = None
        if i + 1 < len(rows) and "tw-border-none" in rows[i+1].get("class", []):
            tag_row = rows[i+1]
            i += 2
        else:
            i += 1

        gre_total = ""
        gre_v = ""
        gre_aw = ""

        tags_text = []
        if tag_row:
            tag_tds = tag_row.select("td")
            if tag_tds:
                tag_divs = tag_tds[0].select("div.tw-inline-flex")
                for div in tag_divs:
                    txt = div.get_text(strip=True)
                    tags_text.append(txt)

        for tag_item in tags_text:
            lower_tag = tag_item.lower()

            # e.g. "GRE 324"
            match_total = re.search(r'\bgre\D*(\d+(\.\d+)?)\b', lower_tag)
            if match_total:
                gre_total = match_total.group(1)

            # e.g. "GRE V 156"
            match_v = re.search(r'\bgre\s+v\s+(\d+(\.\d+)?)\b', lower_tag)
            if match_v:
                gre_v = match_v.group(1)

            # e.g. "GRE AW 4.50"
            match_aw = re.search(r'\bgre\s+aw\s+(\d+(\.\d+)?)\b', lower_tag)
            if match_aw:
                gre_aw = match_aw.group(1)

        all_data.append({
            "Date_Posted": date_posted,
            "Decision_Text": decision_text,
            "GRE_Total": gre_total,
            "GRE_V": gre_v,
            "GRE_AW": gre_aw
        })

    df = pd.DataFrame(all_data)
    print(df)
    return df

if __name__ == "__main__":
    df_local = test_local_html()
    # Expect a row with GRE_Total=324, GRE_V=156, GRE_AW=4.50