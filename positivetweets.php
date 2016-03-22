<html>
	<head>
		<title>Positive tweets only - Twitter</title>
        <link rel="stylesheet" type="text/css" href="style.css">
        <link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon"/>
	</head>
	
	<body>
        <div id = "header"><img src="images/twitterlogo.png" alt = "Twitter Logo"></div>
		<?php
            ini_set('max_execution_time', 300);
            
            $noTrainingSetWarning = "Unable to show tweets: the training set has not been processed yet. ";
            
            $positiveWords = "output/positive words.txt";
            $negativeWords = "output/negative words.txt";
            
            try {
                if (!file_exists($positiveWords) || !file_exists($negativeWords)) {
                    echo "<a href = \"runTrainingSet.php\">Run training set</a> Warning: might take a while.\n";
                    throw new Exception($noTrainingSetWarning);
                }
                #python script is executed
                $showPositiveTweets = escapeshellcmd("python scripts/compareTweets.py");
                $output = shell_exec($showPositiveTweets);
                
                #python script writes output to text file, text file is read by this php script 
                $file = fopen("output\positive tweets.txt", "r");
                
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
                    echo nl2br("Author: " . $tweet[0]) . "\n";
                    echo nl2br("Date and time: " . $tweet[1]) . "\n";
                    echo nl2br($tweet[2]) . "\n";
                }
            } catch (Exception $e) {
                echo $e;
                
            }
            
            
		?>
	</body>
</html>