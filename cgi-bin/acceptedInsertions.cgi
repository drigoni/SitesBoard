#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI;

require 'functions/session_function.cgi';
require 'functions/function.cgi';

#prendo eventuali parametri in ingresso con il GET
my $cgi = new CGI;
my $msgParam = $cgi->param('msgError');

my $session=getSession();
if($session == undef)
{
    print redirect(-url => 'login.cgi');
}

my $userName=getUsername($session);

utf8::encode($userName);


my $cgi = new CGI;
my $index = $cgi->param('index');
if(!defined($index)) { $index=0; }

my $nElementi=5;
my @board=getAcceptedAd($userName);
my $size=scalar @board;
my @annunciAccettati=getBoardSplit($index,$nElementi,\@board);

$index_successivo=$index+$nElementi;
$index_precedente=$index-$nElementi;

if($index_precedente<0){ $index_precedente=0; }



print "Content-type: text/html\n\n";

print <<PRIMA_PARTE;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
		<title>Annunci Accettati - SitesBoard</title> 

		<link href="../css/screen.css" rel="stylesheet" type="text/css" media="screen and (min-width:800px)"/>
		<link href="../css/handheld.css" rel="stylesheet" type="text/css" media="handheld, screen and (max-width:800px)" />
		<link href="../css/print.css" rel="stylesheet" type="text/css" media="print"/>
		<!--[if lt IE 9]>
			<link href="../css/screen.css" rel="stylesheet" type="text/css" media="screen"/>
			<link href="../css/print.css" rel="stylesheet" type="text/css" media="print"/>
		<![endif]-->


		<!-- Meta Tag -->
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta name="title" content="Annunci Accettati - SitesBoard" />
		<meta name="author" content="Davide Rigoni, Francesco Fasolato, Giacomo Zecchin, Antonino Macrì" />
		<meta name="description" content="Pagina degli annunci accettati dall'utente loggato" />
		<meta name="keywords" content="Annunci, Logged, Siti, Web" />
		<meta name="language" content="italian it" />
	</head>
	<body>
				<div class="screen_reader"><a href="#contents" hreflang="it" type="text/html">Se desideri saltare al contenuto segui questo collegamento</a></div>
		<div id="container">
			<!-- HEADER  -->
			<div id="header">
				<a href="home.cgi" hreflang="it"><img id="header_logo" src="../media/logo.png" alt="Logo del sito SitesBoard" title = "Logo del sito"/></a>
				<h1>SitesBoard</h1>
				<h2>La <span xml:lang="en" lang="en">Sites Board</span> per richiedere Siti <span xml:lang="en" lang="en">Web</span></h2>

PRIMA_PARTE


my $username = getSessionUsername($session);
utf8::encode($username);

print <<EOF;


				<!-- Da caricare nel caso l utente sia loggato (se è qui sicuramente ha una sessione valida, altrimenti viene redirectato a login.cgi) -->

				<div id="header_login">
					<div>
						Benvenuto <span class="notable">$username</span>
					</div>
					<div>
						<div class="edit" ><a href="profile.cgi"  id="img_P" hreflang="it" type="text/html">Il tuo profilo</a></div>
						<div class="edit" ><a href="logout.cgi" id="img_EL" hreflang="it" type="text/html">Esci</a></div>
					</div>
				</div>
			</div>

			<!-- PATH  -->
			<div id="path" title="Sezione del sito in cui ti trovi in questo momento">
				Ti trovi in: <span class="notable">Annunci Accettati</span>
			</div>

			<div id="nav_panel">
				<!-- MENÙ DI NAVIGAZIONE -->
				<div id="nav_menu" class="menu" title ="Menù di navigazione del sito">
					<h3>Menù</h3>
					<ul>
						<li><a href="home.cgi" hreflang="it" ><span xml:lang="en" lang="en">Home Page</span></a></li>
						<li><a href="eCommerce.cgi" hreflang="it" >Tipologia <span xml:lang="en" lang="en">E-commerce</span></a></li>
						<li><a href="forum.cgi" hreflang="it" >Tipologia <span xml:lang="en" lang="en">Forum</span></a></li>
						<li><a href="social.cgi" hreflang="it" >Tipologia <span xml:lang="en" lang="en">Social</span></a></li>
						<li><a href="personali.cgi" hreflang="it" >Tipologia Personali</a></li>
						<li><a href="aziendali.cgi" hreflang="it" >Tipologia Aziendali</a></li>
						<li><a href="blog.cgi" hreflang="it" >Tipologia <span xml:lang="en" lang="en">Blog</span></a></li>
						<li><a href="siteMap.cgi" hreflang="it" ><span xml:lang="en" lang="en">Sitemap</span></a></li>
					</ul>
				</div>

				<!-- MENÙ DI AMMINISTRAZIONE-->
				<div id="nav_administration" class="menu" title="Menù di amministrazione del sito">
					<h3>Amministrazione</h3>
					<ul>
						<li><a href="addInsertions.cgi" hreflang="it" type="text/html">Nuova Inserzione</a></li>
						<li><a href="showInsertions.cgi" hreflang="it" type="text/html">Inserzioni Inserite</a></li>
						<li class="current_pageL">Inserzioni Accettate</li>
					</ul>
				</div>
			</div>

			<!-- Contenuti della pagina -->
			<div id="contents">

				<h3><span xml:lang="it" lang="it">Qui sono presenti gli annunci per cui ti sei candidato.</span></h3>
				<div id="cont_annunci">

					<p class="underline">
						Questi sono gli annunci che hai accettato.
					</p>
					<!-- Messaggio di errore  -->
					<p id="cont_msg" class="msgError" title="Messaggio di errore">
