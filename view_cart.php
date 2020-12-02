<?php
include('database.php');

	if(!isset($category)) {
		$category= filter_input(INPUT_GET, 'category_id',
					FILTER_VALIDATE_INT);
		if ($category == NULL  || $category == FALSE) {
			$category = 1;
		}
    }
    
   


    
    //loop thorugh the cart[][] then if 
	
	//$query='SELECT * FROM categories';
	
	//$categories=$db->query($query);
	
	//$query="SELECT * FROM products WHERE categoryID='$category'";
	$query="SELECT * FROM book";// WHERE categoryID='$category'";
  $book=$db->query($query);
  
?>

<!DOCTYPE html>
<html>

<head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Cart</title>

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
      <div class="row">
        <div class="col-sm-12">
          <div class="title-box">
            <h2 class="title">Your <span>Cart</span></h2>
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
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Quantity:
								</td>
								<td align="left"
                                style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">Add to Cart:
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
				  
				  <?php echo '<img src="'.$link.'" width="100" height="100" />'?>
				  
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $row['isbn']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $row['author']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $row['title']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $row['category']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo $row['buy_price']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <?php echo "x".$b['count']?>
                </td>
                <td align="left"
                  style="padding-left: 10px;padding-right: 10px; border: 1px solid black; border-collapse: collapse">
                  <form action="delete_cart.php" method="POST">
                  <input type="hidden" name="isbn" value=<?php echo $row['isbn']?>>
                    <input type="hidden" name="id" value=<?php echo $row['id']?>>
                    <input type="submit" value="Remove from cart" style="font-size: 10px;">
                    </form>
                </td>  
              </tr>
              <?php endforeach;?>
            </table>
            <div class="text-center mt20 col-sm-12" >
            <form action="shop.php" >
                    <button type="submit" class="btn btn-robot pull-left" id="cfsubmit" style="margin-bottom: 2em; margin-top: 3em; ">Back to Shop</button>
            </form> 

            <form action="checkout.php">
                    <button type="submit" class="btn btn-robot pull-right" id="cfsubmit" style="margin-bottom: 2em; margin-top: 3em;">Checkout</button>
            </form>
                  </div>
          </div>
          
    </div>
    
</section>
</body>
</html>