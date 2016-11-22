#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2016
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/matelook/

use CGI qw/:all/;
use CGI::Cookie;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

use DateTime;
use Cwd;
use File::Spec;




$content = "";
sub main() {



    $status = $status || 0;
    $status = param("status") || 0;
    # print start of HTML ASAP to assist debugging if there is an error in the scrip

    #print page_header();
    $content .= page_header();
  
    
    # Now tell CGI::Carp to embed any warning in HTML
    warningsToBrowser(1);   
    # define some global variables
    $debug = 1;

    #$users_dir = "dataset-small";
    $users_dir = "dataset-medium";
    $SearchzNum = param(SearchzNum);
    @users = sort(glob("$users_dir/*"));


#Login
    Login();
    

    MakingProfile();
    MakingPosts();
    MakingComment();
    MakingReply();
#

#

#
   

    if(defined $SearchzNum)
    {
	$status = 1;
    }

    if(defined param(NewAccount))
    {
	$status = 2;
    }

 
    if($status == 1)
    {
	#print Search_page();
	$content .= Search_page();
    }
    if($status == 0)
    {
	$content .= user_page();
	
    }


    if($status == 2)
    {
	$content .= NewAccount_page();
    }

    #print page_trailer();
    $content .= page_trailer();

    if(!defined $user)
    {
	$user = "";
    }
print header(-cookie=>["logFlag=$logFlag","user=$user"]);

print $content;
}

sub Login(){

    %cookies = fetch CGI::Cookie;
    
    if(! defined $user)
    {
	$user = param("user") || "";
    }
    $username = param('username') || '';
    $password = param('password') || '';
    $logFlag = 0;
    $logFlag = param('logFlag') || 0;
    $logFlag = $cookies{'logFlag'}->value if defined $cookies{'logFlag'};
    $user = $cookies{'user'}->value if defined $cookies{'user'};
    #$zNum = $cookies{'zNum'}->value if defined $zNum{'zNum'};

    my $count = 0;

#Check whether the Logout Button clicked
    $LogoutButtonFlag = param(LogoutFlag) || "";
    if($LogoutButtonFlag eq "Logout")
    {
	$logFlag = 0;
	$user = "";
    }
    $LogoutButtonFlag = "";

#


 



#
    #$content .= "####$logFlag####";
    if($logFlag ==  1)
    {
	$content .= $username;

    }else{
    if ($username && $password)
    {
	if(!open F, "$users_dir/$username/user.txt")
	{
	    $content .= 'Unknown username!';
	}
	else
	{ 
	    while($line = <F>)
	    {
		if($line =~ /password.*/)
		{
		    $line =~ s/password\=//gi;
		    if($line !~ /$password/)
		    {
			$content .= 'Incorrect password!';
			$content .= $line;
		    }
		    else
		    {

			$content .= "$username authenticated.\n";
			#$content .= $username;
			$zNum = $username;
			#
			$user = $username;
                        #
			$logFlag = 1;

			$content .= start_form;

			$content .= hidden("logFlag",$logFlag);
		    }
		}
	    }
		close F;
	}
    }
    else 
    {
	$content .= start_form;
	if($username)
	{
	    $content .= hidden("username",$username);
	    $username = param('username');
	    $count++;	    
	}
	else
	{
	    $content.= "Username:\n". textfield('username'). "\n";
	}
	if($password)
	{
	    $content.= hidden("password",$password);
	    $password = param('password');
	    $count++;
	}
	else
	{
	    $content .= "Password:\n".textfield('password')."\n";
	}
	
	
	if ($count eq 2)
	{
	    if(!open F, "$users_dir/$username/user.txt")
	    {
		$content .= 'Unknown username!';
	    }
	    else
	    { 
		$content .= "$username authenticated.\n";
		$zNum = $username;

		#$content .= $logFlag;

		$content .= hidden("logFlag",$logFlag);
	    }
	}

	$content .= submit(value => Login);
	
	$content .= end_form;
    }
    }

}




