#!/usr/bin/env perl
use warnings;

use File::Basename;
use LWP::Simple;
#$query = 'chimpanzee[orgn]+AND+biomol+mrna[prop]';
$query = "\"".$ARGV[0]."\"[TITLE]+AND+prokaryotes[organism]"; # query comes from first argument
$db = $ARGV[1]; # database comes from second argument # eg.: protein
$file_out = $ARGV[2]; # output name comes from third argument
$dir = $ARGV[3]; # output directory

print("QUERY  : ".$query."\n");
print("DATABASE: ".$db."\n");
print("OUTPUT : ".$file_out."\n");

#assemble the esearch URL
$base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
$url = $base . "esearch.fcgi?db=$db&term=$query&usehistory=y";


print("URL: ".$url."\n");

#post the esearch URL
$output = get($url);


#parse WebEnv, QueryKey and Count (# records retrieved)
$web = $1 if ($output =~ /<WebEnv>(\S+)<\/WebEnv>/);
$key = $1 if ($output =~ /<QueryKey>(\d+)<\/QueryKey>/);
$count = $1 if ($output =~ /<Count>(\d+)<\/Count>/);

if(defined $count){
	print("RESULTS: ".$count."\n");
	if($count == 0){print("END\n\n"); exit();};
} else {
	print("RESULTS: ERROR\n");
	exit();
}


# parse file name
$file_out = basename($file_out);
$complete_out = "$dir"."$file_out".".faa"; 

print($complete_out."\n");

#open output file for writing
open(OUT, ">$complete_out") || die "Can't open file!\n";

#retrieve data in batches of 500
$retmax = 500;

for ($retstart = 0; $retstart < $count; $retstart += $retmax) {
        $efetch_url = $base ."efetch.fcgi?db=$db&WebEnv=$web";
        $efetch_url .= "&query_key=$key&retstart=$retstart";
        $efetch_url .= "&retmax=$retmax&rettype=fasta&retmode=text";
        $efetch_out = get($efetch_url);
		if(defined $efetch_out){
			print OUT "$efetch_out";
		}
}
close OUT;

print("END\n\n");
