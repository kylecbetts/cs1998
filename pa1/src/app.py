import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    0: {
        "id": 0,
        "upvotes": 1,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98"
    },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98"
    }
}

comments = {
    0: {
        0: {
            "id": 0,
            "upvotes": 8,
            "text": "Wow, my first Reddit gold!",
            "username": "alicia98"
        }
    },
    1: { 

    }
}

post_id_counter = 2
comment_id_counter = 1


@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here
@app.route("/api/posts/")
def get_posts():
    """
    Gets all posts.
    """
    res = {"posts": list(posts.values())}
    return json.dumps(res), 200


@app.route("/api/posts/", methods=["POST"])
def create_post():
    """
    Creates a new post.

    Throws a 400 error if there is no request body, or the request body does 
    not contain a title, link, or username.
    """
    global post_id_counter
    if not request.data :
        return json.dumps({"error": "No body provided."}), 400
    body = json.loads(request.data)

    title = body.get("title")
    if not title:
        return json.dumps({"error": "No title provided."}), 400

    link = body.get("link")
    if not link:
        return json.dumps({"error": "No link provided."}), 400

    username = body.get("username")
    if not username:
        return json.dumps({"error": "No username provided."}), 400

    post = {
        "id": post_id_counter,
        "upvotes": 1,
        "title": title,
        "link": link,
        "username": username
    }
    posts[post_id_counter] = post
    comments[post_id_counter] = {}
    post_id_counter += 1
    return json.dumps(post), 201


@app.route("/api/posts/<int:post_id>/")
def get_post(post_id):
    """
    Gets the post with id of post_id.

    Throws a 404 error if no post with post_id exists.
    """
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found."}), 404
    return json.dumps(post), 200


@app.route("/api/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(post_id):
    """
    Deletes the post with id of post_id.

    Throws a 404 error if no post with post_id exists.
    """
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found."}), 404
    del posts[post_id]
    del comments[post_id]
    return json.dumps(post), 200


@app.route("/api/posts/<int:post_id>/comments/")
def get_comments(post_id):
    """
    Get all comments for the post with id post_id.

    Throws a 404 error if no post with post_id exists.
    """
    if not post_id in comments:
        return json.dumps({"error": "Post not found."}), 404
    res = {"comments": list(comments[post_id].values())}
    return json.dumps(res), 200


@app.route("/api/posts/<int:post_id>/comments/", methods=["POST"])
def create_comment(post_id):
    """
    Create comment on post with id of post_id.

    Throws a 404 error if no post with post_id exists.

    Throws a 400 error if there is no request body, or the request body does 
    not contain a text, or username.
    """
    global comment_id_counter
    if not post_id in comments:
        return json.dumps({"error": "Post not found."}), 404
    if not request.data :
        return json.dumps({"error": "No data provided."}), 400
    body = json.loads(request.data)

    text = body.get("text")
    if not text:
        return json.dumps({"error": "No title provided."}), 400

    username = body.get("username")
    if not username:
        return json.dumps({"error": "No username provided."}), 400

    comment = {
        "id": comment_id_counter,
        "upvotes": 1,
        "text": text,
        "username": username
    }
    comments[post_id][comment_id_counter] = comment
    comment_id_counter += 1
    return json.dumps(comment), 201


@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods=["POST"])
def edit_comment(post_id, comment_id):
    """
    Edits the comment with id comment_id on post with id post_id.

    Throws a 404 error if no post with post_id exists or no comment with 
    comment_id exists on that post.

    Throws a 400 error if there is no request body, or the request body does 
    not contain a text.
    """
    post_comments = comments.get(post_id)
    if not post_comments:
        return json.dumps({"error": "No comment found."}), 404
    comment = post_comments.get(comment_id)
    if not comment:
        return json.dumps({"error": "No comment found."}), 404
    if not request.data :
        return json.dumps({"error": "No data provided."}), 400
    body = json.loads(request.data)
    text = body.get("text")
    if not text:
        return json.dumps({"error": "No text provided."}), 400
    comments[post_id][comment_id]["text"] = text
    return json.dumps(comments[post_id][comment_id]), 200


