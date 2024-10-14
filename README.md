<h1>OrderTradeRetrievalService</h1>

<p><strong>OrderTradeRetrievalService</strong> is a vital component of the <strong>StockBrokerageSystem</strong> project repository, designed to facilitate efficient retrieval of order and trade data. This microservice allows users to easily access all their orders and trades, enhancing the overall user experience in the trading environment.</p>

<h2>Key Features:</h2>

<ul>
  <li><strong>Fetch All Orders</strong> (GET): Retrieve a complete list of all orders placed by the user, including relevant details for each order.</li>
  <li><strong>Fetch Specific Order</strong> (GET): Access detailed information about a specific order using its unique <code>order_id</code>.</li>
  <li><strong>Fetch All Trades</strong> (GET): Obtain a comprehensive list of all executed trades, including unique trade identifiers, execution timestamps, prices, and quantities.</li>
</ul>

<h2>Architecture</h2>
<p>The <strong>OrderTradeRetrievalService</strong> leverages <strong>MongoDB</strong> for data storage and <strong>Redis</strong> for caching to ensure fast and reliable access to order and trade information. This architecture helps maintain high performance and availability for users.</p>

<h2>Deployment</h2>
<p>The microservice is deployed on <strong>Vercel</strong>, ensuring a scalable and globally accessible platform that enhances the performance of the <strong>StockBrokerageSystem</strong>.</p>

<h2>Integration</h2>
<p>This microservice seamlessly integrates with other components of the <strong>StockBrokerageSystem</strong>, providing users with the ability to manage their trading activities efficiently.</p>
