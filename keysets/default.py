#Default keyset

import math, numpy
import pygame
from pygame.locals import *

#Key-mapping
key_map = {
		K_z:			(0,1),
		K_x:			(0,2),
		K_c:			(0,3),
		K_v:			(0,4),
		K_b:			(0,5),
		K_n:			(0,6),
		K_m:			(0,7),
		K_COMMA:		(0,8),
		K_PERIOD:		(0,9),
		K_SLASH:		(0,10),
		K_a:			(1,1),
		K_s:			(1,2),
		K_d:			(1,3),
		K_f:			(1,4),
		K_g:			(1,5),
		K_h:			(1,6),
		K_j:			(1,7),
		K_k:			(1,8),
		K_l:			(1,9),
		K_SEMICOLON:	(1,10),
		K_QUOTE:		(1,11),
		K_q:			(2,1),
		K_w:			(2,2),
		K_e:			(2,3),
		K_r:			(2,4),
		K_t:			(2,5),
		K_y:			(2,6),
		K_u:			(2,7),
		K_i:			(2,8),
		K_o:			(2,9),
		K_p:			(2,10),
		K_LEFTBRACKET:	(2,11),
		K_RIGHTBRACKET:	(2,12),
		K_1:			(3,1),
		K_2:			(3,2),
		K_3:			(3,3),
		K_4:			(3,4),
		K_5:			(3,5),
		K_6:			(3,6),
		K_7:			(3,7),
		K_8:			(3,8),
		K_9:			(3,9),
		K_0:			(3,10),
		K_MINUS:		(3,11),
		K_EQUALS:		(3,12)
	}

	
def sine_array_onecycle(hz, peak, samp_rate):
	length = samp_rate / float(hz)
	omega = numpy.pi / length
	xvalues = numpy.arange(int(length)) * omega
	return (peak * numpy.sinh(xvalues))
    
def sine_array(hz, peak, n_samples, samp_rate):
    return numpy.resize(sine_array_onecycle(hz, peak, samp_rate), (n_samples, 2))
	
sound_func = None

def sound_funcle(key_info, samp_rate, length):
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
		
		#print f
		sound = pygame.sndarray.make_sound(sine_array(f, 1.0, duration_in_samples, samp_rate))
		#print "playing"
		channel = sound.play()
		if channel:
			channel.set_volume(0.7, 0.3)
		
		sound = pygame.sndarray.make_sound(sine_array(f2, 0.7, duration_in_samples, samp_rate))
		channel = sound.play()
		if channel:
			channel.set_volume(0.2, 0.5)
