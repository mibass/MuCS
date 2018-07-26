#!/usr/bin/perl

use strict;
use warnings;

my $cnt=shift;
my $max_processes=shift; # Change this to limit number of batch jobs running at any one time 

my ($sec,$min,$hour,$day,$month,$yr19,@rest,@timetag);

for(my $i=0; $i<22; $i++) { # Look back up to three weeks
    ($sec,$min,$hour,$day,$month,$yr19,@rest) = localtime(time-$i*24*60*60);
    $yr19 =$yr19+1900;
    $month = sprintf("%02d",${month}+1);
    $day = sprintf("%02d",$day);
    $hour = sprintf("%02d",$hour+1);
    $timetag[${i}]="$yr19$month$day";
}

my $path = "/uboone/data/users/kalousis/MuCS/data/"; 

#"/data1/mega_mini_data_2013/"; # path to scripts and data

my $lab = ""; # folder in path where data lives

my ($folder,$run);

#system qq|ls -ls --time-style=long-iso "${path}/${lab}" > "${path}/${lab}/mucs_temp"|;
system qq|ls -ls --time-style=long-iso "${path}/${lab}" > "/tmp/mucs_temp"|;

my @folderlist;

#open IN, "${path}/${lab}/mucs_temp";
open IN, "/tmp/mucs_temp";
while(<IN>){
    if(/.*Run_(\d{8})_(\d+)$/) { 
	foreach(@timetag) {   
	    if($1 eq $_) { push(@folderlist,"$1"."_$2"); }
	}
    }
}
close IN;

foreach (@folderlist) {
    print "$_\n";
}

my ($temp,@processlist);

for(my $j=0; $j<=$#folderlist; $j++) {# $runnumber (@folderlist) {

    my @files;


    $temp = "$path/$lab/Run_$folderlist[$j]/signal_*.root"; # Run already being processed

    push(@files,<${temp}>);

    $temp = "$path/$lab/Run_$folderlist[$j]/*.filepart";    # Data is still being copied over

    push(@files,<${temp}>);

    $temp = "$path/$lab/Run_$folderlist[$j]/*.log";         # Data being processed 

    push(@files,<${temp}>);

    $temp = "$path/$lab/Run_$folderlist[$j]/USB_*/signal_*.root";         # Data being processed 

    push(@files,<${temp}>);

    $temp = "$path/$lab/Run_$folderlist[$j]/USB_*/*.filepart";         # Data being processed 

    push(@files,<${temp}>);

    $temp = "$path/$lab/Run_$folderlist[$j]/USB_*/*.log";         # Data being processed 
    
    push(@files,<${temp}>);

    if($#files == -1) {push(@processlist,"Run_$folderlist[$j]");}

    undef @files;
}

#print "Processing the first 2 of the following runs:\n";
foreach (@processlist) {
    print "$_\n";
}

#system qq|rm "${path}/${lab}/mega_mini_temp"|;

#my $cnt=0;

my @files0;

foreach $run (@processlist) {
    #$cnt++;
	$folder = "${path}/${lab}/${run}/USB_*";
	my @USBnumber = <${folder}>;
	my $totalusbfound = $#USBnumber + 1;
	print "\n Found RUN $run with $totalusbfound USB data file. Processing data in background.\n";
        foreach $folder (@USBnumber){
	    if($cnt<$max_processes) {
		if(-d "$folder") {
		    print "Creating log file ${folder}/${run}.log...\n";
		    @files0 = <${folder}/signal*.bin>;
		    system qq|/uboone/app/users/kalousis/MuCS/builder/auto_register ${folder} ${run} $#files0 &|;
		    # print "\n Found $#files0 signal files \n";
		    system qq|nohup /usr/bin/perl /uboone/app/users/kalousis/MuCS/builder/Loop.pl ${folder} > ${folder}/${run}.log &|;
		    $cnt++;  #count number of submitted jobs
		}
		else {
		    print "$folder not found. Skipping...\n";
		}
	    }
	}
}
