# -*- coding: utf-8 -*-
"""jリーグ_スタッツランキング.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1D8VNG_Ku-tGqs_m8NZrvf5aI-MMt2Nk2
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# ───────────────────────────────────────────
# 1) 辞書類
# ───────────────────────────────────────────
season_dict = {
    "2025": "2025年シーズン",
    "2024": "2024年シーズン"
}

stat_type_dict = {
    "game": "出場試合数",
    "time": "出場時間",
    "shoot": "シュート総数",
    "shoot_per_game": "1試合平均シュート数",
    "shoot_on_target": "枠内シュート総数",
    "shoot_rate": "シュート決定率",
    "suffer_shoot": "被シュート総数",
    "suffer_shoot_on_target": "被枠内シュート総数",
    "score": "得点ランキング",
    "fk_score": "FK得点数",
    "pk_score": "PK得点数",
    "left_foot_score": "左足得点数",
    "right_foot_score": "右足得点数",
    "head_score": "ヘディング得点数",
    "other_type_score": "その他部位得点数",
    "expected_goals": "ゴール期待値",
    "expected_goals_excl_pk": "ゴール期待値（PK除く）",
    "expected_goals_diff": "得点数とゴール期待値の差分",
    "assist": "アシスト総数",
    "lost": "失点総数",
    "play_count": "プレー総数",
    "play_count_per_game": "1試合平均プレー数",
    "pass_count": "パス総数",
    "pass_count_per_game": "1試合平均パス数",
    "pass_rate": "パス成功率",
    "opponent_area_pass_count": "敵陣パス数",
    "opponent_area_pass_rate": "敵陣パス成功率",
    "opponent_area_pass_count_per_game": "1試合平均敵陣パス数",
    "own_area_pass_count": "自陣パス数",
    "own_area_pass_rate": "自陣パス成功率",
    "own_area_pass_count_per_game": "1試合平均自陣パス数",
    "long_pass_count": "ロングパス総数",
    "long_pass_rate": "ロングパス成功率",
    "long_pass_count_per_game": "1試合平均ロングパス数",
    "dribble_count": "ドリブル総数",
    "dribble_rate": "ドリブル成功率",
    "through_pass_count": "スルーパス総数",
    "through_pass_rate": "スルーパス成功率",
    "cross_count": "クロス総数",
    "cross_rate": "クロス成功率",
    "cross_count_per_game": "1試合平均クロス数",
    "clear_count": "クリア総数",
    "tackle_count": "タックル総数",
    "tackle_rate": "タックル成功率",
    "tackle_count_per_game": "1試合平均タックル数",
    "block_count": "ブロック総数",
    "intercept_count": "インターセプト総数",
    "intercept_count_per_game": "1試合平均インターセプト数",
    "air_battle_win_count": "空中戦勝利数",
    "air_battle_win_rate": "空中戦勝率",
    "foul_count": "ファウル総数",
    "suffer_foul_count": "被ファウル総数",
    "yellow_count": "警告数",
    "red_count": "退場数",
    "chance_create": "チャンスクリエイト総数",
    "chance_create_per_game": "1試合平均チャンスクリエイト数",
    "duels_won": "デュエル勝利総数",
    "recovery_count": "こぼれ球奪取総数",
    "fk": "FK総数",
    "ck": "CK総数",
    "save_count": "セーブ総数",
    "save_rate": "セーブ率",
    "save_count_per_game": "1試合平均セーブ数",
    "save_rate_in_pa": "PA内シュートセーブ率",
    "save_rate_out_pa": "PA外シュートセーブ率",
    "save_catch_rate_in_pa": "PA内シュートキャッチ率",
    "save_catch_rate_out_pa": "PA外シュートキャッチ率",
    "cross_catch_rate": "クロスキャッチ率",
    "save_punch_rate_in_pa": "PA内シュートパンチング率",
    "save_punch_rate_out_pa": "PA外シュートパンチング率",
    "cross_punch_rate": "クロスパンチング率",
    "clean_sheet": "クリーンシート総数",
    "distance": "総走行距離",
    "top_speed": "トップスピード",
    "sprint": "総スプリント回数",
    "at_sprint": "Atスプリント回数",
    "mt_sprint": "Mtスプリント回数",
    "dt_sprint": "Dtスプリント回数",
    "possession_distance": "ポゼッション時の走行距離",
    "possession_sprint": "ポゼッション時のスプリント回数"
}

club_dict_by_season_category = {
    "2024": {
        "j1": {
            "sapporo": "北海道コンサドーレ札幌", "kashima": "鹿島アントラーズ", "urawa": "浦和レッズ", "kashiwa": "柏レイソル",
            "ftokyo": "FC東京", "tokyov": "東京ヴェルディ", "machida": "FC町田ゼルビア", "kawasakif": "川崎フロンターレ",
            "yokohamafm": "横浜F・マリノス", "shonan": "湘南ベルマーレ", "niigata": "アルビレックス新潟", "iwata": "ジュビロ磐田",
            "nagoya": "名古屋グランパス", "kyoto": "京都サンガF.C.", "gosaka": "ガンバ大阪", "cosaka": "セレッソ大阪",
            "kobe": "ヴィッセル神戸", "hiroshima": "サンフレッチェ広島", "fukuoka": "アビスパ福岡", "tosu": "サガン鳥栖"
        },
        "j2": {
            "sendai": "ベガルタ仙台", "akita": "ブラウブリッツ秋田", "yamagata": "モンテディオ山形", "iwaki": "いわきFC",
            "mito": "水戸ホーリーホック", "tochigi": "栃木SC", "gunma": "ザスパ群馬", "chiba": "ジェフユナイテッド千葉",
            "yokohamafc": "横浜FC", "kofu": "ヴァンフォーレ甲府", "shimizu": "清水エスパルス", "fujieda": "藤枝MYFC",
            "okayama": "ファジアーノ岡山", "yamaguchi": "レノファ山口FC", "tokushima": "徳島ヴォルティス", "ehime": "愛媛FC",
            "nagasaki": "V・ファーレン長崎", "kumamoto": "ロアッソ熊本", "oita": "大分トリニータ", "kagoshima": "鹿児島ユナイテッドFC"
        },
        "j3": {
            "hachinohe": "ヴァンラーレ八戸", "morioka": "いわてグルージャ盛岡", "fukushima": "福島ユナイテッドFC", "omiya": "大宮アルディージャ",
            "yscc": "Y.S.C.C.横浜", "sagamihara": "SC相模原", "matsumoto": "松本山雅FC", "nagano": "AC長野パルセイロ",
            "toyama": "カターレ富山", "kanazawa": "ツエーゲン金沢", "numazu": "アスルクラロ沼津", "gifu": "FC岐阜",
            "fcosaka": "FC大阪", "nara": "奈良クラブ", "tottori": "ガイナーレ鳥取", "sanuki": "カマタマーレ讃岐",
            "imabari": "FC今治", "kitakyushu": "ギラヴァンツ北九州", "miyazaki": "テゲバジャーロ宮崎", "ryukyu": "FC琉球"
        }
    },
    "2025": {
        "j1": {
            "kashima": "鹿島アントラーズ", "kashiwa": "柏レイソル", "tokyov": "東京ヴェルディ", "kawasakif": "川崎フロンターレ",
            "yokohamafc": "横浜FC", "niigata": "アルビレックス新潟", "nagoya": "名古屋グランパス", "gosaka": "ガンバ大阪",
            "kobe": "ヴィッセル神戸", "hiroshima": "サンフレッチェ広島", "urawa": "浦和レッズ", "ftokyo": "FC東京",
            "machida": "FC町田ゼルビア", "yokohamafm": "横浜F・マリノス", "shonan": "湘南ベルマーレ", "shimizu": "清水エスパルス",
            "kyoto": "京都サンガF.C.", "cosaka": "セレッソ大阪", "okayama": "ファジアーノ岡山", "fukuoka": "アビスパ福岡"
        },
        "j2": {
            "sapporo": "北海道コンサドーレ札幌", "akita": "ブラウブリッツ秋田", "iwaki": "いわきFC", "omiya": "RB大宮アルディージャ",
            "kofu": "ヴァンフォーレ甲府", "iwata": "ジュビロ磐田", "yamaguchi": "レノファ山口FC", "ehime": "愛媛FC",
            "tosu": "サガン鳥栖", "kumamoto": "ロアッソ熊本", "sendai": "ベガルタ仙台", "yamagata": "モンテディオ山形",
            "mito": "水戸ホーリーホック", "chiba": "ジェフユナイテッド千葉", "toyama": "カターレ富山", "fujieda": "藤枝MYFC",
            "tokushima": "徳島ヴォルティス", "imabari": "FC今治", "nagasaki": "V・ファーレン長崎", "oita": "大分トリニータ"
        },
        "j3": {
            "hachinohe": "ヴァンラーレ八戸", "tochigi": "栃木SC", "gunma": "ザスパ群馬", "matsumoto": "松本山雅FC",
            "kanazawa": "ツエーゲン金沢", "gifu": "FC岐阜", "nara": "奈良クラブ", "sanuki": "カマタマーレ讃岐",
            "kitakyushu": "ギラヴァンツ北九州", "kagoshima": "鹿児島ユナイテッドFC", "fukushima": "福島ユナイテッドFC",
            "tochigicity": "栃木シティ", "sagamihara": "SC相模原", "nagano": "AC長野パルセイロ", "numazu": "アスルクラロ沼津",
            "fcosaka": "FC大阪", "tottori": "ガイナーレ鳥取", "kochi": "高知ユナイテッドSC", "miyazaki": "テゲバジャーロ宮崎",
            "ryukyu": "FC琉球"
        }
    }
}

# ───────────────────────────────────────────
# 2) オプション取得関数
# ───────────────────────────────────────────
def get_jleague_options(season: str, category: str):
    """
    season, category から season_dict・club_dict・stat_type_dict を返す
    """
    club_dict = {"all": "全クラブ"}
    club_dict.update(club_dict_by_season_category.get(season, {}).get(category, {}))
    return season_dict, club_dict, stat_type_dict

# ───────────────────────────────────────────
# 3) メインスクレイピング関数
# ───────────────────────────────────────────
def scrape_jleague_stats(
        season: str,
        stat_type: str,
        category: str = "j1",
        club: str = "all",
        sleep_sec: float = 1.0
    ) -> pd.DataFrame:
    """
    指定の 年・カテゴリ・指標（必須）とクラブ（任意）で DataFrame を返す
    club="all" の場合は該当カテゴリの全クラブをループ
    """

    base_clubs = club_dict_by_season_category.get(season, {}).get(category, {})
    if not base_clubs:
        raise ValueError(f"⛔ {season} の {category.upper()} は辞書未登録です。")

    # ------------- 全クラブモード -------------
    if club == "all":
        dfs = []
        for code, name in base_clubs.items():
            print(f"📥 {season}-{category.upper()} {stat_type} : {name}")
            try:
                dfs.append(
                    scrape_jleague_stats(season, stat_type, category, code, sleep_sec)
                )
            except Exception as e:
                print(f"⚠️ 失敗: {name} → {e}")
            time.sleep(sleep_sec)
        return pd.concat(dfs, ignore_index=True)

    # ------------- 単一クラブ -------------
    if club not in base_clubs:
        raise ValueError(f"⛔ {club} は {season}-{category.upper()} に存在しません。")

    url = f"https://www.jleague.jp/stats/{category}/player/{season}/{club}/{stat_type}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=30)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    data = []
    for li in soup.select("ul.ranking_list li"):
        rank = li.select_one("p[class^='number']")
        name = li.select_one("p.name")
        team = li.select_one("p.team")
        value = li.select_one("div[class^='ranking_stats'] p")

        # player_code
        a_tag = li.find("a", href=True)
        if a_tag and "/player/" in a_tag["href"]:
            player_code = a_tag["href"].strip("/").split("/")[-1]
        else:
            img = li.find("img", src=True)
            m = re.search(r"/player/(\d+)_s\.jpg", img["src"]) if img else None
            player_code = m.group(1) if m else None

        data.append({
            "season": season,
            "season_label": season_dict[season],
            "category": category,
            "club": club,
            "club_label": base_clubs[club],
            "stat_type": stat_type,
            "stat_label": stat_type_dict[stat_type],
            "rank": rank.text.strip() if rank else None,
            "name": name.text.strip() if name else None,
            "team": team.text.strip() if team else None,
            "value": value.text.strip() if value else None,
            "player_code": player_code
        })

    return pd.DataFrame(data)

import pandas as pd
from functools import reduce
import numpy as np
import re

# ──────────────────────────────
#   n 指標対応版コンボランキング
# ──────────────────────────────
def combo_ranking(
        season: str,
        stat_codes: list[str],          # 1 個以上なら自由
        category: str = "j1",
        club: str = "all",
        top: int | None = 20            # 表示・保存したい上位件数 (None なら全件)
    ) -> pd.DataFrame:
    """
    任意本数のスタッツを掛け合わせたランキングを返す
    ・score_prod = すべての指標の積
    戻り値: df_sorted
    """
    if len(stat_codes) == 0:
        raise ValueError("stat_codes を 1 つ以上指定してください。")

    # ------------- 各指標を取得してマージ -------------
    dfs = []
    for code in stat_codes:
        tmp = scrape_jleague_stats(season, code, category, club)[
            ["player_code", "name", "team", "value"]
        ].copy()

        # 数値化（%, カンマ除去）
        tmp[code] = (
            tmp["value"]
            .str.replace("%", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(float)
        )
        tmp.drop(columns="value", inplace=True)
        dfs.append(tmp)

    df = reduce(
        lambda left, right: pd.merge(left, right,
                                     on=["player_code", "name", "team"],
                                     how="inner"),
        dfs
    )

    # ------------- 積スコア計算 -------------
    df["score_prod"] = df[stat_codes].replace(np.nan, 0).prod(axis=1)

    # ------------- ソートして順位付け -------------
    df_sorted = (
        df.sort_values("score_prod", ascending=False)
          .reset_index(drop=True)
    )
    df_sorted.index += 1  # ランキング番号

    # ------------- 表示／保存 -------------
    if top is not None:
        display(df_sorted.head(top))

    fname = f"{season}_{category.upper()}_{'_'.join(stat_codes)}_ranking.csv"
    df_sorted.to_csv(fname, index_label="rank", encoding="utf-8-sig")
    print(f"✅ CSV saved: {fname}")

    return df_sorted

# 好きなだけ指標を並べて OK
my_stats = ["shoot_per_game", "shoot_rate", "air_battle_win_rate"]

df_rank = combo_ranking(
    season="2025",
    stat_codes=my_stats,
    category="j1",
    club="all",
    top=30           # 上位 30 人を表示
)

df_rank

# 既に df_rank と fname が作られている前提
df_rank.to_csv(fname, index=False, encoding='utf-8-sig')  # 元のファイル名のまま保存

# Colab 環境ならローカル（PC）へ即ダウンロード
from google.colab import files
files.download(fname)

