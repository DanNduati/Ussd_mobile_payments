#!/bin/sh
# Goal: Automate running ngrok in the background and getting the tunnel hostname which will then be stored as an env variable

# Set local port from terminal arg or default to 8000(uvicorn default)
LOCAL_PORT=${1-8000}

# Run ngrok tunnel as a background process
#ngrok http ${LOCAL_PORT} &>/dev/null &
ngrok http ${LOCAL_PORT} --log=stdout > ngrok.log &

#get the first tunnel and pipe it to the json processor
echo -n "Extracting ngrok public url ."
NGROK_PUBLIC_URL=""

# Loop hitting the ngrok api curl to get the first tunnel until the NGROK_PUBLIC_URL has a valid value.
while [ -z "$NGROK_PUBLIC_URL" ]; do
    NGROK_PUBLIC_URL=$(curl -s localhost:4040/api/tunnels | jq -r ".tunnels[0].public_url")
    sleep 2
    echo -n "."
done
#print out the public address of the tunnel
echo
echo "NGROK_PUBLIC_URL => [ $NGROK_PUBLIC_URL ]"
#edit lnm callback with new ngrok tunnel hostname
#sed -i.bak "s/NGROK_PUBLIC_URL=/NGROK_PUBLIC_URL=${NGROK_PUBLIC_URL}/g" ../app/.env
sed -i.bak 's|NGROK_PUBLIC_URL=.*|NGROK_PUBLIC_URL='"${NGROK_PUBLIC_URL}"'|g' ../app/.env
sed -i.bak 's|LNM_CALLBACK_URL=.*|LNM_CALLBACK_URL='"${NGROK_PUBLIC_URL}/payments/confirmation"'|g' ../app/.env
