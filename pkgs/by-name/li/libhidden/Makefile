# Compiler and flags
CFLAGS = -fPIC -Wall -Wextra -O2
HIDDEN_CFLAGS = $(CFLAGS) -fvisibility=hidden
LDFLAGS = -shared

# Output shared libraries
HIDDEN_TARGET = libhidden.so
PUBLIC_TARGET = libpublic.so

# Source files
SRCS = example.c
HIDDEN_OBJS = $(SRCS:.c=.hidden.o)
PUBLIC_OBJS = $(SRCS:.c=.public.o)

.PHONY: all clean

# Default target builds both versions
all: $(HIDDEN_TARGET) $(PUBLIC_TARGET)

# Build the hidden visibility shared library
$(HIDDEN_TARGET): $(HIDDEN_OBJS)
	$(CC) $(LDFLAGS) -o $@ $(HIDDEN_OBJS)

# Build the public visibility shared library
$(PUBLIC_TARGET): $(PUBLIC_OBJS)
	$(CC) $(LDFLAGS) -o $@ $(PUBLIC_OBJS)

# Compile object files for hidden version
%.hidden.o: %.c
	$(CC) $(HIDDEN_CFLAGS) -c $< -o $@

# Compile object files for public version
%.public.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean build artifacts
clean:
	rm -f $(HIDDEN_OBJS) $(PUBLIC_OBJS) $(HIDDEN_TARGET) $(PUBLIC_TARGET)