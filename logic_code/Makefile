CPPC=g++
CFLAGS=-I/usr/include/python3.4m
LDLIBS=-lpython3.4m

DEPS=defines.hpp logic_util.hpp

OBJPATH=obj
SRCPATH=src
BINPATH=bin

$(OBJPATH)/%.o: $(SRCPATH)/%.cpp
	$(CPPC) $(CFLAGS) -c -o $@ $<

$(BINPATH)/logic: $(OBJPATH)/logic.o $(OBJPATH)/ai.o $(OBJPATH)/map.o $(OBJPATH)/kernelTL.o
	$(CPPC) -o $@ $^ $(LDLIBS)


