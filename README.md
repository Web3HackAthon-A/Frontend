# Frontend

IPFSの使い方

参考：https://docs.ipfs.tech/install/run-ipfs-inside-docker/#set-up

1. dockerを実行する
2. docker-compose.ymlを実行
```sh
docker-compose up -d
```
3. stagingフォルダーにaddしたいファイルを入れる
4. ipfsに載せる(frontend-ipfs-1となっているところにはdocker psでコンテナ名を確認してそれを入れる, hello.txtにはファイル名を入れる)
```sh
docker exec frontend-ipfs-1 ipfs add /export/hello.txt
```
5. addedの後ろにQmで始まるハッシュ値が表示される。この値を控えておく
6. アップロードしたファイルを確認するときはブラウザに以下のアドレスを入れる。ipfs.ioは接続するためのゲートウェイであって、他にも様々なものがある。（自分で作ることもできる。）
```sh
https://ipfs.io/ipfs/<ハッシュ値>
```

！！注意！！
Pythonでipfsを操作するライブラリipfshttpclientは最新のipfsをサポートしない。
そのため、今のdockerの設定では操作できない（docker hubに載っているイメージより昔のバージョンが必要）
macの場合、以下の手順でローカルにv0.7.0バージョンをインストールすることを推奨

```sh
wget https://ipfs.io/ipns/dist.ipfs.tech/go-ipfs/v0.7.0/go-ipfs_v0.7.0_darwin-amd64.tar.gz

tar xvfz go-ipfs_v0.7.0_darwin-amd64.tar.gz

sudo mv go-ipfs/ipfs /usr/local/bin/

ipfs init

ipfs --version    

#ipfsの実行
ipfs daemon

#ipfsを終了
ipfs shutdown
```
