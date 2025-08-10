#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from typing import List, Dict, Optional, Tuple


def root_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def move_file(src_rel: str, dest_rel_dir: str, rename_to: Optional[str] = None) -> Tuple[str, str]:
    src_abs = os.path.join(root_dir(), src_rel)
    dest_dir_abs = os.path.join(root_dir(), dest_rel_dir)
    ensure_dir(dest_dir_abs)

    if not os.path.exists(src_abs):
        raise FileNotFoundError(f"Source not found: {src_rel}")

    base_name = rename_to if rename_to else os.path.basename(src_abs)
    dest_abs = os.path.join(dest_dir_abs, base_name)

    # If destination exists and rename is not explicitly given, add numeric suffix
    if os.path.exists(dest_abs) and rename_to is None:
        name, ext = os.path.splitext(base_name)
        counter = 2
        while True:
            candidate = f"{name}_{counter}{ext}"
            candidate_abs = os.path.join(dest_dir_abs, candidate)
            if not os.path.exists(candidate_abs):
                dest_abs = candidate_abs
                break
            counter += 1

    shutil.move(src_abs, dest_abs)
    return (src_rel, os.path.relpath(dest_abs, root_dir()))


def main() -> None:
    # Mapping: (source_relative_path, destination_relative_dir, optional_new_filename)
    mappings: List[Tuple[str, str, Optional[str]]] = [
        # 1_考え方/キャリア・専門職 → 01/キャリア設計・専門職, 05/設計原則
        ("1_考え方/キャリア・専門職/エンジニア7つの大罪.JPG", "01_ライフ・自己成長/キャリア設計・専門職", None),
        ("1_考え方/キャリア・専門職/得意なことの例100リスト_1.JPG", "01_ライフ・自己成長/自己理解・アイデンティティ", None),
        ("1_考え方/キャリア・専門職/得意なことの例100リスト_2.JPG", "01_ライフ・自己成長/自己理解・アイデンティティ", None),
        ("1_考え方/キャリア・専門職/得意なことの例100リスト_3.JPG", "01_ライフ・自己成長/自己理解・アイデンティティ", None),
        ("1_考え方/キャリア・専門職/得意なことの例100リスト_4.JPG", "01_ライフ・自己成長/自己理解・アイデンティティ", None),
        ("1_考え方/キャリア・専門職/設計の心構え.JPG", "05_プロダクト・戦略・設計/設計原則・アーキテクチャ", None),

        # 1_考え方/コミュニケーション・人間関係 → 02
        ("1_考え方/コミュニケーション・人間関係/人の言葉に傷つく必要なんてない.JPG", "02_対人スキル・コミュニケーション/コミュニケーション基礎", None),
        ("1_考え方/コミュニケーション・人間関係/仕事がうまくいくコミュニケーション.JPG", "02_対人スキル・コミュニケーション/コミュニケーション基礎", None),
        ("1_考え方/コミュニケーション・人間関係/声かけ変換表.jpeg", "02_対人スキル・コミュニケーション/言い換え・声かけ", None),
        ("1_考え方/コミュニケーション・人間関係/平等と公平.JPG", "02_対人スキル・コミュニケーション/公平性・倫理", None),
        ("1_考え方/コミュニケーション・人間関係/心理的安全性をつくる4つの因子.JPG", "02_対人スキル・コミュニケーション/心理的安全性・信頼", None),
        ("1_考え方/コミュニケーション・人間関係/言い換え言葉.jpeg", "02_対人スキル・コミュニケーション/言い換え・声かけ", None),
        ("1_考え方/コミュニケーション・人間関係/部下をやる気にさせる.jpeg", "02_対人スキル・コミュニケーション/マネジメント・部下育成", None),
        ("1_考え方/コミュニケーション・人間関係/関係の質の深まり.JPG", "02_対人スキル・コミュニケーション/心理的安全性・信頼", None),

        # 1_考え方/マインドセット・考え方 → 01/08/03
        ("1_考え方/マインドセット・考え方/できることとできないことの間.JPG", "01_ライフ・自己成長/マインドセット", None),
        ("1_考え方/マインドセット・考え方/ものさし.jpeg", "01_ライフ・自己成長/マインドセット", None),
        ("1_考え方/マインドセット・考え方/人生が変わる覚えておきたい数字.JPG", "08_データ・統計/数の感覚・指標", None),
        ("1_考え方/マインドセット・考え方/心が軽くなる考え方.JPG", "01_ライフ・自己成長/マインドセット", None),
        ("1_考え方/マインドセット・考え方/知らない世界を否定しない.JPG", "01_ライフ・自己成長/人生観・価値観", None),
        ("1_考え方/マインドセット・考え方/自信と理解度の相関.JPG", "03_仕事術・学習法/学習手順・学習定着", None),

        # 1_考え方/仕事術・スキルアップ → 03/05
        ("1_考え方/仕事術・スキルアップ/リスクのマンダラ化.JPG", "03_仕事術・学習法/思考法・フレームワーク", None),
        ("1_考え方/仕事術・スキルアップ/仕事ができる人の見方.JPG", "03_仕事術・学習法/仕事の進め方・可視化", None),
        ("1_考え方/仕事術・スキルアップ/仕事するときにみるやつ.JPG", "03_仕事術・学習法/仕事の進め方・可視化", None),
        ("1_考え方/仕事術・スキルアップ/戦略の階層.JPG", "05_プロダクト・戦略・設計/戦略の階層・意思決定", None),
        ("1_考え方/仕事術・スキルアップ/教え方が上手い人は何をしているか.JPG", "03_仕事術・学習法/教え方・ナレッジ共有", None),
        ("1_考え方/仕事術・スキルアップ/新しいことを学ぶ手順.JPG", "03_仕事術・学習法/学習手順・学習定着", None),
        ("1_考え方/仕事術・スキルアップ/理解の循環.JPG", "03_仕事術・学習法/学習手順・学習定着", None),
        ("1_考え方/仕事術・スキルアップ/要領良い人の特徴.jpeg", "03_仕事術・学習法/仕事の進め方・可視化", None),

        # 1_考え方/自己成長・人生観 → 01
        ("1_考え方/自己成長・人生観/生きがいの図.PNG", "01_ライフ・自己成長/人生観・価値観", None),
        ("1_考え方/自己成長・人生観/生き方.JPG", "01_ライフ・自己成長/人生観・価値観", None),
        ("1_考え方/自己成長・人生観/自分の上位互換.JPG", "01_ライフ・自己成長/自己理解・アイデンティティ", None),
        ("1_考え方/自己成長・人生観/自分らしさの図.JPG", "01_ライフ・自己成長/自己理解・アイデンティティ", None),

        # 2_IT業界 → 04/05/06/07/01
        ("2_IT業界/2022_副業系サービスカオスマップ.JPG", "04_ビジネス・マーケティング/市場・業界マップ・カオス", None),
        ("2_IT業界/NoCodeのカオスマップ.JPG", "04_ビジネス・マーケティング/市場・業界マップ・カオス", None),
        ("2_IT業界/Web制作で必要な技術.jpg", "06_ソフトウェア開発（基礎知識）/Web基礎（HTML/CSS/HTTP）", None),
        ("2_IT業界/エンジニアの評価されるエンジニア.JPG", "01_ライフ・自己成長/キャリア設計・専門職", None),
        ("2_IT業界/エンジニア知識体系図.pdf", "06_ソフトウェア開発（基礎知識）", None),
        ("2_IT業界/カタカナビジネス用語.JPG", "04_ビジネス・マーケティング/ビジネス用語・概念整理", None),
        ("2_IT業界/この歩兵ってのと横に動かせば.JPG", "05_プロダクト・戦略・設計/戦略の階層・意思決定", None),
        ("2_IT業界/プロダクト開発の手順.jpg", "05_プロダクト・戦略・設計/プロダクト思考・ユーザー価値", None),
        ("2_IT業界/使われるプロダクトを考える_1.JPG", "05_プロダクト・戦略・設計/プロダクト思考・ユーザー価値", None),
        ("2_IT業界/使われるプロダクトを考える_2.JPG", "05_プロダクト・戦略・設計/プロダクト思考・ユーザー価値", None),
        ("2_IT業界/使われるプロダクトを考える_3.JPG", "05_プロダクト・戦略・設計/プロダクト思考・ユーザー価値", None),
        ("2_IT業界/使われるプロダクトを考える_4.JPG", "05_プロダクト・戦略・設計/プロダクト思考・ユーザー価値", None),

        # 3_IT学習 → 06/05/07/10/09/03/04/02/01/05/08
        ("3_IT学習/0&null&undefinedの例え.JPG", "06_ソフトウェア開発（基礎知識）/JavaScript基礎（非同期・配列関数）", None),
        ("3_IT学習/Amazonで使いたい機能.jpeg", "05_プロダクト・戦略・設計/プロダクト思考・ユーザー価値", None),
        ("3_IT学習/asynchronous_js.JPG", "06_ソフトウェア開発（基礎知識）/JavaScript基礎（非同期・配列関数）", None),
        ("3_IT学習/ChatGPTの質問文47.pdf", "10_学習資料・チートシート/質問テンプレート・プロンプト", None),
        ("3_IT学習/Cloud Comparison.JPG", "07_IT基礎・インフラ/クラウド比較", None),
        ("3_IT学習/DXとは.JPG", "07_IT基礎・インフラ/IT概論・DX", None),
        ("3_IT学習/Figmaだけで出来る文字デザイン_1.JPG", "09_ツール・操作ガイド/Figma", None),
        ("3_IT学習/Figmaだけで出来る文字デザイン_2.JPG", "09_ツール・操作ガイド/Figma", None),
        ("3_IT学習/Figmaだけで出来る文字デザイン_3.JPG", "09_ツール・操作ガイド/Figma", None),
        ("3_IT学習/Figmaだけで出来る文字デザイン_4.JPG", "09_ツール・操作ガイド/Figma", None),
        ("3_IT学習/flexbox-cheatsheet.pdf", "10_学習資料・チートシート/チートシート各種（Flexbox等）", None),
        ("3_IT学習/Git/gitの図解_0.JPG", "06_ソフトウェア開発（基礎知識）/Git・バージョン管理", None),
        ("3_IT学習/Git/gitの図解_1.JPG", "06_ソフトウェア開発（基礎知識）/Git・バージョン管理", None),
        ("3_IT学習/Git/gitの図解_2.JPG", "06_ソフトウェア開発（基礎知識）/Git・バージョン管理", None),
        ("3_IT学習/Git/gitの図解_3.JPG", "06_ソフトウェア開発（基礎知識）/Git・バージョン管理", None),
        ("3_IT学習/Git/gitの図解_4.JPG", "06_ソフトウェア開発（基礎知識）/Git・バージョン管理", None),
        ("3_IT学習/Git/ちづみさんのGit図解/Git 用語図解_1.jpeg", "06_ソフトウェア開発（基礎知識）/Git・バージョン管理", None),
        ("3_IT学習/Git/ちづみさんのGit図解/Git 用語図解_2.jpeg", "06_ソフトウェア開発（基礎知識）/Git・バージョン管理", None),
        ("3_IT学習/Git/ちづみさんのGit図解/Git 用語図解_3.jpeg", "06_ソフトウェア開発（基礎知識）/Git・バージョン管理", None),
        ("3_IT学習/Git/ちづみさんのGit図解/Git 用語図解_4.jpeg", "06_ソフトウェア開発（基礎知識）/Git・バージョン管理", None),
        ("3_IT学習/hrefの分解.JPG", "06_ソフトウェア開発（基礎知識）/Web基礎（HTML/CSS/HTTP）", None),
        ("3_IT学習/jsの配列関数.JPG", "06_ソフトウェア開発（基礎知識）/JavaScript基礎（非同期・配列関数）", None),
        ("3_IT学習/Python資料.jpg", "06_ソフトウェア開発（基礎知識）/Python基礎・配布", None),
        ("3_IT学習/Right Database?.JPG", "06_ソフトウェア開発（基礎知識）/データベース設計", None),
        ("3_IT学習/Webサイトを作る上で知っておきたいこと.JPG", "06_ソフトウェア開発（基礎知識）/Web基礎（HTML/CSS/HTTP）", None),
        ("3_IT学習/Whisperで音声を文字に変換.JPG", "06_ソフトウェア開発（基礎知識）/AI・音声処理（Whisper等）", None),
        ("3_IT学習/ショートカット_VSCode_1.pdf", "09_ツール・操作ガイド/VSCode（概要・ショートカット）", "ショートカット_VSCode_1_学習.pdf"),
        ("3_IT学習/ショートカット_VSCode_2.pdf", "09_ツール・操作ガイド/VSCode（概要・ショートカット）", "ショートカット_VSCode_2_学習.pdf"),
        ("3_IT学習/ネットワーク用語比較.jpeg", "07_IT基礎・インフラ/コンピュータ・ネットワーク", None),
        ("3_IT学習/パーキンソンの法則とエメットの法則.JPG", "03_仕事術・学習法/思考法・フレームワーク", None),
        ("3_IT学習/フルスタック技術の分解.PNG", "07_IT基礎・インフラ/IT概論・DX", None),
        ("3_IT学習/プログラミング学習の死の谷.JPG", "03_仕事術・学習法/学習手順・学習定着", None),
        ("3_IT学習/仕事ができる人とできない人の動き方の違い.JPG", "03_仕事術・学習法/仕事の進め方・可視化", None),
        ("3_IT学習/企業分析.jpeg", "04_ビジネス・マーケティング/企業・業界分析", None),
        ("3_IT学習/作成したpythonコードを配布する.JPG", "06_ソフトウェア開発（基礎知識）/Python基礎・配布", None),
        ("3_IT学習/例：システム概念図.JPG", "05_プロダクト・戦略・設計/業務フロー・システム概念", None),
        ("3_IT学習/全ての人を納得させる難しさ.JPG", "02_対人スキル・コミュニケーション/コミュニケーション基礎", None),
        ("3_IT学習/学習定着率.JPG", "03_仕事術・学習法/学習手順・学習定着", None),
        ("3_IT学習/感覚が先事実が後.JPG", "01_ライフ・自己成長/マインドセット", None),
        ("3_IT学習/文字と年齢.PNG", "09_ツール・操作ガイド/Figma", None),
        ("3_IT学習/業務フロー図.png", "05_プロダクト・戦略・設計/業務フロー・システム概念", None),
        ("3_IT学習/業界市場動向.jpeg", "04_ビジネス・マーケティング/企業・業界分析", None),
        ("3_IT学習/正規表現チートシート.JPG", "06_ソフトウェア開発（基礎知識）/正規表現・文字列処理", None),
        ("3_IT学習/無料学習①.jpeg", "10_学習資料・チートシート/無料学習リソース", None),
        ("3_IT学習/無料学習②.jpeg", "10_学習資料・チートシート/無料学習リソース", None),
        ("3_IT学習/無料学習③.jpeg", "10_学習資料・チートシート/無料学習リソース", None),
        ("3_IT学習/無料学習④.jpeg", "10_学習資料・チートシート/無料学習リソース", None),
        ("3_IT学習/研修資料まとめ①.jpeg", "10_学習資料・チートシート/研修資料まとめ", None),
        ("3_IT学習/研修資料まとめ②.jpeg", "10_学習資料・チートシート/研修資料まとめ", None),
        ("3_IT学習/統計データサイエンス.jpeg", "08_データ・統計/統計・データサイエンス", None),

        # 4_操作 → 09
        ("4_操作/Google Gmail.PNG", "09_ツール・操作ガイド/Google Workspace（Gmail/カレンダー/スプレッドシート/スライド）", None),
        ("4_操作/Googleカレンダー.PNG", "09_ツール・操作ガイド/Google Workspace（Gmail/カレンダー/スプレッドシート/スライド）", None),
        ("4_操作/Googleスプレッドシート.PNG", "09_ツール・操作ガイド/Google Workspace（Gmail/カレンダー/スプレッドシート/スライド）", None),
        ("4_操作/Googleスライド.PNG", "09_ツール・操作ガイド/Google Workspace（Gmail/カレンダー/スプレッドシート/スライド）", None),
        ("4_操作/Mac のキーボードショートカット.pdf", "09_ツール・操作ガイド/Mac（キーボード・OS操作）", None),
        ("4_操作/VSCode.PNG", "09_ツール・操作ガイド/VSCode（概要・ショートカット）", None),
        ("4_操作/ショートカット_VSCode_1.pdf", "09_ツール・操作ガイド/VSCode（概要・ショートカット）", "ショートカット_VSCode_1_操作.pdf"),
        ("4_操作/ショートカット_VSCode_2.pdf", "09_ツール・操作ガイド/VSCode（概要・ショートカット）", "ショートカット_VSCode_2_操作.pdf"),
        ("4_操作/ショートカットキーMAP.PNG", "09_ツール・操作ガイド/Mac（キーボード・OS操作）", None),
        ("4_操作/ユーザー辞書登録一覧.JPG", "09_ツール・操作ガイド/ユーザー辞書", None),

        # 5_マーケティング → 04
        ("5_マーケティング/マーケティングの心理効果_1.JPG", "04_ビジネス・マーケティング/マーケティング心理・行動経済", None),
        ("5_マーケティング/マーケティングの心理効果_2.JPG", "04_ビジネス・マーケティング/マーケティング心理・行動経済", None),
        ("5_マーケティング/マーケティングの心理効果_3.JPG", "04_ビジネス・マーケティング/マーケティング心理・行動経済", None),
        ("5_マーケティング/マーケティングの心理効果_4.JPG", "04_ビジネス・マーケティング/マーケティング心理・行動経済", None),
        ("5_マーケティング/行動心理学①.JPG", "04_ビジネス・マーケティング/マーケティング心理・行動経済", None),
        ("5_マーケティング/行動心理学②.JPG", "04_ビジネス・マーケティング/マーケティング心理・行動経済", None),
    ]

    # Ensure all destination directories exist first
    dest_dirs = sorted(set(d for _, d, _ in mappings))
    for d in dest_dirs:
        ensure_dir(os.path.join(root_dir(), d))

    moved: List[Tuple[str, str]] = []
    errors: List[Tuple[str, str]] = []
    for src, dest_dir, rename_to in mappings:
        try:
            result = move_file(src, dest_dir, rename_to)
            moved.append(result)
        except Exception as e:
            errors.append((src, str(e)))

    # Summary
    print("Moved files:")
    for src, dest in moved:
        print(f"  {src} -> {dest}")
    if errors:
        print("\nErrors:")
        for src, msg in errors:
            print(f"  {src} :: {msg}")


if __name__ == "__main__":
    main()


