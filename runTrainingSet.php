<html>
	<head>
		<title>Training positive tweet algorithm</title>
        <link rel="stylesheet" type="text/css" href="style.css">
		<link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon"/>
	</head>
	
	<body>
        <div id = "header"><a href = "index.php"><img src = "images/twitterlogo.png" alt = "Twitter Logo"></a></div>
		<?php
            ini_set('max_execution_time', 0);
            try {
				echo "<div id = \"button\">The training set is being processed</div>";
                $runTrainingSet = escapeshellcmd("python scripts/getWordLists.py");
                $output = shell_exec($runTrainingSet);
                echo "<pre><center>";
                print_r($output);
                echo "</center></pre>";
                echo "<div id = \"button\"><a href = \"positivetweets.php\">Return to positive tweets page</a></div>";
            } catch (Exception $e) {
                echo $e;
            }
        ?>
	</body>
</html>