sub Initialize(){




}




sub Addmate{
    $FriendButton = param("Friend") || 0;
    $UnFriendButton = param("UnFriend");

    #$content.= $user;
    #$content.=$zNum;
    if($logFlag == 1 && $FriendButton eq "Friend")
    {
	$content .= "ADD!";
	$content .= $FriendButton;

	$user_to_show = "$users_dir/$user";
	my $dir = "$user_to_show/posts/New";

	my $filename = "$user_to_show/user.txt";

	open my $in,  '<',  $filename      or die "Can't read old file: $!";
	open my $out, '>', "$filename.new" or die "Can't write new file: $!";

	while($line = <$in> )
	{
	    if($line =~ /^mates(.*)\].*/)
	    {
		if($line !~ /.*$zNum.*/)
		{
		    $line =~ s/\]/\, $zNum\]/gi;
		}
	    }	
	    #print $out $_;
		print $out $line;
	}
	
	close $out;

	rename("$filename.new", "$filename");
	
    }
    
    if($logFlag == 1 && $UnFriendButton eq "UnFriend")
    {
	$content .= "Delete";

	my $user_to_show = "$users_dir/$user";
	my $dir = "$user_to_show/posts/New";
	
	my $filename = "$user_to_show/user.txt";
	
	open my $in,  '<',  $filename      or die "Can't read old file: $!";
	open my $out, '>', "$filename.new" or die "Can't write new file: $!";
	
	while($line = <$in> )
	{
	    if($line =~ /^mates(.*)\].*/)
	    {
		    $line =~ s/$zNum, //gi;
		    $line =~ s/, $zNum//gi;
	    }	
	    #print $out $_;
	    print $out $line;
	}
	
	close $out;
	
	rename("$filename.new", "$filename");
	

       
    }



#perl change a line in file


}

sub MakingProfile(){
    if(!defined $user_to_show)
    {
	    if(!defined $user)
	    {
		$user = "";
	    }
	$user_to_show = "$users_dir/$user";
    }
    $others = param("others");
    #$content .= param(Saveothers);
    if(defined $others && defined param(Saveothers))
    {


	my $otherfile = "$users_dir/$user/others.txt";	
	$content .= $otherfile;
	if(! -e $user_to_show)
	{
	    my $dir = "$user_to_show";
	    mkdir $dir;
	}
	my $filename = $otherfile;
	open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
	print $fh "$others","\n";
	close $fh;
	


    }
#<textarea rows="2" cols="4" name="others">
#</textarea>
#<input type="submit" name = "Saveothers" value="Save" class="matelook_button">

}


sub MakingPosts(){

    #$content .=   start_form, "\n",
    #textarea(-name=>'content', -rows=>10,-cols=>60), "\n",
    #p, submit('Save'), "\n",
    #end_form, "\n",
    #end_html;

    $NewPost = param('NewPost');

    if(!defined $zNum)
    {
	$zNum = param('zNum0');
	if(!defined $zNum)
	{
	    $zNum = param('zNum') || "z3275760";
	}
	$zNum =~ s/[\x0A\x0D]//g; 
	$zNum =~ s/%0D%0A//g;
    }

    if(defined param(SavePost))
    {
	my $user_to_show = "$users_dir/$zNum";
	my $dir = "$user_to_show/posts/New";
	mkdir $dir;
	#mkdir( $dir ) or die "Couldn't create $dir directory, $!";
	my $filename = "$user_to_show/posts/New/post.txt";
	open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
	print $fh "from=$zNum","\n";
	print $fh "message = $NewPost\n";
	print $fh "time=";
	close $fh;
    }

}

