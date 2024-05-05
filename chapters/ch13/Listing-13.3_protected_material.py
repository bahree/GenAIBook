import requests
import os
import http.client

CONTENT_SAFETY_ENDPOINT = os.getenv("CONTENT_SAFETY_ENDPOINT")
CONTENT_SAFETY_KEY = os.getenv("CONTENT_SAFETY_KEY")
API_VERSION = "2023-10-15-preview"

#connection = http.client.HTTPSConnection(CONTENT_SAFETY_ENDPOINT)

# Old The text to be analyzed
# text_to_analyze = "Kiss me out of the bearded barley Nightly beside the green, green grass Swing, swing, swing the spinning step You wear those shoes and I will wear that dress Oh, kiss me beneath the milky twilight Lead me out on the moonlit floor Lift your open hand Strike up the band and make the fireflies dance Silver moon's sparkling So, kiss me Kiss me down by the broken tree house Swing me upon its hanging tire Bring, bring, bring your flowered hat We'll take the trail marked on your father's map."

# Once upon a time
# The planets and the fates and all the stars aligned
# You and I ended up in the same room at the same time
# And the touch of a hand lit the fuse
# Of a chain reaction of countermoves
# To assess the equation of you
# Checkmate, I couldn't lose
# What if I told you none of it was accidental?
# And the first night that you saw me
# Nothing was gonna stop me
# I laid the groundwork, and then just like clockwork
# The dominoes cascaded in a line
# What if I told you I'm a mastermind?
# And now you're mine
# It was all by design
# 'Cause I'm a mastermind
# You see, all the wisest women had to do it this way
# 'Cause we were born to be the pawn in every lover's game
# If you fail to plan, you plan to fail
# Strategy sets the scene for the tale
# I'm the wind in our free-flowing sails
# And the liquor in our cocktails
# What if I told you none of it was accidental?
# And the first night that you saw me I knew I wanted your body
# I laid the groundwork, and then just like clockwork
# The dominoes cascaded in a line
# What if I told you I'm a mastermind?
# And now you're mine
# It was all my design
# 'Cause I'm a mastermind
# No one wanted to play with me as a little kid
# So I've been scheming like a criminal ever since
# To make them love me and make it seem effortless
# This is the first time I've felt the need to confess
# And I swear
# I'm only cryptic and Machiavellian 'cause I care
# So I told you none of it was accidental?
# And the first night that you saw me
# Nothing was gonna stop me
# I laid the groundwork, and then saw a wide smirk
# On your face, you knew the entire time
# You knew that I'm a mastermind
# And now you're mine
# Yeah, all you did was smile
# 'Cause I'm a mastermind


text_to_analyze = "Once upon a time The planets and the fates and all the stars aligned You and I ended up in the same room at the same time And the touch of a hand lit the fuse Of a chain reaction of countermoves To assess the equation of you Checkmate, I couldn't lose What if I told you none of it was accidental? And the first night that you saw me Nothing was gonna stop me I laid the groundwork, and then just like clockwork The dominoes cascaded in a line What if I told you I'm a mastermind? And now you're mineIt was all by design 'Cause I'm a mastermind You see, all the wisest women had to do it this way 'Cause we were born to be the pawn in every lover's game If you fail to plan, you plan to fail Strategy sets the scene for the tale I'm the wind in our free-flowing sails And the liquor in our cocktails What if I told you none of it was accidental"

# Set up the API request
url = f"{CONTENT_SAFETY_ENDPOINT}/contentsafety/text:detectProtectedMaterial?api-version={API_VERSION}"

headers = {
  "Content-Type": "application/json",
  "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY
}
data = {
  "text": text_to_analyze
}

# Send the API request
response = requests.post(url, headers=headers, json=data, timeout=10)

# Handle the API response
if response.status_code == 200:
    result = response.json()
    print("Analysis result:", result)
else:
    print("Error:", response.status_code, response.text)