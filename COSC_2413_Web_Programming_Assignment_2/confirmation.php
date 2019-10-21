<?php session_start() ?>
<?php
	$order = fopen("order\order.txt", "a+") or die("Unable to open file!");
	if(isset($_SESSION)){
	fwrite($order,$_SESSION['firstName']);
	fwrite($order,',');
	fwrite($order,$_SESSION['lastName']);
	fwrite($order,',');
	fwrite($order,$_SESSION['address']);
	fwrite($order,',');
	fwrite($order,$_SESSION['email']);
	fwrite($order,',');
	fwrite($order,$_SESSION['phone']);
	fwrite($order,',');
	fwrite($order,$_SESSION['DM']);
	fwrite($order,',');
	fwrite($order,$_SESSION['total']);
	fwrite($order,"\n");
	unset($_SESSION);
	}
	rewind($order);
	$orderNumber=0;
	?>
	<html>
     <head>
         <meta charset="UTF-8"/>
         <title>Josh Thomas | A Comedian</title>
         <link rel="icon" href="img/favicon.ico"/>
		 <link href="css/main.css" type="text/css" rel="stylesheet" />
		 <link href="css/nav.css" type="text/css" rel="stylesheet" />
		 <link href="css/footer.css" type="text/css" rel="stylesheet" />
		 <link href="css/confirmation.css" type="text/css" rel="stylesheet">
     </head>
	 <body>
		<header>
			<?php include'header.php';?>
		</header>
		<nav>
			<?php include'nav.php';?>
		</nav>
		<main>
	<?php
	$line = count(file("order\order.txt"));  
	while($orderNumber<$line){
		$temp=fgets($order);
		$userInfo=explode(',',$temp);
		echo "<div class=\"orderInfo\">";
		echo "#".($orderNumber+1)." order <br /> Customer Name: ".$userInfo[0].$userInfo[1]." Address: ".$userInfo[2]." E-mail: ".$userInfo[3]." Phone Number: ".$userInfo[4]." Delivery Method: ".$userInfo[5]." Total: ".$userInfo[6]."<br />";
		echo "</div>";
		$orderNumber++;
	}
	fclose($order);
?>
</main>
		<footer>
			<?php include'footer.php';?>

		</footer>
			<div id="debug">
			<?php include_once('/home/eh1/e54061/public_html/wp/debug.php'); ?>
			<div id="debug">
	 </body>
 </html>