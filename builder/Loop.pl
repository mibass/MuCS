#!/usr/bin/perl

use strict;
use warnings;
my $folder = shift;
my $binfile;
my $outfile;
my $ext="/uboone/app/users/kalousis/MuCS/builder/";

my @files = <${folder}/*.bin>;
print "Found " . ($#files+1) . " files.\n";    


foreach $binfile (@files){
    $outfile = $binfile;
    $outfile =~ s|bin$|root|g;
    print "Building NTuple on $binfile...\n";
    print "created file : $outfile \n";
    system qq|${ext}/ChipProgram $binfile $outfile|;
}
