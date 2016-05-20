package twitterfeed.kafka;

import java.util.Properties;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import kafka.producer.KeyedMessage;
import kafka.producer.ProducerConfig;

import org.apache.log4j.Logger;
import org.json.JSONObject;

import twitterfeed.config.AppConfig;

import com.google.common.collect.Lists;
import com.twitter.hbc.ClientBuilder;
import com.twitter.hbc.core.Client;
import com.twitter.hbc.core.Constants;
import com.twitter.hbc.core.endpoint.StatusesFilterEndpoint;
import com.twitter.hbc.core.processor.StringDelimitedProcessor;
import com.twitter.hbc.httpclient.auth.Authentication;
import com.twitter.hbc.httpclient.auth.OAuth1;

/**
 * @author Pavan PC
 * @Date 19-May-2016
 * 
 *       Main Application class to read data from Twitter Stream api and publish to kafka
 *
 */

public class KafkaProducer {
	private final static Logger logger = Logger.getLogger(KafkaProducer.class);
	private static final String topic = "twitter-topic";
	private static final BlockingQueue<String> queue = new LinkedBlockingQueue<String>(10000);
	
	/**
	   * This method publishes messages to kafka .
	   * @param
	   * 		producer- kakfka producer client object
	   * 		
	   * @exception InterruptedException On process interuption.
	   * 
	   */
	static void puslishMessages(kafka.javaapi.producer.Producer<String, String> producer)
	{
		logger.debug("INFO: Got messages.Pubslishig messages to kafka topic...");
		for (int msgRead = 0; msgRead < 1000; msgRead++) {
			KeyedMessage<String, String> message = null;
			try {
				message = new KeyedMessage<String, String>(topic, queue.take());
				String msg = queue.take();
//				System.out.println(msg);
				JSONObject obj = new JSONObject(msg);
				String text= obj.getString("text");
//				System.out.println(text);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			producer.send(message);
		}
	}
	
	/**
	   * This method establishes connection with Twitter streaming api using hbc client
	   * @param
	   * 		consumerKey-twitter api consumerKey
	   * 		consumerSecret- twitter api consumerSecret
	   * 		token- twitter api access token
	   * 		secret- twitter api secret
	   * 		
	   * @exception InterruptedException On process interuption.
	   * 
	   */
	
	public static void run(String consumerKey, String consumerSecret,
			String token, String secret) throws InterruptedException {

		Properties properties = new Properties();
		properties.put("metadata.broker.list", "localhost:9092");
		properties.put("serializer.class", "kafka.serializer.StringEncoder");
		properties.put("client.id","camus");
		ProducerConfig producerConfig = new ProducerConfig(properties);
		kafka.javaapi.producer.Producer<String, String> producer = new kafka.javaapi.producer.Producer<String, String>(
				producerConfig);

		
		StatusesFilterEndpoint endpoint = new StatusesFilterEndpoint();
		// add some track terms
		// this is to ge data from twitter api contianing trackterms say #a
		endpoint.trackTerms(Lists.newArrayList("twitterapi",
				"#a"));

		Authentication auth = new OAuth1(consumerKey, consumerSecret, token,
				secret);

		// Create a new BasicClient. By default gzip is enabled.
		Client client = new ClientBuilder().hosts(Constants.STREAM_HOST)
				.endpoint(endpoint).authentication(auth)
				.processor(new StringDelimitedProcessor(queue)).build();

		// Establish a connection
		client.connect();
		puslishMessages(producer);
		producer.close();
		client.stop();

	}

	/**
	   * The main method which reads config and calls run method
	   */
	public static void main(String[] args) {
		try {
			// Read application config like consumer key, token etc form
			// AppConfig.properties file
			// Appconfig file should not be exposed outside.
			// TODO: Add config properties to env variables and read, so that keys are not exposed outside
			AppConfig appConfig = new AppConfig();
			// Intialize app config object with required values after reading
			// property file
			appConfig.init();
			String consumerKey= appConfig.getConsumerKey();
			String consumerSecret= appConfig.getConsumerSecret();
			String token=appConfig.getToken();
			String secret=appConfig.getSecret();
			KafkaProducer.run( consumerKey,consumerSecret,token,secret);
		} catch (InterruptedException e) {
			logger.debug("Problem in initialiazing application");
		}
	}
}