sub MakingComment(){
    $NewComment = param("comment");
    $ComRou = param("ComRou");
    #$content .= $ComRou;
 



    if(defined $NewComment && defined param('CommentButton'))
       {
	   my $user_to_show = "$users_dir/$user";
	   
	   my $dir = "$ComRou/New";
	   mkdir $dir;
	   #mkdir( $dir ) or die "Couldn't create $dir directory, $!";
	
	   #my $filename = "$dir/comment.txt";


	   my $filename = "$ComRou/New/comment.txt";
	   open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
	   print $fh "from=$user","\n";
	   print $fh "message=$NewComment\n";
	   print $fh "time=";
	   close $fh;
	
       }
#"<form><textarea row = '4' cols = '30' name></textarea><input type='submit' value='comment' name='CommentButton' class='matelook_button'></form>"

}


sub MakingReply{
    $NewReply = param("reply");
    $RepRou = param("RepRou");
    
    #$content .= $RepRou . "ddddddddddddddd";
    #$content .= $NewReply;
    if(defined $NewReply && defined param('ReplyButton'))
    {
	#my $user_to_show = "$users_dir/$user";
	#$content .= "ssss";
	if(! -e $RepRou)
	{
	    mkdir $RepRou;
	}


	my $dir = "$RepRou/New";
	#$content .= $dir;
	if(! -e $dir)
	{
	    mkdir $dir;
	}
	my $filename = "$dir/reply.txt";
	$content .= $filename;
	
	if(open(my $fh, '>', $filename))
	{
	    $content .= "1";
	
	    print $fh "from=$user","\n";
	    print $fh "message=$NewReply\n";
	    print $fh "time=";
	    close $fh;
	}
	else
	{
	    $content .= "0";

	}



	#my $filename = "$user_to_show/posts/New/post.txt";
	#open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
	#print $fh "from=$zNum","\n";
	#print $fh "message = $NewPost\n";
	#print $fh "time=$PostTime";
	#close $fh
    }



#$replyField = "<form><textarea row = '2' cols = '15' name = '$reply'></textarea><input type = 'submit' value='reply' name='ReplyButton' class='matelook_button'><input type='hidden' name='RepRou' value='$route2' /></form>

}



sub NewAccount_page(){


    $NewUsername = param("NewUsername");
    $NewPassword = param("NewPassword");
    #$NewUsername = param("YourUsername");
    #$NewPassword = param("YourPassword");
    $EmailAddr = param("EmailAddr");
    $veri = param("Verification");

    

    if(defined param("VerificationButton"))
    {
	$content .= $EmailAddr;
	$to = $EmailAddr;
	$from = 'webmaster@yourdomain.com';
	$subject = 'Test Email';
	
	$Random = rand(6);
	#href='?zNum=$mate;
	#$message = "<a href = 'http://cgi.cse.unsw.edu.au/~z5077890/ass2/matelook.cgi?NewUsername=$NewUsername & ?NewPassword=$NewPassword & ?EmailAddr= $NewEmail & Confirm=Confirm &status=2'>This is test email sent by Perl Script</a>";
	$message = "<p>Your verification code is:$Random</p>";
	
	open(MAIL, "|/usr/sbin/sendmail -t");
	
# Email Header
	print MAIL "To: $to\n";
	print MAIL "From: $from\n";
	print MAIL "Subject: $subject\n\n";
	print MAIL "Content-type: text/html\n";
# Email Body
	print MAIL $message;
	
	close(MAIL);
	$content .= "Email Sent Successfully\n";
    }


    if(defined param("Confirm"))
    {

	$Random = param("Random");
	$content .= $Random;
	$content .= $veri;
	if($veri eq $Random)
	{
	    $content .= $NewUsername;
	    $content .= $NewPassword;
	    my $user_to_show = "$users_dir/$NewUsername";
	    if(-e $user_to_show)
	    {
		$content .= "The username exist";
	    }
	    else
	    {
		

		my $dir = "$user_to_show";
		mkdir $dir;
		
		my $filename = "$user_to_show/user.txt";
		open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
		print $fh "zid=$NewUsername","\n";
		print $fh "email=$EmailAddr\n";
		print $fh "password=$NewPassword";
		close $fh;


		$content .= "Congratulation!!!";
	    }
	}
	else
	{
	    $content .= "Verification code is incorrect";
	}
	 





    }



    
    


    return <<eof

<form id = "search"> 
<div>
  Search:
</div>
  <input type="text" name="SearchzNum">
  <input type="submit" value="Search"><br>
</form>


<div class="NewAccount">
<form id="NewAccount">

<p>
Your Username:
<input type="text" name="NewUsername" value="$NewUsername"/>
</p>
<p>
Your Password:
<input type="text" name="NewPassword" value="$NewPassword"/>
</pb>
<p>
Your Email:
<input type="text" name="EmailAddr"  value="$EmailAddr"/>
</p>
<p>
Verification code:
<input type="text" name="Verification"  value="$veri"/>
<input type="submit" name="VerificationButton" value="Verification" class="matelook_button">
<input type="hidden" name="Random" value="$Random">
</p>
<input type="submit" name="Confirm" value="Confirm" class="matelook_button"/>
<input type="hidden" name="status" value="$status" />

</form>

<form>
</br>
<input type="submit" name="Mypage" value="Back" class="matelook_button">
</form>
</div>



eof




}







