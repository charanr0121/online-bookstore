<?php



// Get the product data
$isbn = filter_input(INPUT_POST, 'isbn');
$id = filter_input(INPUT_POST, 'id');

session_start();





function addToCart($id) {
	foreach($_SESSION['cart'] AS &$result) {
		if ($result['id'] == $id) {
			$quantity =  $result['count'];
			
			$quantity = $quantity + 1;
			$result['count'] = $quantity;
			
			unset($result);
			return;
		}
  }
 
  $_SESSION['cart'][] = array('id'=> $id, 'count'=>1);
}

if(isset($_SESSION['cart'])) {

	
	
	$count = 0;
	$count = $_SESSION['count'];
	$count++;
	$_SESSION['count'] = $count;
	

	$cart_index = $_SESSION['cart_index'];
	$cart_index++;
	$_SESSION['cart_index'] = $cart_index;

	addToCart($id);
	
	
	
	
} else {
	$_SESSION['cart_index'] = 0;
	$_SESSION['count'] = 1;
	$_SESSION['cart'][] = array('id'=> $id, 'count'=>1);
}
include('shop.php');
?>