package twitterfeed.config;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

import org.apache.log4j.Logger;

import twitterfeed.exception.AppConfigException;

public class AppConfig {
	private final static Logger logger = Logger.getLogger(AppConfig.class);
	private String consumerKey;
	private String consumerSecret;
	private String token;
	private String secret;
	private static final String appConfigFileName = "AppConfig.properties";
	private Properties prop = new Properties();
	private InputStream input = null;
	
	
	public String getConsumerSecret() {
		return consumerSecret;
	}
	
	public String getToken() {
		return token;
	}
	
	public String getSecret() {
		return secret;
	}
	
	public String getConsumerKey() {
		return consumerKey;
	}
	
	/*
	 * Method to initialize application config properties
	 */
	public void init() {
		try {

			input = new FileInputStream(appConfigFileName);
			// load property file
			prop.load(input);
			this.consumerKey = prop.getProperty("consumerKey");
			this.consumerSecret = prop.getProperty("consumerSecret");
			this.token=prop.getProperty("token");
			this.secret=prop.getProperty("secret");

		}catch (FileNotFoundException e) {
			logger.debug("\nERROR: AppConfig.properties file not found. Please copy it to current directory");
			logger.debug(e.getMessage());
			throw new AppConfigException(
					"ERROR: AppConfig.properties file not found. Please copy it to current directory");
		}
		catch (IOException e) {
			logger.debug("Problem in initialiazing app configurations");
			logger.debug(e.getMessage());
			throw new AppConfigException(
					"\nERROR: Error in  Reading AppConfig properties ");

		} finally {
			if (input != null) {
				try {
					input.close();
				} catch (IOException e) {
					logger.debug("Problem in initialiazing app configurations");
					logger.debug(e.getMessage());
					throw new AppConfigException(
							"ERROR: Error in Reading AppConfig properties ");
					// e.printStackTrace();
				}
			}
		}

	}

}
