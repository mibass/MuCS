
#
# mega-micro code makefile
#
# author: Leonidas N. Kalousis
#

# files

srcs = mega_micro_code_a.cc

objs = $(srcs:.cc=.o)

exe = $(srcs:.cc=)

# libs

cxx = g++

cxxflags = -g -W -O -Wall -Wno-deprecated -fPIC 

cxxflags += -I$(ROOTSYS)/include/ 

rootlibs = $(shell root-config --glibs) -lMinuit -lMinuit2

# targets

all	: start $(exe) end

start	: 
	@echo ''		
	@echo ' * mega-micro code make ... '
	@echo ''
	@rm -f ./#* ./*~ ./*.*~	

$(exe)	: $(objs) 
	@$(cxx) $(rootlibs) $(cxxflags) -o $@ $^
	@echo ' * building ( exe )  :' $@
	@echo ''

%.o	: %.cc	
	@$(cxx) $(cxxflags) -c -o $@ $<
	@echo ' * building ( objs ) :' $@
	@echo ''

end	:
	@echo ' * make done !'
	@echo ''

clean	:	
	@echo ''	
	@echo ' * make clean ...'
	@echo ''		
	@rm -f ./#* ./*~ ./*.*~ *.o $(exe)
