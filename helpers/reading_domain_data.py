#!/usr/bin/env python3
"""
阅读领域测试数据生成工具

生成30个知名作家和经典作品的组合，用于测试数据插入工具。
"""

READING_DOMAIN_DATA = [
    # 中国现当代作家
    ("鲁迅", "狂人日记", "lu_xun_kuang_ren_ri_ji"),
    ("鲁迅", "阿Q正传", "lu_xun_a_q_zheng_zhuan"),
    ("老舍", "茶馆", "lao_she_cha_guan"),
    ("老舍", "骆驼祥子", "lao_she_luo_tuo_xiang_zi"),
    ("钱钟书", "围城", "qian_zhong_shu_wei_cheng"),
    ("沈从文", "边城", "shen_cong_wen_bian_cheng"),
    ("张爱玲", "倾城之恋", "zhang_ai_ling_qing_cheng_zhi_lian"),
    ("莫言", "红高粱家族", "mo_yan_hong_gao_liang_jia_zu"),
    ("余华", "活着", "yu_hua_huo_zhe"),
    ("路遥", "平凡的世界", "lu_yao_ping_fan_de_shi_jie"),
    
    # 国际经典作家
    ("列夫·托尔斯泰", "战争与和平", "lev_tolstoy_war_and_peace"),
    ("陀思妥耶夫斯基", "罪与罚", "dostoevsky_crime_and_punishment"),
    ("海明威", "老人与海", "hemingway_the_old_man_and_the_sea"),
    ("乔治·奥威尔", "1984", "george_orwell_1984"),
    ("J.K.罗琳", "哈利·波特与魔法石", "jk_rowling_harry_potter"),
    ("村上春树", "挪威的森林", "murakami_norwegian_wood"),
    ("东野圭吾", "解忧杂货店", "higashino_naoya_miracles"),
    ("马尔克斯", "百年孤独", "marquez_one_hundred_years"),
    ("雨果", "悲惨世界", "hugo_les_miserables"),
    ("简·奥斯汀", "傲慢与偏见", "austen_pride_and_prejudice"),
    
    # 古典文学作家
    ("曹雪芹", "红楼梦", "cao_xue_qin_dream_of_red_mansions"),
    ("施耐庵", "水浒传", "shi_nai_an_water_margin"),
    ("罗贯中", "三国演义", "luo_guan_zhong_romance_of_three_kingdoms"),
    ("吴承恩", "西游记", "wu_cheng_en_journey_to_the_west"),
    ("莎士比亚", "哈姆雷特", "shakespeare_hamlet"),
    ("但丁", "神曲", "dante_divine_comedy"),
    
    # 特殊字符和边界情况测试
    ("O'Henry", "The Gift of the Magi", "o_henry_gift_of_magi"),
    ("José Saramago", "Blindness", "jose_saramago_blindness"),
    ("François Rabelais", "Gargantua and Pantagruel", "rabelais_gargantua"),
    ("Émile Zola", "Germinal", "emile_zola_germinal")
]

def generate_csv_data():
    """生成CSV格式的测试数据"""
    csv_lines = []
    for author, book_title, slot_rename in READING_DOMAIN_DATA:
        csv_lines.append(f'"{author}","{slot_rename}","string"')
    return csv_lines

def generate_tsv_data():
    """生成TSV格式的测试数据"""
    tsv_lines = []
    for author, book_title, slot_rename in READING_DOMAIN_DATA:
        tsv_lines.append(f'{author}\t{slot_rename}\tstring')
    return tsv_lines

if __name__ == "__main__":
    print("CSV格式数据:")
    for line in generate_csv_data():
        print(line)
    
    print("\nTSV格式数据:")
    for line in generate_tsv_data():
        print(line)