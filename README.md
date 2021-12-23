# prime-auction
This application is a demo auction app where user can register, login, post their product for auction and view other users' bid. 

# basic authentication
path 1: '/app/login' or '/app/' 
This is the landing page of application. You can enter the email and can register or login if are registered.

path 2: '/dashboard' or '/dashboard/<user_id>'
This is the home page of user. You can see the auctions posted by other. There are buttons to post your auction, see your posted auctions, see your winning bid and logout. You can click on products to see the details.

path 3: '/get/product/<product_id>'
The product page carries all the details and bidding options. If the product belongs to you, you can not post any bid, but you can bid on items posted by others and update them. There is a bid table which is showing the bidding prices by users.

path 4: '/add/product'
You can add products here with all details and one thing to remember that bid deadline should be in this format 
mm/dd/yyyy hh:mm AM/PM .

path 5: '/admin/app/product/'
You can see analytics of products in auction in charts and tables in this page. 

