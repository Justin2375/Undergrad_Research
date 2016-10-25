/**
 * 
 */
package edu.siu.sentiment;

import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

import com.opencsv.CSVReader;

import uk.ac.wlv.sentistrength.SentiStrength;

/**
 * @author Amiangshu
 *
 */
public class SentimentTest {

	
	public ArrayList<RatedComment> readCSVFile(String fileName) throws IOException{
		
		CSVReader reader = new CSVReader(new FileReader(fileName));
	    
		ArrayList<RatedComment> oracle=new ArrayList<RatedComment>();
		String [] nextLine;
	        
	    
	    while ((nextLine = reader.readNext()) != null) {
	        
	    	RatedComment comment= new RatedComment(nextLine[1], Integer.parseInt(nextLine[2]));
	    	oracle.add(comment);
	        
	     }
		return oracle;
	}
	
	
	public SentimentTest(String oracleFile){
		SentiStrength sentiStrength = new SentiStrength(); 
		String ssthInitialisation[] = {"sentidata", "./data/","trinary"};
		sentiStrength.initialise(ssthInitialisation); 
		int numComment=0;
		int numCorrect=0;
		
		try {
			ArrayList<RatedComment> commentOracle=readCSVFile(oracleFile);
			
			for(RatedComment comment : commentOracle )
			{
				numComment++;
				String[] sentiResult=sentiStrength.computeSentimentScores(comment.getComments()).split("\\s+");
				
				int rating=Integer.parseInt(sentiResult[2]);
				
				if(comment.getRating()==rating)
					numCorrect++;				
								
			}
			
			float accuracy= (float)numCorrect/(float)numComment;
			
			System.out.println("Total comment "+ numComment+ ", Got accurate: "+numCorrect);
			System.out.println("Accuracy: "+accuracy);
			
		} catch (IOException e) {
			
			e.printStackTrace();
			return;
			
		}
		
		
		
	}
	
	public static void main(String[] args) {
		
		SentimentTest test=new SentimentTest("Sentiment-comments.csv");
	}

}
