<html>
	<head>
		<title>Welcome to Twitter</title>
        <link rel="stylesheet" type="text/css" href="style.css">
		<link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon"/>
	</head>
	
	<body>
        <div id = "header">
			<div id = "header"><a href = "index.php"><img src = "images/twitterlogo.png" alt = "Twitter Logo"></a></div>
		</div>
		<div id = "button">
			<a href = "positivetweets.php">Show positive tweets</a>
		</div>
		<?php
			try {
				#python script is executed
				$showPositiveTweets = escapeshellcmd("python scripts/showNormalTweets.py");
				$output = shell_exec($showPositiveTweets);
				
				#python script writes output to text file, text file is read by this php script 
				$file = fopen("output\all tweets.txt", "r");
				
				#create new array to store tweets in
				$tweets = array();
				
				#add tweets from file to tweets array
				while (($line = fgets($file)) !== false) {
					#create new array to store tweet data in
					$tweet = array();
					#add first line (author) from file to tweet 
					array_push($tweet, $line);
					#go to next line
					$line = fgets($file);
					#add second line (date and time) from file to tweet
					array_push($tweet, $line);
					#go to next line
					$line = fgets($file);
					#add third line (tweet) from file to tweet
					array_push($tweet, $line);
					#tweet is now an array with 3 variables: author, datetime and tweet
					#tweet is pushed to tweets array
					array_push($tweets, $tweet);
				}
				fclose($file);
				
				#show tweets on page
				foreach ($tweets as $tweet) {
					echo "<div id = \"tweet\">";
					echo "<h2>" . $tweet[2] . "</h2>"; # show tweet
					echo "<h2>" . $tweet[0] . "</h2>"; # show author
					echo "<h2>" . $tweet[1] . "</h2>"; # show date and time
					echo "</div>";
				}
			} catch (Exception $e) {
				echo $e;
			}
		?>
	</body>
</html>