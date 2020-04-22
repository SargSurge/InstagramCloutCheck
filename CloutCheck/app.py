from flask import Flask, request, jsonify
from pygram import PyGram as gram
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
app = Flask(__name__)

user = 'perez_sergio_'
password = 'Sergitopito0104*'
ig = gram(user,password)

def get_followers(cloutcheck_user):
    profile = ig.get_profile(cloutcheck_user)
    followers = profile['followers_count']
    return followers

def following_ratio(cloutcheck_user):
    
    profile = ig.get_profile(cloutcheck_user)
    followers = int(profile['followers_count'])
    following = int(profile['followed_count'])
    follow_ratio = followers/following

    return follow_ratio

def likes_to_follow(cloutcheck_user):

    posts = ig.get_posts(cloutcheck_user, limit = 10)
    profile = ig.get_profile(cloutcheck_user)
    likes = []
    for post in posts:
        likes.append(post['likes_count'])
    if not likes:
        return 0
    avg_likes = sum(likes)/len(likes)
    followers = int(profile['followers_count'])

    return avg_likes/followers

def clout_check(cloutcheck_user):

    like_ratio = likes_to_follow(cloutcheck_user)
    follow_ratio = following_ratio(cloutcheck_user)

    return {'like':like_ratio,'follow':follow_ratio}

@app.route('/cloutcheck', methods = ['POST'])
def submit():
    clout_user = request.form.get('user')
    likeRatio = round(likes_to_follow(clout_user), 3)
    followRatio = round(following_ratio(clout_user), 3)
    num_followers = int(get_followers(clout_user))
    clout_score = int(((likeRatio+followRatio)/2)*num_followers)
    file = open('clout.html')
    clout_html = file.read()
    lastLine = ''
    if likeRatio == 0:
        lastLine = 'Please set your profile to Public for a more accurate score.'
    else:
        lastLine = 'Thank you for using Clout Check!'

    return clout_html.format(clout_user,num_followers, followRatio, likeRatio, clout_score, lastLine)

@app.route('/cloutapi', methods = ['GET'])
def respond():
    clout_user = request.args.get("user")
    results = clout_check(clout_user)
    return jsonify(results)
    
@app.route('/')
def index():
    f = open('form.html')
    ig_form = f.read()
    return ig_form

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
