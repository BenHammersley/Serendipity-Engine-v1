#!/usr/bin/perl -w
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use IMDB::Film;
use Lyrics::Fetcher;
use WWW::Wikipedia;
use Lingua::Translate;
use JSON::PP;
use LWP::Simple;
use Lingua::StopWords qw(getStopWords);
use List::Util qw/shuffle/;
#use Device::SerialPort;
#my $port = Device::SerialPort->new("/dev/tty.usbmodem1a21");


my $cgi = CGI->new();
my $name = $cgi->param("name");

#Film lookup on IMDB
my $film = $cgi->param("film");
my $imdbobj = new IMDB::Film (crit => "$film", debug => 1);
my $filmplot = ($imdbobj->storyline());
my @plotwords = ($filmplot =~ /(\w+)/g);
my $tenplotwords = join ' ', @plotwords[0..10];


#Lyrics lookup from song
my $song = $cgi->param("song");
my $artist = $cgi->param("artist");
my $songlyrics = Lyrics::Fetcher->fetch("$artist", "$song");
my @songwords = ($songlyrics =~ /(\w+)/g);
my $tensongwords = join ' ', @songwords[0..5];

#Subject lookup on Wikipedia
my $subject = $cgi->param("subject");
my $wiki = WWW::Wikipedia->new();
my $wikiobj = $wiki->search("$subject");
my $subjectsummary = $wikiobj->text();
my @subjectwords = ($subjectsummary =~ /(\w+)/g);
my $tensubjectwords = join ' ', @subjectwords[60..65];
my $subjectrelated = $wikiobj->related();


#Father Subject lookup on Wikipedia
my $father = $cgi->param("father");
my $fwiki = WWW::Wikipedia->new();
my $fwikiobj = $wiki->search("$father");
my $fsubjectsummary = $fwikiobj->text();
my @fsubjectwords = ($fsubjectsummary =~ /(\w+)/g);
my $tenfsubjectwords = join ' ', @fsubjectwords[150..153];

#Mother Subject lookup on Wikipedia
my $mother = $cgi->param("mother");
my $mwiki = WWW::Wikipedia->new();
my $mwikiobj = $wiki->search("$mother");
my $msubjectsummary = $fwikiobj->text();
my @msubjectwords = ($msubjectsummary =~ /(\w+)/g);
my $tenmsubjectwords = join ' ', @msubjectwords[30..35];

