/**
 * 
 */
package edu.siu.sentiment;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
//import java.util.Arrays; DEBUGGING

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;

import uk.ac.wlv.sentistrength.SentiStrength;

/**
 * @author Amiangshu
 * @author jakereed
 *
 */
public class SentimentTest {
	
	/**
	 * Reads the .csv file as an input to the program 
	 * to be used against SentiStrength.
	 * @param fileName .csv file that will be used for human coded data 
	 * @return The array list that has the information regarding comments and human coded values
	 * @throws IOException Thrown when there is an issue reading the file or one does not exist
	 */
	public ArrayList<RatedComment> readCSVFile(String fileName) throws IOException{
		// Reader created for the file
		CSVReader reader = new CSVReader(new FileReader(fileName));
	    
		// ArrayList of type RatedComment will store the comments from the .csv file 
		ArrayList<RatedComment> oracle = new ArrayList<RatedComment>();
		String [] nextLine; 
	        
	    // Read from the file until all comments have been read
	    while ((nextLine = reader.readNext()) != null) {
	    	RatedComment comment= new RatedComment(nextLine[1], Integer.parseInt(nextLine[2]));
	    	oracle.add(comment);
	     }
		return oracle;
	}
	
	/**
	 * Writes individual sentiment results to a .csv file for
	 * better understanding of how SentiStrength is scoring comments.
	 * Will be handy in optimizing SentiStrength.
	 * @param posSentiment Positive sentiment score given to the comment
	 * @param negSentiment Negative Sentiment score given to the comment
	 * @param comBody The comment itself
	 * @throws IOException Thrown if the file does not exist
	 */
	public void writeIndividualResultsToFile(int posSentiment, int negSentiment, String comBody) throws IOException{
		CSVWriter writer = new CSVWriter(new FileWriter("indiv_results.csv"), '\t');
	}
	
	/**
	 * Constructor for the SentiStrength runner program.
	 * This will take in a .csv file containing the human codedd
	 * values, comments, and the comment number to be processed by
	 * SentiStrength.
	 * @param oracleFile  .csv file that will be read like a DB table containing comments, comment number, 
	 * and the human coded final rating.
	 */
	public SentimentTest(String oracleFile){
		SentiStrength sentiStrength = new SentiStrength(); 
		String ssthInitialisation[] = {"sentidata", "./data/","trinary"};
		sentiStrength.initialise(ssthInitialisation); 
		int numComment = 0;
		int numCorrect = 0;
		
		try {
			ArrayList<RatedComment> commentOracle=readCSVFile(oracleFile);
			for(RatedComment comment : commentOracle ) {
				numComment++;
				String[] sentiResult = sentiStrength.computeSentimentScores(comment.getComments()).split("\\s+");
				
				// System.out.println(Arrays.toString(sentiResult) + comment.getComments()); DEBUGGING
				
				// Parse the human coded rating from the .csv file
				int rating = Integer.parseInt(sentiResult[2]);
				
				// Increment the number of correct answers if the human code value and sentiment value are equivalent 
				if(comment.getRating()==rating)
					numCorrect++;								
			}
			
			// Compute the acurracy of SentiStrength by taking the given result divided by the human coded result
			float accuracy = ((float)numCorrect/(float)numComment) * 100;
			
			// Output the accuracy to the console
			System.out.println("Total comment "+ numComment+ ", Got accurate: "+numCorrect);
			System.out.println("Accuracy: "+accuracy);
			
		} catch (IOException e) { // Catch any errors with reading the file
			System.out.println("ERROR:  Unable to read the file!");
			e.printStackTrace();
			return;
			
		}
	}
	
	/**
	 * Runs the program and calculates how successful 
	 * SentiStrength was in determining whether or not
	 * the sentiment was positive negative or neutral
	 * @param args
	 */
	public static void main(String[] args) {
		// Create a new test object and run SentiStrength
		SentimentTest test=new SentimentTest("Sentiment-comments.csv");
	}

}
