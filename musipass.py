import os, sys, math
import pygame
from pygame.locals import *
import numpy
import pickle, imp

default_keyset_name = "default"

#Define grid size for window and other constants
rows = 6
cols = 5
unit_size = 80
unit_inner_size = int(unit_size * 0.75)
unit_inner_offset = int(unit_size * 0.125)
x = 0
y = 0

#Database to test passwords against
test_db = {}

def load_text(fname):
	try:
		file = open(fname, 'r')
		data = file.read()
		file.close()
		return data
	except:
		print "No file '%s' found." % fname
		return ""

def load_pkl(fname):
	try:
		pkl_file = open(fname, 'rb')
		data = pickle.load(pkl_file)
		pkl_file.close()
		return data
	except:
		print "No file '%s' found." % fname
		
def load_db(fname='musipass.pkl'):
	global test_db

	data = load_pkl(fname)
	if data:
		test_db = data
	else:
		print "No database found."
	
def save_db(fname='musipass.pkl'):
	global test_db
	try:
		output = open(fname, 'wb')
		pickle.dump(test_db, output)
		output.close()
	except Exception as e:
		print "Couldn't save database. %s" % e
	
#Array of keysets
current_keyset = ""
keysets = {}
key_map = None
sound_func = None

def set_keyset(name):
	global current_keyset, key_map, sound_func
	current_keyset = name
	key_map = keysets[name].key_map
	sound_func = keysets[name].sound_func
	print "Set to keyset: " + name
	

def check_keyset_folder(keyset_list, dir, names):
	#Add all python file names (minus extension) to a list
	for n in names:
		print os.path.join(dir, n)
		if os.path.isfile(os.path.join(dir, n)) and n[-3:] == ".py":
			keyset_list.append(n[:-3])
	
	#Empty list of names, so no subdirectories are checked
	del names[:]

#Get list of files in keysets
found_keysets = []
os.path.walk('./keysets/', check_keyset_folder, found_keysets)
	
for fk in found_keysets:
	#Check for modules found in keysets dir
	stats = imp.find_module(fk, ['./keysets/'])
	#If an open file object returned
	if stats[0]:
		try:
			#load module
			mod = imp.load_module(fk, *stats)
			#save into list of keysets
			keysets[fk] = mod
		finally:
			#close file for module
			stats[0].close()

#Find and set to default keyset
for ks in keysets:
	if ks == default_keyset_name:
		set_keyset(ks)
		print "Loaded keyset " + ks

#Load key sets
# for keyset_name in keysets:
	
	# text = load_text(keyset_name)
	# if text:
		# key_map, sound_func = eval(text)
		# key_maps.append(key_map)
		# if sound_func:
			# sound_funcs.append(sound_func)
		# else:
			# sound_funcs.append(None)
	# else:
		# print "Couldn't load empty keyset '%s'." % keyset_name

if len(keysets) == 0:
	print "Couldn't load any keysets. Exiting"
	sys.exit(0)

def sine_array_onecycle(hz, samp_rate):
	length = samp_rate / float(hz)
	#get multiplier to get 2pi worth over the length = one full cycle
	omega = 2.0 * numpy.pi / length
	xvalues = numpy.arange(int(length)) * omega
	return numpy.sin(xvalues)
    
def sine_array(hz, n_samples, samp_rate):
    return numpy.resize(sine_array_onecycle(hz, samp_rate), (n_samples, 2))

