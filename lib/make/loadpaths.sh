
while read line; do
    name=$(echo "$line" | cut -d$'\t' -f1)
    value=$(echo "$line" | cut -d$'\t' -f2)
    export $name=$value
done <"$1"
