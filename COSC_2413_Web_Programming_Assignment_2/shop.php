 <! DOCTYPE html>
 <!--Sells BluRay and DVD version of Please Like Me 1-3-->
 	 	<?php session_start() ?>
 <html>
     <head>
         <meta charset="UTF-8"/>
         <title>Josh Thomas | A Comedian</title>
         <link rel="icon" href="img/favicon.ico"/>
		 <link href="css/main.css" type="text/css" rel="stylesheet" />
		 <link href="css/nav.css" type="text/css" rel="stylesheet" />
		 <link href="css/footer.css" type="text/css" rel="stylesheet" />
		 <link href="css/shop.css" type="text/css" rel="stylesheet">
		 <script src="js/shop.js"></script>
     </head>
	 <body>

		<header>
			<?php include'header.php';?>
		</header>
		<nav>
			<?php include'nav.php';?>
		</nav>
		<main>
			<form action="cart.php" method="post">>
				<fieldset id="PLM">
					<legend>
						'Please Like me' Shop
					</legend>

					<img src="img/PleaseLikeMe_ProgrammingPage.jpg" id="banner">
					<div>
						<details>
							<summary>Season 1</summary>
							<p class="PLSIntro">With his 21st birthday just around the corner, life finally seems to be coming together for Josh (Josh Thomas). He’s sharing a house with his best (and only) friend, Tom (Tom Ward), his dog, John, and Tom’s rabbit, $haniqua, and he’s doing adult things like cooking roast chickens and eating asparagus. But the events of one day throw his world into chaos. He’s dumped by his girlfriend, Claire (Caitlin Stasey), and introduced to a decidedly odd but very attractive man, Geoffrey (Wade Briggs). And when his divorced mum, Rose (Debra Lawrance), overdoses on pain killers, Josh is forced to move back into the family home to keep an eye on her. If that’s not enough, he has to deal with his dad Alan’s (David Roberts) guilt over his ex-wife and clumsy attempts to hide his new, younger girlfriend, Mae (Renee Lim). It’s all a bit more than Josh had planned for - which was just to plate up a tasty dinner.</p>
						</details>
							<div id="season1" class="season">
									<span>Unit-price:$17.00/set</span>
									<span>Quality:<input type="number" value="1" id = "Q1" name="plm[s1]"min="0" max="5"></span>
									<span>Sub-total:<span id="sub1"></span></span>
							</div>
					</div>
					<div>
						<details>
							<summary>Season 2</summary>
							<p class="PLSIntro">The award-winning Please Like Me, created by Josh Thomas, is back. In Season Two, Josh tries to get through the day without upsetting anyone. There's a new dog, a new rabbit and a new baby. There’s no big twist. It isn't Lost.</p>
						</details>
							<div id="season2" class="season">
									<span>Unit-price:22.50$/set</span>
									<span>Quality:<input type="number" value="1" id ="Q2" name="plm[s2]"min="0" max="5"></span>
									<span>Sub-total:<span id="sub2"></span></span>
							</div>
					</div>
					<div>
						<details>
							<summary>Season 3</summary>
							<p class="PLSIntro">In season three, new characters arrive, complications ensue, and a cast of extraordinary performers competes again for screen time with John the cavoodle. Josh and Tom acquire new housemates: some fluffy, innocent baby chickens. Josh is also trying to acquire a new boyfriend, the anxiety-ridden Arnold, but Arnold is struggling to commit.</p>
						</details>
							<div id="season3" class="season">
									<span>Unit-price:26.75$/set</span>
									<span>Quality:<input type="number" value="1" id = "Q3"name="plm[s3]"min="0" max="5"></span>
									<span>Sub-total:<span id="sub3"></span></span>
							</div>
					<p id="total"></p>
					
					
					<script src="js/shop.js"></script>
					<input type="submit" value="!Buy!" id="buy">
				</fieldset>
			</form>
				<img src="img/please.jpg" class="PLMIMG" id="PLMIMG1">
				<img src="img/pleaselikemecanren-700x400.jpg" class="PLMIMG" id="PLMIMG2">
				<table id="online_store">
					<tr>
						<td>Season 1</td>
						<td><a target="_blank" href="https://itunes.apple.com/au/tv-season/please-like-me-season-1/id616877503"><img src="img/appstore.jpg" alt="Get It On app store" class="appstore"></a></td>
						<td><a target="_blank" href="https://play.google.com/store/tv/show/Please_Like_Me?id=RtnabrwLBEs&cdid=tvseason-9aM7tHsSt5EjPpLQ3AMKhw"><img src="img/google_play_icon.png" alt="Get It On google play" class="googleplay"></a></td>
					</tr>
					<tr>
						<td>Season 2</td>
						<td><a target="_blank" href="https://itunes.apple.com/au/tv-season/please-like-me-season-2/id906508728"><img src="img/appstore.jpg" alt="Get It On app store" class="appstore"></a></td>
						<td><a target="_blank" href="https://play.google.com/store/tv/show/Please_Like_Me?id=RtnabrwLBEs&cdid=tvseason-9aM7tHsSt5EjPpLQ3AMKhw"><img src="img/google_play_icon.png" alt="Get It On google play" class="googleplay"></a></td>
					</tr>
					<tr>
						<td>Season 3</td>
						<td><a target="_blank" href="https://itunes.apple.com/au/tv-season/please-like-me-season-3/id1047334958"><img src="img/appstore.jpg" alt="Get It On app store" class="appstore"></a></td>
						<td><a target="_blank" href="https://play.google.com/store/tv/show/Please_Like_Me?id=RtnabrwLBEs&cdid=tvseason-9aM7tHsSt5EjPpLQ3AMKhw"><img src="img/google_play_icon.png" alt="Get It On google play" class="googleplay"></a></td>
					</tr>
				</table>
		</main>
		<footer>
			<?php include'footer.php';?>

		</footer>
			<div id="debug">
			<?php include_once('./debug.php'); ?>
			<div id="debug">
	 </body>
 </html>