EOF
if(defined($msgParam))
{
	print $msgParam;
}
					print "</p>";
					print '<ul id="block_insertions">';
					for (my $i=0; $i <scalar(@annunciAccettati); $i++) {
						$titolo=$annunciAccettati[$i][0];
						$oggetto=$annunciAccettati[$i][1];
						$tipologia=$annunciAccettati[$i][2];
						$data=$annunciAccettati[$i][3];
						$autore=$annunciAccettati[$i][4];
						$id_annuncio=$annunciAccettati[$i][5];
						$id_persona=$annunciAccettati[$i][6];

						#$tipologia accessibile
						$tipologia=addSpan($tipologia);
					
						utf8::encode($titolo);
						utf8::encode($oggetto);
						utf8::encode($tipologia);
						utf8::encode($data);
						utf8::encode($autore);
						utf8::encode($id_persona);
						utf8::encode($id_annuncio);
					
						print "<li>
									<dl class='block_insertion'>
										<dt>Titolo:</dt>
										<dd><a href='insertion.cgi?idUser=$id_persona&amp;idInsertion=$id_annuncio'>$titolo</a></dd>
										<dt>Tipologia:</dt>
										<dd>$tipologia</dd>
										<dt>Oggetto:</dt>
										<dd>$oggetto</dd>
										<dt>Autore:</dt>
										<dd><a href='userProfile.cgi?user=$autore'>$autore</a></dd>
										<dt>Data:</dt>
										<dd>$data</dd>
									</dl>
								</li>";
				}
print <<FINE;
					</ul>
FINE
if($index_precedente>=0 && $index ne 0){
	print "<a href='acceptedInsertions.cgi?index=$index_precedente' id='BI_PN' hreflang='it' type='application/xhtml+xml'>Precedente</a>";
}

if($index_successivo<$size){
	print "<a href='acceptedInsertions.cgi?index=$index_successivo' id='BI_PN' hreflang='it' type='application/xhtml+xml'>Successiva</a>";
}

print <<FINE;
				</div>


			</div>

			<!-- Div necessario per spostare il footer in fondo alla pagina -->
			<div id="push_block">
			</div>
		</div>




		<!-- FOOTER -->
		<div id="footer">
			<span title="Pagina validata con lo standard XHTML 1.0 Strict">
			    <a href="http://validator.w3.org/check?uri=referer" hreflang="en" >
			    	<img class="img_validator" src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>
			</span>
			<span title="CSS della pagina validato secondo lo standard CSS2">
				<!--hrflang varia a seconda dello stato -->
			    <a href="http://jigsaw.w3.org/css-validator/check/referer" > 
			        <img class="img_validator" src="http://jigsaw.w3.org/css-validator/images/vcss" alt="CSS Valido!" /></a>
			</span>
			<span title="Accessibile secondo lo standard WCAG2 Livello AA">
			    <a href="http://www.w3.org/WAI/intro/wcag"  hreflang="en-US">
			        <img class="img_validator" src="https://www.totalvalidator.com/images/valid_n_wcag2_aa.gif" alt="Pagina accessibile" />
			    </a>
			</span>
		</div>
	</body>
</html>
	
FINE
exit;
