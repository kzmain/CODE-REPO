<?php session_start() ?>
<?php 
        $_SESSION['total']=$_SESSION['plm']['s1']*17+$_SESSION['plm']['s3']*26.75+$_SESSION['plm']['s2']*22.5;
    if(isset($_POST['creditCard'])&&isset($_POST['creditCardExpireDate'])){
		$formY=explode('-',$_POST['creditCardExpireDate'])[0];
		$formM=explode('-',$_POST['creditCardExpireDate'])[1];
		$continue = false;
		if($formY<date('Y')){
			
		}else if(($formY==date('Y'))&&($formM<date('n'))){
			
		}else{
			$continue=true;
		}
		if($continue==true){
			$_SESSION['firstName']=$_POST['firstName'];
  			$_SESSION['lastName']=$_POST['lastName'];
  		    $_SESSION['address']=$_POST['address'];
  		    $_SESSION['email']=$_POST['email'];
        	$_SESSION['phone']=$_POST['phone'];
   	     	$_SESSION['DM']=$_POST['DM'];
   	    	switch($_SESSION['DM']){
        	    case 'free':
              	  break;
           		case 'RC':
                	$_SESSION['total'] += 7;
                	break;
            	case 'EC':
                	$_SESSION['total'] += 10.50;
                	break;
            	default:
               		break;
        	}
        	$_SESSION['creditCard']=$_POST['creditCard'];
        	$_SESSION['creditCardExpireDate']=$_POST['creditCardExpireDate'];
			header("Location: confirmation.php"); 
		}

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
		 <link href="css/checkout.css" type="text/css" rel="stylesheet">
         <script src="js/checkout.js"></script>
     </head>
	 <body>
		<header>
			<?php include'header.php';?>
		</header>
		<nav>
			<?php include'nav.php';?>
		</nav>
		<main>
<form action="checkout.php" method="post" name="checkout" onsubmit="return rememberMe()">
	<fieldset>
		<legend>Confirmation</legend>
		<div class="userInfo">
			<span>
				<lable for="firstName">First Name:</lable>
			</span>
			<span>
				<input type=text id="firstName" name="firstName" pattern="[a-zA-Z0-9_\-,;.]+" required/>
			</span>
		</div>
		<div class="userInfo">
			<span>
				<lable for="lastName">Last Name:</lable>
			</span>
			<span>
				<input type=text id="lastName" name="lastName" pattern="[a-zA-Z0-9_\-,;.]+" required/>
			</span>
		</div>
		<div class="userInfo">
			<span>Address:</span>
			<span><textarea id="address" name="address" pattern="[a-zA-Z0-9_\-,;.]+" required></textarea></span>
		</div>
		<div class="userInfo">
			<span>E-mail:</span>
			<span><input type="email" id="email" name="email" required></span>
		</div>
		<div class="userInfo">
			<span>Phone:</span>
			<span><input type="tel" id="phone" name="phone" pattern="^04[0-9]{8}" title="Please enter your phone number start with 04"required></span>
		</div>
		<div class="userInfo">
			<span>Delivery Method</span>
			<span>
				<select name="DM">
					<option value="free">Regular delivery price:free</option>
					<option value="Regular courier">Regular courier price: $7.00</option>
					<option value="Express courier">Express courier price: $10.50</option>
				</select>
			</span>
		</div>
		<div class="userInfo">
			<span>Credit card:</span>
			<span><input type="text" id="creditCard" name="creditCard" pattern="[0-9]{13,18}" title="Please enter your 13-18 credit number"></span>
		</div>
		<div class="userInfo">
			<span>Credit card expire date:</span>
			<span><input type="month" value="<?php echo date('Y-n'); ?>" name="creditCardExpireDate" id="creditCardExpireDate" required></span>
		</div>
		<div id="rememberMe">
            </br>
			<span>Remember Me:</span>
			<span><input type="checkbox" checked="checked" name="RM" value="RM" id="RM"></span>
		</div>
		<div id="submit">
            <input type="submit" value="Submit"/>
        </div>
	</fieldset>
</form>
		</main>
		<footer>
			<?php include'footer.php';?>
		</footer>
			<div id="debug">
			<?php include_once('/home/eh1/e54061/public_html/wp/debug.php'); ?>
			<div id="debug">
     <script src="js/checkout.js"></script>
 </html>