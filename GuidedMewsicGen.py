'''

	author: cbullers (http://github.com/cbullers/)

	This file is what contains all function definitions, etc that will be used for guided generation

	Outline:
		1. Manually compile multi-dimensional tuple with notes from certain songs, such as in classical or pop genres
		2. Generate a probability dictionary which includes the notes and their probabilities of showing up in the song
		3. Generate a set amount of notes, based off the duration argv
		4. Build the song taking in bpm and other song based variables (synth etc)
		5. Place the WAVE file somewhere in the web server
		6. Return the location of the file for the web server to serve

'''

import sys #argv and such
import pysynth, pysynth_b, pysynth_c, pysynth_d, pysynth_e, pysynth_p, pysynth_s #all available synths
from numpy.random import choice #weighted probability choosing
import os

synths = {
	'a': pysynth,
	'b': pysynth_b,
	'c': pysynth_c,
	'd': pysynth_d,
	'e': pysynth_e,
	'p': pysynth_p,
	's': pysynth_s
} # so each synth can be recognized when passed in argv

'''

	argv breakdown:
		argv[0] is duration of the song in seconds
		argv[1] is the synthesizer that the gen will use in a,b,c format
		argv[2] is the songs that the user will be using for their predictive input
		argv[3] is the bpm or tempo of the song

'''
synthToUse = synths[sys.argv[1]]

'''
	
	songs format:
		list of tuples including notes in the format ('noteOctave-beat',quantity) i.e. ('c4-16',12) for middle c sixteenth note twelve times

'''
songs = {
	"furelise": [('e5-16', 23),('d#5-16', 23),('b5-16', 23),('d5-16', 18),('c5-16', 12),('a5-16', 14),('c4-16', 2),('e4-16', 5),('g#4-16', 1),('g4-16', 5),('f5-16', 4),('f4-16', 3),
 	('e6-16', 1),('a#6-16', 1),('a6-16', 3),('g6-16', 15),('a#5-16', 1),('c6-16', 1),('b6-16', 2)],

	"moonlightsonata": [('f-4', 5),('b-4', 17),('c#3-4', 2),('c#-4', 19),('f#-4', 9),('g#3-4', 16),('g3-4', 9),('g#-4', 11),('d#-4', 7),('e-4', 27),('a3-4', 2),
	('d-4', 2),('b#-4', 1),('e3-4', 1),('a-4', 7)],

	"takeonme": [('a4-4', 4),('f4-4', 4),('d4-4', 4),('g4-4', 4),('c5-4', 5),('d5-4', 5),('g4-8', 4),('g5-4', 5),('g5-8', 5),('f5-4', 5),('f5-8', 5),('e5-4', 5),('d5-2', 5),
 	('e5-8', 5),('a6-4', 6),('b6-8', 6),('c4-1', 4),('b5-1', 5),('c5-1', 5),('g4-1', 4),('a4-1', 4),('e4-1', 4),('c5-2', 5)],

 	"everybodywantstoruletheworld": [('d6-4', 6),('a6-4', 6),('f5-4', 5),('a5-4', 5),('d4-8', 4),('f4-4', 4),('a5-8', 5),('b5-4', 5),('g4-8', 4),('g4-2', 4),('g4-1', 4),
 	('b5-8', 5),('a5-2', 5),('e5-4', 5),('d5-4', 5),('d5-8', 5),('e4-8', 4)]
}

def uniquify(songsu):
	newList = [('c4-16',1)]
	
	for i in songsu:
		try:
			for m in (range(len(newList)) or range(1)):
				if i[0] == newList[m][0]:
					newList[m] = (newList[m][0],i[1]+newList[m][1])
					raise Exception()
			newList.append(i)
		except Exception:
			continue

	return newList

# to be able to be used with pysynth
def generateNotes(songArray, numberOfNotes):

	numberOfUniqueNotes = 0
	uniqueNotes = []
	weightedProb = []
	for i in songArray:
		numberOfUniqueNotes+=i[1]

	for i in songArray:
		uniqueNotes.append(i[0])
		weightedProb.append(i[1]/numberOfUniqueNotes)

	randum = choice(uniqueNotes, numberOfNotes, p=weightedProb)

	noteTuple = ()

	for i in randum:
		length = i[-1]
		noteTuple += (i.split("-")[0],int(length)),

	return noteTuple

#print(generateNotes(songs["moonlightsonata"],100))


def generateWave(duration,synth,tempo,fileLoc):
	synthToUse.make_wav(generateNotes(songs["moonlightsonata"]+songs["furelise"],100), fn=fileLoc)