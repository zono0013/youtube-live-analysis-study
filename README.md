# youtube-live-analysis-study
研究室の冬休み課題(統計)でデータの取得のために使用したYoutube Data APIのコードである

## 実装概要
以下の一連の動作を実装しています。
1. YouTube Data APIを使用して日本の完了したライブストリームを検索します。
2. 動画タイトル、チャンネル名、開始/終了時間、視聴回数などのメタデータを収集します。
3. 結果を日本語のコンテンツにフィルタリングし、ライブストリームの期間などの追加情報を計算します。
4. 結果をCSVファイルに保存し、さらに分析できるようにします。


## 環境設定 (Mac)

1.  仮想環境を作成する
```
python3 -m venv venv 
source venv/bin/activate
```

2.  ライブラリをインストールする
```
pip install google-api-python-client pandas
```

## 実行方法
```
python3 youtube_data.py
```

# 出力
スクリプトは `japanese_live_streams_filtered.csv` というファイルを生成します。内容は以下のようになります。
```
video_id,title,channel_name,published_at,description,start_time,end_time,view_count,duration_minutes
wc42Cek3BeM,【ライブ】命と未来をまもる ～能登半島地震から1年～　ライブBBTスペシャル,FNNプライムオンライン,2024-12-31 16:55:26+09:00,能登半島地震の発生から1年を前に大晦日の午後3時半から午後4時50分まで富山テレビは報道特別番組を放送します。 富山県内の ...,2024-12-31 15:16:46+09:00,2024-12-31 16:49:48+09:00,6926,93.03333333333333
J0rOLu4C2OI,【バイオ RE4】108発のロケランでクリアを目指す！【除夜のロケラン】,つなまぐろ,2025-01-01 00:29:43+09:00,【ルール】 主武器は無限ロケラン108発のみ。 手榴弾、閃光手榴弾、ナイフは使います！ 【LIVE中の注意事項】 ※改善されない ...,2024-12-31 20:57:46+09:00,2025-01-01 00:11:05+09:00,,32831,193.31666666666666
HSrNIWbMauE,【LIVE】朝のニュース（Japan News Digest Live）最新情報など｜TBS NEWS DIG（1月1日）,TBS NEWS DIG Powered by JNN,2025-01-01 11:13:24+09:00,1月1日（水）の早朝から TBS NEWS で放送された最新のニュースをダイジェストでお届けします。 ・今年の“ご来光”は静岡 ...,2025-01-01 06:06:11+09:00,2025-01-01 10:59:25+09:00,101504,293.23333333333335
b2tSaeUKo7I,【バイオハザード作品全部】時系列順にクリアするまで終われません!!2025【Resident Evil】＃８,コジマ店員のホラーは恐くない,2025-01-01 14:57:42+09:00,【次】→https://www.youtube.com/watch?v=3q_aypuRwvo 【2025年時系列バイオ ...,2025-01-01 09:00:11+09:00,2025-01-01 14:39:48+09:00,109584,339.6166666666667
tfk0k5-qt9I,【バイオハザード作品全部】時系列順にクリアするまで終われません!!2025【Resident Evil】＃６,コジマ店員のホラーは恐くない,2024-12-31 16:16:01+09:00,【次】→https://www.youtube.com/watch?v=zI-aH2EUMnI 【2025年時系列バイオ ...,2024-12-31 13:00:12+09:00,2024-12-31 16:06:22+09:00,84498,186.16666666666666
AQrsAq5F7wc,【ライブ】12/31 昼ニュースまとめ 最新情報を厳選してお届け,ANNnewsCH,2024-12-31 16:14:49+09:00,大晦日も帰省ラッシュ続く 全日空は下り混雑ピーク 大晦日に“年越しそば” 店では朝から大にぎわい 渋谷駅前「ハチ公」像を封鎖 ...,2024-12-31 10:29:20+09:00,2024-12-31 16:00:02+09:00,64254,330.7
iiFEPZqicJw,🔴2025年！年越し配信！【フォートナイト】【フォートナイト】【Fortnite】,ぜるふぃー / ZELLFY,2025-01-01 00:07:05+09:00,SNS ○Twitter @zellfyyyn https://twitter.com/zellfyyyn ○陰stagram @zellfyyyn https://www.instagram.com/zellfyyyn/ ▽関連 ...,2024-12-31 23:00:46+09:00,2025-01-01 00:01:20+09:00,40000,60.56666666666667
iRGuoy23ai4,🔴みんなで年越ししよう！明けましておめでとう！【フォートナイト】,LiaqN【りあん】,2025-01-01 00:22:35+09:00,サブチャンネル：https://www.youtube.com/channel/UCe7MlnaxzpUZve253jOXJoQ りあんの企画用ディスコードサーバー！,2024-12-31 21:46:23+09:00,2025-01-01 00:12:04+09:00,81826,145.68333333333334
z7_s-NEGA7g,【圧倒的に不評ゲーム再び】とんでもない低評価を受けている狩りゲーをやる【Dauntless】,からすまAチャンネル,2025-01-01 01:39:39+09:00,あーねんまつ どうも、クソ投稿者こと「からすま」です。 ーーーーーーーーーーーーーーーーーーーーーーーーーー 主に ...,2024-12-31 22:45:40+09:00,2025-01-01 01:28:40+09:00,66320,163.0
0ETT645BNLs,【年越し配信】The Outlast Trials 耐久ローグライトモード,あまり驚かないガッチマンはホラーゲームばかりやっている,2025-01-01 02:51:41+09:00,登録者200万人目前なので、久しぶりにメインチャンネルでの年越し配信 The Outlast Trialsの耐久ローグライトモードで年越し ...,2024-12-31 20:00:27+09:00,2025-01-01 02:29:45+09:00,183273,389.3
```

## 注意事項
`APIキー`：スクリプト内のプレースホルダー(youtube_data.py:164行目)に有効なYouTube Data APIキーを設定してください。

APIキーの取得手順については、下記のガイドに従ってください。
https://developers.google.com/youtube/v3/docs?hl=ja


