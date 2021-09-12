
import time
import random

# this is time countdown stuff, not necessary
def countdown(time_sec):
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        time_sec -= 1

    print("Time's up!")

songs = ["Uh Huh", "Archive", "Holy Smokes", "Not tha Same", "Packrunner Bitch", "Off Tha Lot", "Glue", "Summer Rain"]
artists = ["Kankan", "Kankan", "Trippie Redd", "Yeat", "Summrs", "Yeat", "ByVincii", "Yung Lean"]
def playgame(songs, artists) :
    songsLen = len(songs)
    wrongAnswer = False
    score = 0

    while wrongAnswer == False :
        currNum = random.randint(0, len(songs)-1)
        currSong = songs[currNum]
        currArtist = artists[currNum]
        # countdown(5)
        print(currSong)
        guess = input("\nEnter the song name: ")
        if(guess.lower() == currSong.lower()) :
            print('\nCorrect!')
            songs.remove(currSong)
            artists.remove(currArtist)
            score += 1
            if(score == songsLen) :
                print("You guessed all songs correctly!")
                print("Your score was", score)
                break
        else :
            print('\nIncorrect! The song was', currSong, 'by', currArtist)
            print('Your score was', score)
            wrongAnswer = True

playgame(songs, artists)