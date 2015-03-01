import Queue


def snapshot(queue_name): 
	if queue_name.empty():
		print "%s is empty." %queue_name

	for process in list(queue_name.queue):
		print process


def main():

	print ("Hello \n Goodbye")

if __name__ == '__main__':
	main()