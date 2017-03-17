from sound import Sound
from pocketsphinx import LiveSpeech
import time


#function for decreasing volume where input is speed
def decrease(inputspeed):
	#while current volume is not desired volume
	#decrease volume at rate according to speed
	speed = int(inputspeed)
	count = 0
	if speed == 1:
		while count <= 15:
			#1 second reduction for 15 bars
			Sound.volume_down()
			time.sleep(1 / 15)
			count += 1
	elif speed == 3:
		while count <= 15:
			#3 second reduction for 15 bars
			Sound.volume_down()
			time.sleep(3 / 15)
			count += 1
	elif speed == 5:
		while count <= 15:
			#5 second reduction for 15 bars
			Sound.volume_down()
			time.sleep(5 / 15)
			count += 1

def instant_decrease():
	Sound.volume_set(10)

#reset volume 
def normalize():
	Sound.volume_set(40)



if __name__ == "__main__":

	#set initial volume to 20 bars
	normalize()

	while(1): #while listening
		#
		print("Choose a decrease speed: 0 1 3 5")
		print("To return to original type norm")
		print("To stop type exit")
		print("To trigger vol decrease if speech isn't recognized ^C")
		option = input("> ")
		print("")
		if (option == "0" or option == "1" or option == "3" or option == "5"):
			speech = LiveSpeech(lm=False, keyphrase='hey', kws_threshold=1e+20)
			for phrase in speech:
				print(phrase)
				break
			if option == "0":
				instant_decrease()
			else:
				decrease(option)
			continue
		if option == "norm":
			normalize()

		if option == "exit":
			exit(0)
