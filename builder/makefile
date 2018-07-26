
srcs = auto_analyser.cxx

objs = $(srcs:.cxx=.o)

exe = $(srcs:.cxx=)

cxx = g++

cxxflags = -g -W -O -Wall -Wno-deprecated -fPIC 

cxxflags += -I$(ROOTSYS)/include/ 

rootlibs = $(shell root-config --glibs) -lMinuit -lMinuit2

all	: start $(exe) end

start	: 
	@echo ''		
	@echo ' * make ... '
	@echo ''
	@rm -f ./#* ./*~ ./*.*~	

$(exe)	: $(objs) 
	@$(cxx) $(rootlibs) $(cxxflags) -o $@ $^
	@echo ' * building ( exe )  :' $@
	@echo ''

%.o	: %.cxx	
	@$(cxx) $(cxxflags) -c -o $@ $<
	@echo ' * building ( obj ) :' $@
	@echo ''

end	:
	@echo ' * make done !'
	@echo ''

clean	:	
	@echo ''	
	@echo ' * make clean ...'
	@echo ''		
	@rm -f ./#* ./*~ ./*.*~ *.o $(exe)