my @locations = ('at a cafe', 'while flying', 'at home', 'at a gym', 'in a street you have never been before', 'in a familiar place', 'in a public place', 'in a field', 'at a friends');
my $location = $locations[int rand($#locations)];

my @context1s = ('with friends', 'alone', 'with strangers', 'with family', 'with a secret crush', 'with a shopkeeper', 'with a pet', 'with an acquaintance', 'with an unrequited love', 'with an enemy', 'with a person with violet eyes');
my $context1 = $context1s[int rand($#context1s)];

my @context2s = ('drinking', 'smoking', 'kissing', 'exercising', 'dancing', 'starting into space','sleeping','walking a friendly dog','playing an instrument','having a coffee', 'looking in the mirror', 'mediatating', 'tidying');
my $context2 = $context2s[int rand($#context2s)];

my @lowhigh = ('LOW', 'HIGH', 'WANTING');
my $lowhigh1 = $lowhigh[int rand($#lowhigh)];
my $lowhigh2 = $lowhigh[int rand($#lowhigh)];
my $lowhigh3 = $lowhigh[int rand($#lowhigh)];
my $lowhigh4 = $lowhigh[int rand($#lowhigh)];


#my $x18r = Lingua::Translate->new(src => "en", dest => "de");
my $english = $tenfsubjectwords.$tenplotwords.$tensongwords.$tensubjectwords.$subjectrelated.$tenmsubjectwords;
#my $german = $x18r->translate($english);

#my $x18r2 = Lingua::Translate->new(src => "de", dest => "en");
#my $english2 = $x18r2->translate($german);

#my $german2 = $x18r->translate($english2);
#my $english3 = $x18r2->translate($german2);

my $stopwords = getStopWords('en');
my @words = ($english =~ /(\w+)/g);
my $chosenwords = 4;
my @chosen = (shuffle(@words))[0..$chosenwords-1];
my $displaytext = join ' ', grep { !$stopwords->{$_} } @chosen;


#######
## Access the Suitcase Arduino
#######

# Not happy about this fixed IP here, but hey ho
my $suitcaseJSON = get("http://192.168.2.177/analogReadJSON/all/");
my $suitcasetext = "You would benefit from paying more attention to the suitcase." unless defined $suitcaseJSON;

my $json = JSON::PP->new;
my $decodedJSON = $json->decode($suitcaseJSON);

# I'm guess here, before I go and get some midget gems
my $switchzero  = $decodedJSON->{"0"};
my $switchone   = $decodedJSON->{"1"};
my $switchtwo   = $decodedJSON->{"2"};
my $switchthree = $decodedJSON->{"3"};
my $switchfour  = $decodedJSON->{"4"};

my $switchzerotext = "You are unclear.";
my $switchonetext = "You are confused.";
my $switchtwotext = "You are giving me mixed signals.";
my $switchthreetext = "You are befuddling.";


if ($switchzero > 500) 
	{ 
	$switchzerotext = "Have you ever read Sartre? You would probably think he is overrated. That might be an answer in itself.";
	}	else	{ 
	$switchzerotext = "The Serendipity Engine wonders if you have a connection to Spain in some way?";
	}

if ($switchone > 500) 
	{ 
	$switchonetext = "You need more sleep. We all do. Admit it.";
	}	else	{ 
	$switchonetext = "You feel perky. Oh so perky. But beware the crash.";
	}

if ($switchtwo > 500) 
	{ 
	$switchtwotext = "You might be feeling a little jittery. Try to relax.";
	}	else	{ 
	$switchtwotext = "You're more of a traditionalist. Try something new.";
	}

if ($switchthree > 500) 
	{ 
	$switchthreetext = "You're a natural optimist, but sometimes you secretly feel insecure. You should confide in someone.";
	}	else	{ 
	$switchthreetext = "You inspire with your grit, and take pride in your tenacity. Serendipity will come when you allow yourself to be vulnerable.";
	}



#$port->baudrate(9600); # you may change this value
#$port->databits(8); # but not this and the two following
#$port->parity("none");
#$port->stopbits(1);


#$port->write("Hello $name \n\n\n");
#$port->write("Your Serendipity\n");
#$port->write("Recipe Is\n\n\n");
#$port->write("$displaytext\n");

#$port->write("Think about this\n");
#$port->write("$location\n");
#$port->write("$context1\n");
#$port->write("$context2\n");


print "Content-type: text/html\n\n";
print <<EOM;
<html>
<head>
<title>Serendipity Engine, The Prescription</title></head>
<link rel="stylesheet" type="text/css" href="styles.css"/>
<body>
<h1>Your Serendipity Recipe</h1>
<p>Hello, $name. Thank you for using the Serendipity Engine. Based on an analysis of your answers to the questions, plus your selections in the suitcase, the Serendipity Engine has determined that you are $lowhigh1 in social support, $lowhigh2 in creativity, $lowhigh3 in physical well being. You are $lowhigh3 in Head-RAM(tm), $lowhigh1 in attention and $lowhigh2 in access to knowledge. You are $lowhigh1 in Grit. Do not worry about any of this. Think on it. And go to theserendipityengine.com to find out more about the science behind these scales.</p>

<p>$switchzerotext $switchonetext $switchtwotext $switchthreetext</p>

<p>In addition, the Engine's Human Task Force has identified, based on your portrait and your drawings, your level of personal attractiveness and elegance.</p>

<p>Finally, the Serendipity Engine prescribes the following tailor-made Serendipity Mediation Koan to be considered $location, while $context1 $context2:</p>

<h2></h2>
<div id="recipe">
<p>$displaytext</p>
</div>
EOM
exit;