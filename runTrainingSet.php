<html>
	<head>
		<title>Training positive tweet algorithm</title>
        <link rel="stylesheet" type="text/css" href="style.css">
		<link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon"/>
	</head>
	
	<body>
        <div id = "header"><img src="images/twitterlogo.png" alt = "Twitter Logo"></div>
		<?php
            try {
                $runTrainingSet = escapeshellcmd("python scripts/getWordLists.py");
                $output = shell_exec($runTrainingSet);
                echo "<a href = \"positivetweets.php\">Return to positive tweets page</a>";
            } catch (Exception $e) {
                echo $e;
            }
        ?>
	</body>
</html>