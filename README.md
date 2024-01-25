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