sub Search_page{
    
#Search
    my @postfiles = glob("$users_dir/*/posts/*/*.*");
    #$content .= $postfiles[0];
    #$Search
    #$content .= $SearchzNum;

    if (defined $SearchzNum) 
    {
	for $user0 (@users)
	{
	    $user0 =~ s/.*\///gi;

	    if($user0 =~ /.*$SearchzNum.*/)
	    {
		push(@matchUsers,$user0);
	    }	
	}
    }

    for $user0(@matchUsers)
    {
	$mate =~ s/ //gi;
	my $usersphoto_filename = "$users_dir/$user0/profile.jpg";
	#$zNum = $user; 
	$users_photo = "<a href='?zNum=$user0 '><img src = '$usersphoto_filename' alt = '' height= '150' width= '150' /></a>";
	push(@users_photos,$users_photo);
    }



#Print Post
    foreach $file (@postfiles){
	#$content .= $fine . "aaaa";

	open F, '<', $file or die;
	while($line = <F>){
	    #$content .= $line;
	    if($line =~ /^time/){
		$line =~ s/^time=//;
		$sortedFile{$line} = $file;
	    }
	}
    }

    

#print post in order
    for $postkey(sort keys %sortedFile)
    {	

	#open my $F, "$postfile" or die "can not open $postfile: $!";
	open my $F, "$sortedFile{$postkey}" or die "can not open $postfiles{$postkey}: $!";
	while($line = <$F>)
	{
	    if($line =~ /^from.*/)
	    {
		#$line = s/from://gi;
		$from = $line;

	    }
	    if($line =~ /^message.*$SearchzNum.*/)
	    {
		# if($line =~ /$SearchzNum/)
		{
		    $Searchpost = $line . '<br><br>';
		    push(@Searchpost,$from);
		    push(@Searchpost,$Searchpost);
		}
	    }
	}

	close $F;
    }


#

    



       return <<eof

<form id = "search"> 
<div>
  Search:
<div>
  <input type="text" name="SearchzNum">
  <input type="submit" value="Search"><br>
</form>


<h3>
<br>
Result:
</h3>

<pb><font size = 6>Users:</font></pb>
<p>
<div>
<font size =5>
@matchUsers
</font>
</div>
</p>

<form method = "POST" action="demo_form.asp">
<p>
@users_photos
</p>
</form>

</br></br>
<p>
<pb><font size = 6>Post:</font></pb>
<div>
@Searchpost
</div>
</p>


eof

#
 
}



