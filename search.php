<?php
$isbn = filter_input(INPUT_POST, 'isbn', FILTER_VALIDATE_INT);
$url = filter_input(INPUT_POST, 'url');
$valid = true;

if ($isbn == NULL || $isbn == false) {
        echo "Invalid ISBN format entered";
        $valid = false;
        header("location: index.php");
		
} else {
	require_once('database.php');
       error_reporting(E_ALL ^ E_NOTICE);
       $e = false;
       $result = $db->query("SELECT * FROM `book` WHERE isbn = '$isbn'");
       
       $b = $result->fetch();  

      $title = $title[0][0];

       if ($title) {
           
       } else {
           
       }
	
}
?>

<!DOCTYPE html>
<html>

<head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Bookstore</title>

        <!-- google fonts -->
        <link href='https://fonts.googleapis.com/css?family=Roboto:400,300,500,700' rel='stylesheet' type='text/css'>
        <link href='https://fonts.googleapis.com/css?family=Oswald:400,300,700' rel='stylesheet' type='text/css'>

        <!-- files -->
        <link href="assets/css/bootstrap.min.css" rel="stylesheet">
        <link href="assets/css/magnific-popup.css" rel="stylesheet">
        <link href="assets/css/owl.carousel.css" rel="stylesheet">
        <link href="assets/css/owl.carousel.theme.min.css" rel="stylesheet">
        <link href="assets/css/ionicons.css" rel="stylesheet">
        <link href="assets/css/main.css" rel="stylesheet">
    </head>

<body>
	 <!-- Bookstore Header -->
	 <div class="site-header-bg">
            <div class="container">
                <div class="row">
                    <div class="col-sm-6">
                        <a href="index.php"><img src="assets/images/book_logo.png" alt="logo"></a>
                    </div> 
                    <div class="col-sm-3 col-sm-offset-3 text-right">
                        <span class="ion-android-cart"></span> <?php if (session_status() == PHP_SESSION_NONE) {
    session_start();
}
                        if (isset($_SESSION['count'])) {
                         echo($_SESSION['count']);
                        } else {
                          echo("0");
                        }
                        ?> books
                        <form action="search.php" method="POST">
                        <div class="input-group">
                        <input name="isbn" id="search_info" type="text" class="form-control" placeholder="">
                        <span class="input-group-btn">
                        <button name="url" value="shop.php" class="btn btn-default btn-robot" type="submit">ISBN</button>
                        </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    <!-- Header -->

        <section id="header" class="main-header">
            <div class="container">

                <div class="row">
                    <nav class="navbar navbar-default">
                        <div class="navbar-header">
                            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#site-nav-bar" aria-expanded="false">
                                <span class="sr-only">Toggle navigation</span>
                                <span class="icon-bar"></span>
                                <span class="icon-bar"></span>
                                <span class="icon-bar"></span>
                            </button>
                        </div>

                        <div class="collapse navbar-collapse" id="site-nav-bar">
                            <ul class="nav navbar-nav">
                                <li ><a href="index.php">Home</a></li>
                                <li ><a href="about.html">About</a></li>
                                <li class="active"><a href="shop.php">Shop</a></li>
                                <li><a href="view_profile.php">view profile</a></li>
                                   <?php if (isset($_SESSION['user'])) {
                         echo('<li><a href="logout.php">Logout</a></li>');
                        } else {
                          echo( '<li><a href="login.php">Login</a></li>');
                        }
                        ?>
                           
                            </ul>
                        </div>
                    </nav>
                </div>
		</section>
		




<section id="product" class="product">
    <div class="container section-bg">
      <div class="row">
        <div class="col-sm-12">
          <div class="title-box">
            <h2 class="title">Book <span>Library</span></h2>
            <table align="center"
			  style="font-family:Courier; text-transform:none; font-size: 20px;border: 1px solid black; border-collapse: collapse">
			  				<tr>

							  <td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Cover:
                                </td>
                                <td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">ISBN:
                                </td>
                                <td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Author:
                            
                                </td>
                                <td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Title:
                                </td>

                                <td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Category:
                                </td>
                                
                                <td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Buy Price:
								</td>
								<td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Sell Price:
								</td>
								<td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Add to Cart:
                                </td>
                            </tr>
              
              <tr>

			  <td align="left"
				  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
				  
				  <?php $link = "http://covers.openlibrary.org/b/isbn/" . $b['isbn'] . ".jpg"?>
				  
				  <?php echo '<img src="'.$link.'" width="100" height="100" />'?>
				  
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $b['isbn']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $b['author']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $b['title']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $b['category']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $b['buy_price']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $b['sell_price']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <form action="add_to_cart.php" method="POST">
                    <input type="hidden" name="isbn" value=<?php echo $b['isbn']?>>
                    <input type="hidden" name="id" value=<?php echo $b['id']?>>
                    <input type="submit" value="Add to Cart" style="font-size: 10px;">
                    </form>
                </td>  
              </tr>
            
            </table>
            <div class="text-center mt20 col-sm-12">
            <form action="view_cart.php">
                    <button type="submit" class="btn btn-robot pull-left" id="cfsubmit" style="margin-bottom: 2em; margin-top: 3em; ">Checkout</button>
                </form>
                  </div>
          </div>
          
    </div>
    
</section>
</body>
</html>
