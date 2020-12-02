<?php
include('database.php');

	if(!isset($category)) {
		$category= filter_input(INPUT_GET, 'category_id',
					FILTER_VALIDATE_INT);
		if ($category == NULL  || $category == FALSE) {
			$category = 1;
		}
	}
 
	//$query='SELECT * FROM categories';
	
	//$categories=$db->query($query);
	
	//$query="SELECT * FROM products WHERE categoryID='$category'";
	$query="SELECT * FROM book";// WHERE categoryID='$category'";
  $book=$db->query($query);
  $total = 0.0;
?>

<!DOCTYPE html>
<html>

<head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Checkout</title>

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
                        <form>
                            <div class="input-group">
                                <input type="text" class="form-control" placeholder="">
                                <span class="input-group-btn">
                                    <button class="btn btn-default btn-robot" type="button">ISBN</button>
                                </span>
                            </div>
                        </form>
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
      <div class="row" style="">
      <div class="boxed">
        <div class="col-sm-12">
          <div class="title-box">
            <h2 class="title">Checkout <span></span></h2>

            <h3 style="text-align: left;">Payment & Shipping </h3>
            <hr>
            
                
            <table align="left"
			  style="font-family:Courier; text-transform:none; font-size: 15px;border: 1px solid black; border-collapse: collapse; ">
			  				<tr>

							  <td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Cover:
                                </td>
                                
                                <td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Author:
                                </td>

                                <td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Price:
                                </td>
                                <td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Quantity:
                                </td>

                            </tr>
                            <?php  foreach($_SESSION['cart'] as $b):?> 
                
                <?php 
                
                $query="SELECT * FROM book WHERE id =".$b['id']. " LIMIT 1";
                
                    $book=$db->query($query); 
                    if ($book != false) {
                    $row = $book->fetch();    
                    }
                   ?>


              <tr>

			  <td align="left"
				  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
				  
				  <?php $link = "http://covers.openlibrary.org/b/isbn/" . $row['isbn'] . ".jpg"?>
				  
				  <?php echo '<img src="'.$link.'" width="50" height="50" />'?>
				  
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $row['title']." by ".$row['author'] ?>
                </td>

                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $row['buy_price'] ;   
                  $total = $total + ($row['buy_price'] * $b['count']);  ?>
                
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo "x".$b['count']?>
                </td>
              </tr>
              <?php endforeach;?>
            </table>
            <div class="text-center mt20 col-sm-12">

            <p style="text-align: left; color: black; padding:">Total: <?php echo($total); ?> </p>
            <form action="view_cart.php">
                    <button type="submit" class="btn btn-robot pull-left" id="cfsubmit" style="margin-bottom: 2em; margin-top: 0em; ">Edit Cart</button>
            </form>
                  </div>
          </div>

                </div>
                </div>
                </div>
          <div class="container" >
          
          <div class="row">
            <div class="boxed">
              <form action="confirmation.php" class="contact-form" id="add_user" method="POST" algn="left">
                <div class="row">
                  <div class="col-sm-5">
                    <div class="form-group">
                        <input type="text" class="form-control" name="name" placeholder="name" id="username" required>
                    </div> <!-- /.form-group -->
                  </div> <!-- /.col-sm-6 -->
                  <div class="col-sm-5">
                    <div class="form-group">
                      <input type="text" class="form-control" name="ccnumber" placeholder="1111-2222-3333-4444" id="password">
                    </div> <!-- /.form-group -->
                  </div> <!-- /.col-sm-6 -->
                  <div class="col-sm-5">
                    <div class="form-group">
                      <input type="text" class="form-control" name="addy" placeholder="1418 Earth Drive" id="email">
                    </div> <!-- /.form-group -->
                  </div> <!-- /.col-sm-6 -->
                  <div class="col-sm-2">
                    <div class="form-group">
                      <input type="text" class="form-control" name="zip" placeholder="Zip Code" id="address">
                    </div> <!-- /.form-group -->
                  </div> <!-- /.col-sm-6 -->
                  <div class="col-sm-3">
                    <div class="form-group">
                      <input type="text" class="form-control" name="state" placeholder="state" id="address">
                    </div> <!-- /.form-group -->
                  </div> <!-- /.col-sm-6 -->
                  <div class="col-sm-5">
                    <div class="form-group">
                      <input type="text" class="form-control" name="phone" placeholder="800-400-200" id="name" >
                    </div> <!-- /.form-group -->
                  </div> <!-- /.col-sm-6 -->
                  <div class="col-sm-5">
                    <div class="form-group">
                      <input type="text" class="form-control" name="email" placeholder="Email" id="phone">
                    </div> <!-- /.form-group -->
                  </div> <!-- /.col-sm-6 -->


                  <div  class="text-center mt20 col-sm-12">
                    <button type="submit" class="btn btn-robot pull-left" id="cfsubmit" style="margin-bottom: 15px;">Submit</button>
                  </div>
            </form>
          
    </div>
    
</section>

</body>
</html>