<?php session_start() ?>
<?php
    if(!empty($_POST)&&(!isset($_POST['delS1']))&&(!isset($_POST['delS2']))&&(!isset($_POST['delS3']))){
       $_SESSION['plm']=$_POST['plm'];
    }

    $post_data_is_invalid = false;
    foreach ($_SESSION['plm'] as $v1) {
           if(($v1>5)||($v1<0)){
               $post_data_is_invalid = true;
        }
    }
        if ( isset($_POST["delS1"]) ) {
       $_SESSION['plm']['s1']=0; 
    }
    if ( isset($_POST["delS2"]) ) {
       $_SESSION['plm']['s2']=0; 
    }
    if ( isset($_POST["delS3"]) ) {
       $_SESSION['plm']['s3']=0; 
    }
    if ( $post_data_is_invalid === true||(($_SESSION['plm']['s1']===0)&&($_SESSION['plm']['s2']===0)&&($_SESSION['plm']['s3']===0))){
  header("Location: shop.php"); 
  } 

?>

<html>
     <head>
         <meta charset="UTF-8"/>
         <title>Josh Thomas | A Comedian</title>
         <link rel="icon" href="img/favicon.ico"/>
		 <link href="css/main.css" type="text/css" rel="stylesheet" />
		 <link href="css/nav.css" type="text/css" rel="stylesheet" />
		 <link href="css/footer.css" type="text/css" rel="stylesheet" />
		 <link href="css/cart.css" type="text/css" rel="stylesheet">
     </head>
	 <body>
		<header>
			<?php include'header.php';?>
		</header>
		<nav>
			<?php include'nav.php';?>
		</nav>
		<main>
    <form action="checkout.php" method="post">>
    	<fieldset id="cart">
           <legend>Cart</legend>
           <?php 
           if($_SESSION["plm"]["s1"]>0){
                    echo '<div class = "disc">
                        <span>Please Love Me Season 1</span>
                        <span>Unit-price:$17.00/set</span>
                        <span>Quality:';
                    echo $_SESSION["plm"]["s1"];
                    echo '</span><span>Sub-total:'.(number_format($_SESSION['plm']['s1']*17,2)).'</span><span><input type="submit" name="delS1" value="delete" formaction="cart.php"></span></div>';
           }
           if($_SESSION["plm"]["s2"]>0){
                    echo '<div class = "disc">
                    <span>Please Love Me Season 2</span>
                    <span>Unit-price:$22.50.00/set</span>
                    <span>Quality:';
                    echo $_SESSION["plm"]["s2"];
                    echo '</span><span>Sub-total:'.(number_format($_SESSION['plm']['s2']*22.5,2)).'</span><span><input type="submit" name="delS2" value="delete" formaction="cart.php"></span></div>';
           }
           if($_SESSION["plm"]["s3"]>0){
                   echo '<div class = "disc">
                         <span>Please Love Me Season 3</span>
                         <span>Unit-price:$26.75.00/set</span>
                         <span>Quality:';
                    echo $_SESSION["plm"]["s3"];
                    echo '</span><span>Sub-total:'.(number_format($_SESSION['plm']['s3']*26.75,2)).'</span><span><input type="submit" name="delS3" value="delete" formaction="cart.php"></span></div>';
                    
                    echo '<br/><div id="total"><span id="total">Total:'.(number_format(($_SESSION['plm']['s1']*17+$_SESSION['plm']['s3']*26.75+$_SESSION['plm']['s2']*22.5),2)).'</span></div>';
                    echo '<br/><div><input type="submit" value="Continue" id="continue"></div>';
           }
           ?>
           
        </fieldset>
    </form>
		</main>
		<footer>
			<?php include'footer.php';?>

		</footer>
			<div id="debug">
			<?php include_once('/home/eh1/e54061/public_html/wp/debug.php'); ?>
			<div id="debug">
	 </body>
 </html>