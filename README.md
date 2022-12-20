# packing_qr_image

## Prerequisites
---
 * Python 3.8.10

## installation
---
```
```
## Usage
---
Parameters.pyのパラメータを適切に設定
- Parameters
  - device_id デバイスの種類．登録していない場合は番号を追加して選択する．
    - device 0 : Inspiron 5480
    - device 1 : raspi
    - device 2 : desktop PC
  - cut_tag は分割した画像セット. どのセットを使用するか選択する．
  - bin_width, bin_height パッキングする空画像(bin)のサイズ.
- measure_time.sh 
  - try_steps 実行回数．

その後，
```
sh measure_time.sh
```
を実行する