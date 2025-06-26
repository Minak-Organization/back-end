import os
from app import create_app, db
from app.models import Song

app = create_app()

with app.app_context():
    audio_dir = os.path.join("static", "audio")
    files = [f for f in os.listdir(audio_dir) if f.lower().endswith(".mp3")]

    added = 0
    for filename in files:
        if Song.query.filter_by(audio_filename=filename).first():
            print(f" Skipping: {filename} already exists in DB")
            continue

        title = filename.rsplit(".", 1)[0].replace("_", " ").title()
        new_song = Song(title=title, artist="Unknown Artist", audio_filename=filename)
        db.session.add(new_song)
        added += 1
        print(f" Added: {title}")

    db.session.commit()
    print(f"\n Done! {added} new songs were added to the database.")