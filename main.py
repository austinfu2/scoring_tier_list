import os
import random
import sqlite3
from flask import Flask, request, render_template, url_for
from bs4 import BeautifulSoup

app = Flask(__name__)

# get a list of all player image filenames in the player_faces folder
player_images = os.listdir("static/player_faces")
# shuffle the list of player image filenames
random.shuffle(player_images)

# loop over each imagebox and assign a random image to its src attribute
with open("templates/index.html") as file:
    soup = BeautifulSoup(file, 'html.parser')

@app.route('/')
def home():
    # find all the image tags and update their src attributes with the random filenames
    for i, img in enumerate(soup.find_all('img', class_='player-image')):
        img['src'] = f"{{{{ url_for('static', filename='player_faces/{player_images[i]}') }}}}"
        img.parent['data-image'] = player_images[i][:-4]

    # save the updated HTML back to the file
    with open("templates/index.html", "w") as output_file:
        output_file.write(str(soup))
    return render_template("index.html", player_images=player_images)

# loop over the dropzones and insert the player positions into the database
@app.route('/submit', methods=["GET", "POST"])
def submit():
    try:
        # connect to the database
        with sqlite3.connect('mydatabase.db') as conn:
            # create a cursor object
            cursor = conn.cursor()

            for i in range(1, 11):
                dropzone_id = f"dropzone-{i}"
                player_id = request.form.get(dropzone_id)
                if player_id:
                    cursor.execute("INSERT INTO player_positions (player_id, position) VALUES (?, ?)", (player_id, dropzone_id))
        # commit the changes
        conn.commit()

        return render_template("results.html", message="Data successfully saved to database.")
    except Exception as e:
        return render_template("results.html", message=f"Error: {e}")

# define the route for the results page
@app.route('/results')
def results():
    return render_template("results.html")

# add a context processor to make the player_images list available to all templates
@app.context_processor
def inject_player_images():
    return dict(player_images=player_images)

if __name__ == "__main__":
    app.run(debug=True)