def make_sound(key_info, samp_rate, length):
	octave = 1 #math.floor(key_info[0] / 2.0)
	f = 200 * math.pow(2, octave)
	f *= math.pow(2, float(key_info[1]) / 12.0)
	
	if key_info[0] == 0:
		if key_info[2]:
			f2 = 5.0 * f / 3.0 #major 6th
		else:
			f2 = f
	elif key_info[0] == 1:
		if key_info[2]:
			f2 = 5.0 * f / 4.0 #major 3rd
		else:
			f2 = 6.0 * f / 5.0 #minor 3rd
	elif key_info[0] == 2:
		if key_info[2]:
			f2 = 3.0 * f / 2.0 #5th
		else:
			f2 = 4.0 * f / 3.0 #perfect 4th
	elif key_info[0] == 3:
		if key_info[2]:
			f2 = 7.0 * f / 4.0 #major 7th?
		else:
			f2 = 0.5 * f #octave
		
	#  3.0 * f / 2.0 #5th
	#  4.0 * f / 3.0 #perfect 4th
	#  5.0 * f / 4.0 #major 3rd
	#  5.0 * f / 3.0 #major 6th
	#  6.0 * f / 5.0 #minor 3rd
	#  7.0 * f / 6.0 #minor 7th?
	#  7.0 * f / 5.0 #dim
	#  7.0 * f / 4.0 #major 7th?
	#  7.0 * f / 3.0 #dim
	
	#Set duration of the tone (sample rate * seconds to play)
	duration_in_samples = int(samp_rate * length)
	
	sound = pygame.sndarray.make_sound(sine_array(f, duration_in_samples, samp_rate))
	channel = sound.play()
	if channel:
		channel.set_volume(0.7, 0.3)
	
	sound = pygame.sndarray.make_sound(sine_array(f2, duration_in_samples, samp_rate))
	channel = sound.play()
	if channel:
		channel.set_volume(0.2, 0.5)

def print_status():
	scr_size = screen.get_size()
	text_size = status_text[current_mode].get_size()
	text_x = (scr_size[0] / 2) - (text_size[0] / 2)
	text_y = (scr_size[1] - (unit_size * 0.5) - (text_size[1] * 0.5) )
	
	screen.blit(status_text[current_mode], (text_x, text_y))
		
#Init pygame systems
pygame.mixer.pre_init(44100, -16, 2)
pygame.init()
#Create screen size with allowed grid plus 1 row for status text
screen = pygame.display.set_mode((cols * unit_size, (rows + 1) * unit_size))
pygame.display.set_caption('MusiPass 0.1')
pygame.mouse.set_visible(0)

#Load up the database
load_db()

#Get sound config
sound_format = pygame.mixer.get_init()
sample_rate = sound_format[0]
sample_bits = abs(sound_format[1])
sample_signed = sound_format[0] < 0
if sound_format[1] != -16:
	print "Sound format unexpected. Exiting."
	sys.exit(0)

#Create visual display
background = pygame.Surface(screen.get_size()).convert()
background.fill((0, 0, 0))
screen.blit(background, (0,0))

block = pygame.Surface((unit_size, unit_size)).convert()
block.fill((255, 0, 0))

block_inner = pygame.Surface((unit_inner_size, unit_inner_size)).convert()
block_inner.fill((255, 0, 0))

#Render game mode names
font = pygame.font.SysFont('Comic Sans', 24, bold=True, italic=False)
if not font:
	print "Font couldn't be loaded. Exiting."
	sys.exit(0)
	
status_text = { "musimode" : font.render('Musimode', True, (192, 255, 192), (64, 64, 64)),
				"passmode" : font.render('Passmode', True, (255, 192, 192), (64, 64, 64)),
				"testmode" : font.render('Testmode', True, (192, 192, 255), (64, 64, 64)) }

current_mode = "musimode"

#Print current status on the screen
print_status()
				
pygame.display.flip()

#Blocks hold information about each key pressed
blocks = []

last_pass = ""
last_entry = ""
confirm = False
typing = False

