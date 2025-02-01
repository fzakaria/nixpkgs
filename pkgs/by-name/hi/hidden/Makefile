all: hidden public

hidden: example.o
	$(CC) $(LDFLAGS) -o $@ $^ -lhidden

public: example.o
	$(CC) $(LDFLAGS) -o $@ $^ -lpublic

example.o: example.c
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	rm -f hidden public *.o

.PHONY: all clean
