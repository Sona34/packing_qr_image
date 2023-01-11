try_steps=1

for i in `seq 0 $try_steps`
do

#   %E	経過した実時間（書式は、[hours:]minutes:seconds）
#   %e	経過した実時間（秒単位）
#   %S	コマンドを実行するのに使用したシステムCPU時間（秒単位）
#   %U	コマンドを実行するのに使用したユーザーCPU時間（秒単位）
#   %P	コマンド実行時のCPU使用率（％）。計算式は、（%U + %S） / %e
  echo $i
  time --output 5rect.log --append -f '%e,%S,%U' python3 Packing.py >> 5rect.log
  # echo $(($try_steps - $i))
done