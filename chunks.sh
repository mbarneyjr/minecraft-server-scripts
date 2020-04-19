DELAY=1
INCREMENT=240

send() {
    screen -p 0 -S minecraft -X eval "stuff \"$@\"\\015"
}

send "gamerule doDaylightCycle false"
send "gamerule doWeatherCycle false"
send "gamerule doMobSpawning false"

X=-720
Z=-720
Y=192
send "tp @p $X $Y $Z"
sleep $DELAY

for i in {1..6}; do
    echo "$X, $Z"

    for j in {1..6}; do
        send "tp @p $X $Y $Z -90 20"
        sleep $DELAY
        send "tp @p $X $Y $Z 0 20"
        sleep $DELAY
        send "tp @p $X $Y $Z 90 20"
        sleep $DELAY
        send "tp @p $X $Y $Z 180 20"
        sleep $DELAY

        X=$((X + INCREMENT))
        send "tp @p $X $Y $Z"
        sleep $DELAY
    done

    Z=$((Z + INCREMENT))
    X=-720
    send "tp @p $X $Y $Z"
    sleep $DELAY
done

send "gamerule doDaylightCycle true"
send "gamerule doWeatherCycle true"
send "gamerule doMobSpawning true"
