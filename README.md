# jleague-scraper
Jリーグ選手名鑑とスタッツの自動収集・分析用リポジトリ

## 🔍 プロジェクト概要
本リポジトリは、Jリーグ各クラブの選手名鑑とスタッツデータを自動収集し、分析・ランキング作成を行うプロジェクトです。

## 🛠 使用技術
- Python 3.11
- Selenium / BeautifulSoup
- pandas / matplotlib
- GitHub

## 📁 ディレクトリ構成
```
jleague-scraper/
├── scraper.py
├── ranking.py
├── data/
│ └── kawasaki.csv
└── README.md
```

## 🧪 使い方（予定）
1. `scraper.py` を実行して選手データを収集
2. `ranking.py` を実行してスタッツランキング出力
3. 出力CSVは `data/` フォルダに保存される

## 🚀 今後の展望
- 全クラブ対応
- 複数指標の掛け合わせランキング
- 可視化や分析結果の発信（Colab連携）
