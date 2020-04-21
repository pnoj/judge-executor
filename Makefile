build: $(runtime)
	cp files/* runtimes/$(runtime)/
	echo build
	for file in files/*
	do
	    echo delete runtime/$(runtime)/$(file)
	done
