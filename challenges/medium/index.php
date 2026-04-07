<?php
$secret = "admin_token_123";
if (isset($_GET['token']) && $_GET['token'] === $secret) {
    echo file_get_contents("flag.txt");
} else {
    echo "Access denied";
}
?>