def finalize(save=True):
	global blocks, x, y, confirm, last_pass, current_mode, test_db, last_entry, typing
	password = "".join( [ a[0] for a in blocks ] )
	if current_mode == "testmode" and save:
		if not confirm:
			if not password in test_db:
				print "Entry not found for", password
			else:
				saved_blocks = test_db[password]
				last_pass = "".join( [ a[0] for a in saved_blocks ] )
				last_entry = password
				print "Please confirm password for", password
				confirm = True
		else:
			if password == last_pass:
				print "Password confirmed!"
			else:
				print "Incorrect password!"
			confirm = False
	elif current_mode == "passmode" and save:
		#If first save notify user to confirm
		if not confirm :
			print "Please confirm password: " + password
			confirm = True
			typing = False
			last_pass = password
		#Second save (confirming) then save to text file
		elif not typing:
			if last_pass != password:
				print "Password mismatch: %s != %s" % (password, last_pass)
				confirm = False
			else:
				print "Password confirmed: %s" % (password)
				print "Save name?"
				typing = True
				last_entry = blocks
		else:
			if password:
				test_db[password] = last_entry
				print "Saved"
				print password
			#get out of confirm mode
			confirm = False
			typing = False
			
	else:
		last_pass = ""
		confirm = False
		
	blocks = []
	x = y = 0
	screen.blit(background, (0,0))
	print_status()
	pygame.display.flip()

while 1:
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			save_db()	
			sys.exit(0)
		elif event.type == KEYDOWN:
			if event.key == K_RETURN:
				finalize()
			elif event.key == K_BACKQUOTE:
				finalize(False)
			elif event.key == K_BACKSPACE:
				if len(blocks) > 0:
					blocks[len(blocks)-1:] = []
					x -= 1
					if x < 0:
						x += cols
						y -= 1
					
					block.fill((0,0,0))
					screen.blit(block, (x * unit_size, y * unit_size))
					pygame.display.flip()
					if len(blocks) > 0:
						if not typing and (current_mode != "testmode" or confirm):
							make_sound(blocks[len(blocks)-1][1])
			elif event.key == K_PAGEUP or event.key == K_PAGEDOWN:
				ks_names = keysets.keys()
				j = -1
				#find index of current keyset
				for i in range(len(ks_names)):
					if ks_names[i] == current_keyset:
						j = i
				#increment or decrement
				if event.key == K_PAGEUP:
					j += 1
					j = j % len(ks_names)
				else:
					j -= 1
					if j < 0:
						j = len(ks_names) - 1
				set_keyset(ks_names[j])
			elif event.key == K_TAB:
				confirm = False
				typing = False
				last_entry = ""
				if current_mode == "musimode":
					current_mode = "passmode"
				elif current_mode == "passmode":
					current_mode = "testmode"
				else:
					current_mode = "musimode"
				print_status()
				pygame.display.flip()
			elif event.key in key_map:
				mod = 0
				if event.mod & KMOD_SHIFT:
					mod = 1
				key_info = list(key_map[event.key])
				key_info.append(mod)
				blocks.append((event.unicode, key_info))
				if not typing and (current_mode != "testmode" or confirm):
					#If using custom sound function, call it
					if sound_func:
						sound_func(key_info, sample_rate, 0.07)
					#Otherwise, call default sound function
					else:
						make_sound(key_info, sample_rate, 0.07)
				color = (key_info[0] * 48 + key_info[1] * 4, key_info[1] * 18 + key_info[0] * 2, key_info[2] * 200)
				color2 = ((12 - key_info[1]) * 18 + (4 - key_info[0]) * 2, (1 - key_info[2]) * 200, (4 - key_info[0]) * 48 + (12 - key_info[1]) * 4)
				block.fill(color)
				block_inner.fill(color2)
				screen.blit(block, (x * unit_size, y * unit_size))
				screen.blit(block_inner, (x * unit_size + unit_inner_offset, y * unit_size + unit_inner_offset))
				text = font.render(event.unicode, False, (255, 255, 255), (0,0,0))
				screen.blit(text, (x * unit_size + (unit_size * 0.5) - (text.get_size()[0] * 0.5), y * unit_size + (unit_size * 0.5) - (text.get_size()[1] * 0.5)))
				pygame.display.flip()
				x += 1
				if x >= cols:
					x = 0
					y += 1
				#pygame.time.delay(100)
				if y >= rows:
					finalize(False)
				
				
			