@app.route("/api/extra/posts/", methods=["POST"])
def extra_credit_create_post():
    """
    Extra credit: Creates a new post.

    Throws a 400 error if there is no request body, or the request body does 
    not contain a title, link, or username.

    Also throws a 400 error if the title, link, or username is of the wrong 
    type or format.
    """
    global post_id_counter
    if not request.data :
        return json.dumps({"error": "No body provided."}), 401
    body = json.loads(request.data)

    title = body.get("title")
    if not title:
        return json.dumps({"error": "No title provided."}), 401
    if not isinstance(title, str):
        return json.dumps({"error": "title is invalid."}), 401

    link = body.get("link")
    if not link:
        return json.dumps({"error": "No link provided."}), 401
    if not isinstance(link, str):
        return json.dumps({"error": "link is invalid."}), 401

    username = body.get("username")
    if not username:
        return json.dumps({"error": "No username provided."}), 401
    if not isinstance(username, str):   
        return json.dumps({"error": "username is invalid."}), 401

    post = {
        "id": post_id_counter,
        "upvotes": 1,
        "title": title,
        "link": link,
        "username": username
    }
    posts[post_id_counter] = post
    comments[post_id_counter] = {}
    post_id_counter += 1
    return json.dumps(post), 201


@app.route("/api/extra/posts/<int:post_id>/comments/", methods=["POST"])
def extra_credit_create_comment(post_id):
    """
    Extra credit: Create comment on post with id of post_id.

    Throws a 404 error if no post with post_id exists.

    Throws a 400 error if there is no request body, or the request body does 
    not contain a text or username.

    Also throws a 400 error if the text or username is of the wrong 
    type or format.
    """
    global comment_id_counter
    if not post_id in comments:
        return json.dumps({"error": "Post not found."}), 404
    if not request.data :
        return json.dumps({"error": "No data provided."}), 401
    body = json.loads(request.data)

    text = body.get("text")
    if not text:
        return json.dumps({"error": "No text provided."}), 401
    if not isinstance(text, str):
        return json.dumps({"error": "text is invalid."}), 401

    username = body.get("username")
    if not username:
        return json.dumps({"error": "No username provided."}), 401
    if not isinstance(username, str):
        return json.dumps({"error": "username is invalid."}), 401

    comment = {
        "id": comment_id_counter,
        "upvotes": 1,
        "text": text,
        "username": username
    }
    comments[post_id][comment_id_counter] = comment
    comment_id_counter += 1
    return json.dumps(comment), 201


@app.route("/api/extra/posts/<int:post_id>/comments/<int:comment_id>/", methods=["POST"])
def extra_credit_edit_comment(post_id, comment_id):
    """
    Extra credit: Edits the comment with id comment_id on post with id post_id.

    Throws a 404 error if no post with post_id exists or no comment with 
    comment_id exists on that post.

    Throws a 400 error if there is no request body, or the request body does 
    not contain a text.

    Also throws a 400 error if the title, link, or username is of the wrong 
    type or format.
    """
    post_comments = comments.get(post_id)
    if not post_comments:
        return json.dumps({"error": "No comment found."}), 404
    comment = post_comments.get(comment_id)
    if not comment:
        return json.dumps({"error": "No comment found."}), 404
    if not request.data :
        return json.dumps({"error": "No data provided."}), 401
    body = json.loads(request.data)

    text = body.get("text")
    if not text:
        return json.dumps({"error": "No text provided."}), 401
    if not isinstance(text, str):
        return json.dumps({"error": "text is invalid."}), 401

    comments[post_id][comment_id]["text"] = text
    return json.dumps(comments[post_id][comment_id]), 200


@app.route("/api/extra/posts/<int:post_id>/", methods=["POST"])
def extra_credit_increment_upvotes(post_id):
    """
    Extra credit: Increments the upvotes on post with id post_id.

    If a body is included, the value in the field upvotes determines 
    how much to increment the upvotes by. If no body is provided, the upvotes 
    are incremented by 1.

    Throws a 404 error if no post with post_id exists.

    Throws a 400 error if the request body does not contain an upvotes.
    """
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found."}), 404
    upvotes = post["upvotes"]

    # If no body, increment votes by 1
    if not request.data:
        upvotes += 1
    else:
        body = json.loads(request.data)
        inc_upvotes = body.get("upvotes")
        if not upvotes:
            return json.dumps({"error": "No upvotes provided."}), 400
        upvotes += inc_upvotes
    posts[post_id]["upvotes"] = upvotes
    return json.dumps(posts[post_id]), 200


@app.route("/api/extra/posts/")
def extra_credit_get_posts():
    """
    Gets all posts sorted in order of upvotes.
    """
    sort_direction = request.args["sort"]
    post_list = list(posts.values())
    if not sort_direction:
        return json.dumps({"error": "No sort provided."}), 400
    if sort_direction == "increasing":
        post_list.sort(key=lambda x: x["upvotes"])
    else:
        post_list.sort(key=lambda x: x["upvotes"], reverse=True)
    res = {"posts": post_list}
    return json.dumps(res), 200
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
