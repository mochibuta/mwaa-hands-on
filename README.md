
# Setup

## 1. mwaa-local-runnerのdockerイメージをビルドする
[aws-mwaa-local-runner](https://github.com/aws/aws-mwaa-local-runner)をclone

```bash
git clone https://github.com/aws/aws-mwaa-local-runner
```

mainブランチがbuild-imageに失敗するので修正する([修正方法](https://github.com/aws/aws-mwaa-local-runner/pull/73/files))
[6e5925bafba68d803e807efc98d53233d80796ad]  

```diff
cd aws-mwaa-local-runner
vim aws-mwaa-local-runner/docker/config/constraints.txt

- Flask-OpenID==1.2.5
+ Flask-OpenID==1.3.0
```

vscodeでdevcontainerを使用するためにtarを使えるようにする

```diff
vim mwaa-local-env

#SYTEM_DEPS=tarをbuild-argに追加
+build_image() {
+   docker build --rm --compress -t amazon/mwaa-local:$AIRFLOW_VERSION ./docker --build-arg SYSTEM_DEPS=tar
+}
```

```
./mwaa-local-env build-image
```

## 2. ローカル環境を起動する

```bash
docker compose up -d
```

起動後、[localhost:8080](localhost:8080)へアクセスする

```
username: admin
password: test
```

# dagの開発

- vscodeの[Remote-Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)拡張を入れる
- `Ctrl + Shift + P`から`Remote-Containers: Reopen in Container`を選択してdagを編集する

- テストデータをlocalstackに送信
```bash
aws s3api create-bucket --bucket test --endpoint-url http://localhost:4566
aws s3 cp ./testdata/test.csv s3://test --recursive --endpoint-url http://localhost:4566
```