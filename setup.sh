# You should have setup.sh and requirements.txt available
chmod +x setup.sh
source setup.sh
# The setup.sh will run the following:
export DATABASE_URL="postgres://nwoghaaslorwxo:5e62f2605c69b6286de746b2ee3197298272b9f72afe37cad412eab8908d278e@ec2-3-230-122-20.compute-1.amazonaws.com:5432/d9o84b2cfr9tha"
export EXCITED="true"
export AUTH0_DOMAIN="coffieshop.us.auth0.com"
export ALGORITHMS="RS256"
export API_AUDIENCE="https://coffee"

echo $DATABASE_URL
echo $EXCITED
echo $AUTH0_DOMAIN
echo $ALGORITHMS
echo $API_AUDIENCE