#
# Show unformatted details for user "n".
# Increment parameter n and store it as a hidden variable
#
sub user_page {

    Addmate();

    #
    $Mypage=param("Mypage");
    if(defined $Mypage)
    {
	$zNum = $user;
    }
    #

    if(!defined $zNum)
    {
	$zNum = param('zNum') || "z3275760";
    }
	@users = sort(glob("$users_dir/*"));
    
    $zLocal = $zNum;

    #my $user_to_show  = $users[$n % @users];
    
    my $user_to_show = "$users_dir/$zNum";
    
    my $details_filename = "$user_to_show/user.txt";
    my $other_filename = "$user_to_show/others.txt";
    my $photo_filename = "$user_to_show/profile.jpg";
    my @details;
    my $post;
    my @postlist;
    my @postfiles = glob("$user_to_show/posts/*/*.*");
    #my %postfiles;
    #my @postorder = keys %postfiles;
    my %sortedFile = ();
    my %postRoute = ();
    





#
    
    open my $p, "$details_filename" or die;
    while($line = <$p> )
    {
	#$details = join '', <$p>;
	if($line !~ /^password=.*/ && $line !~ /^courses.*/ && $line !~ /^email.*/ && $line !~ /^home_l.*/)
	{
	    push(@details, $line);
	    #$details = join $details, $line;
	}
    }
    close $p;

    if(-e $other_filename)
    {
	open my $q, "$other_filename" or die;
	while($line = <$q>)
	{
	    push(@details, $line);
	}
	close $q;
    }






# Sort post;
    foreach $file (@postfiles){

	my $abs_path = File::Spec->rel2abs($file) ;


	open F, '<', $file or die;
	while($line = <F>){

	    if($line =~ /^time/){
		$line =~ s/^time=//;
		$sortedFile{$line} = $file;

		$abs_path =~ s/post\.txt/comments/gi;
		$abs_path =~ s/.*\/$users_dir/$users_dir/gi;
		#$content .= $abs_path;
		$postRoute{$line} = $abs_path;
	    }
	}
        #
	close F;
	#
    }

    

#print post in order
    #for $postfile (@postfiles)
    for $postkey(sort keys %sortedFile)
    {	

	#open my $F, "$postfile" or die "can not open $postfile: $!";
	open my $F, "$sortedFile{$postkey}" or die "can not open $postfiles{$postkey}: $!";
	while($line = <$F>)
	{
	    if($line =~ /^message.*/)
	    {
		my @commentList;
		$CommentField = "<form><textarea row = '4' cols = '30' name='comment'></textarea><input type='submit' value='comment' name='CommentButton' class='matelook_button'><input type='hidden' name='ComRou' value='$postRoute{$postkey}' /><input type='hidden' name='zNum' value='$zNum'/></form>";

		#
		#$postRoute{$line}
		$route = $postRoute{$postkey};
		#$content .= $route."aaaa";
		my @commentFiles = glob("$route/*/*.*");

		for $commentFile(@commentFiles)
		{
		    #$content .= $commentFile;
		    #$commentRoute{$commentFile} = $commentFile;
		    #$route2 = $commentFile;
		    open P, '<', "$commentFile" or die "aaaaaa";
			while($line2 = <P>)
			{ 
			   if($line2 =~ /^message\=.*/)
			    {
				my @replyList;
				
				#$content .= $line2;
				$route2 = "$commentFile";
				$route2 =~ s/comment\.txt/replies/gi;
				#$content .= $route2;
				#$content .= ",,,,,,,,,,";


                                $replyField = "<form><textarea row = '2' cols = '15' name = 'reply'></textarea><input type = 'submit' value='Reply' name='ReplyButton' class='matelook_button'><input type='hidden' name='RepRou' value='$route2' /><input type='hidden' name='ComRou' value='$postRoute{$postkey}' /><input type='hidden' name='zNum' value='$zNum' /></form>";

				my @replyFiles = glob("$route2/*/reply\.txt");
				#$content .= "@replyFiles";
				for $replyFile(@replyFiles)
				{
				    open $q, '<', "$replyFile" or die "bbb";
				    while($line3 = <$q>)
				    {
					#$content .= $line3;
					if($line3 =~ /^message\=.*/)
					{
					    $line3 =~ s/message\=/response\:/gi;
					    $response = "<p>" . $line3 . "</p>";
					    push(@replyList, $response);
					}
				    }
				    close $q;
				   
				}
				$line2 =~ s/message\=/comment\:/gi;
				#$constent .= $route2;
				#$replyField = "<form><textarea row = '2' cols = '15' name = 'reply'></textarea><input type = 'submit' value='reply' name='ReplyButton' class='matelook_button'><input type='hidden' name='RepRou' value='$route2' /></form>";
				$comment = "<font size= '3'>" . $line2 . "</br>" . "</font>" . "</br>" . "<font size = '2'>" ."@replyList" . "</font>" . $replyField . "</br>"; 
				push(@commentList,$comment);
			    }
			}
		    close P;
		}
		#$content .= "@commentList";
		#
		#$post = $line . $CommentField  . '<br><br>';
		$line =~ s/message\=/post\: /gi;
		$post = "<font size = '4'>" . $line . "</font>" . '</br></br>' ."Comment------". '<br>' ."@commentList" . $CommentField  . '</br></br>';
		push(@postlist,$post);
	    }
	}

	close $F;
    }



###printmate();
  open  $p, '<' ,"$details_filename" or die "can not open $details_filename: $!";
    while($line = <$p> )
    {
	#$details = join '', <$p>;
	if($line =~ /mates=.*z\d*/)
	{
	    $line =~ s/.*\[//gi;
	    $line =~ s/].*//gi;
	    

	    @mates = split(/\,/,$line);

	}
    }
  close $p;

    for $mate(@mates)
    {
	$mate =~ s/ //gi;
	my $matephoto_filename = "$users_dir/$mate/profile.jpg";
	$zNum = $mate; 
	$mate_photo = "<a href='?zNum=$mate'><img src = '$matephoto_filename' alt = '' height= '75' width= '75' /></a>";
	push(@mate_photos,$mate_photo);
    }




    #$content .= "$zNum";



###
   # my $next_user = $n + 1;
    return <<eof
<form>
<input type="submit" value="Logout" name="LogoutFlag" class="matelook_button">
<input type="submit" value="New Account" name="NewAccount" class="matelook_button">
</form>

<form id = "search"> 
  Search:
  <input type="text" name="SearchzNum">
  <input type="submit" value="Search" class="matelook_button"><br>
</form>

<div id="Whole">
<div class="matelook_user_details">
@details
</div>
</div>

<div id="Whole">
<img src="$photo_filename" alt = ""  height="342" width="342"/>
<form>
<input type="submit" name="Friend" value="Friend" class="matelook_button">
<input type="hidden" name = "zNum0" value="$zLocal">
<input type="submit" name="UnFriend" value="UnFriend" class="matelook_button">
</form>

<form>
<p>Add new line in profile:</p>
<p class="PostArea">
<textarea rows="2" cols="4" name="others">
</textarea>
<input type="submit" name = "Saveothers" value="Save" class="matelook_button">
<p>
</form>

<form>
<p>Making Post:</p>
<p class="PostArea">
<textarea rows="4" cols="50" name="NewPost">
</textarea>
<p>
<input type="submit" name = "SavePost" value="Save" class="matelook_button">
<input type="hidden" name = "zNum0" value="$zLocal">

</form>


<p>
<b><font size=5>Post-------------</font></b>
<div id="Post">
@postlist
</div>

</p>


<p>
<div>
<font size = 3>
mates: </br>@mates
</font>
</div>
</p>

<form method = "POST" action="demo_form.asp">

<p>
@mate_photos
</p>
</form>




<p>


<form>
<input type="submit" name="Mypage" value="Mypage" class="matelook_button">
</form>

</div>




eof



}


#
# HTML placed at the top of every page
#
sub page_header {
    return <<eof
<!DOCTYPE html>
<html lang="en">
<head>
<title>matelook</title>
<link href="matelook.css" rel="stylesheet">

<script typ="text/javascript">

</script>
</head>
<body>
<div class="matelook_heading">
<i>
matelook
</i>
</div>
eof
}


#
# HTML placed at the bottom of every page
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}

main();
