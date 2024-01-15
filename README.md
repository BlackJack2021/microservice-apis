# 当リポジトリについて

[実践マイクロサービス API](https://www.shoeisha.co.jp/book/detail/9784798179735) を読み、それを手元で再現しながら学習を進めた際の記録となります。

適宜、GPT に概念を質問したりしながら深められた理解は各種 `note.md` にてまとめられています。

# 実行環境

docker を用いて環境を構築しています。ルートディレクトリにて、

```
docker compose up -d
```

コマンドを叩いてコンテナを作成後

```
docker compose exec app bash
```

と打ち込むことでコンテナに入ることができます。

依存関係は poetry で管理しています。
